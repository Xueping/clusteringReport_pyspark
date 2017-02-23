'''
Created on 17 Jan 2017

@author: xuepeng
'''

import json
from pyspark import SparkContext
from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.mllib.clustering import KMeans
from pyspark.mllib.linalg import Vectors
from pyspark.sql.context import SQLContext
import random
import subprocess
import sys
import tempfile

def parseRowOneHotRegression(line, categoricalFeatures,originalFeature):
     
    feature = []
       
    for of in originalFeature:
        feature.append(line[of])
        
    for f in categoricalFeatures:
        feature.extend(line[f+'Vec'].toArray())
         
    return  (Vectors.dense(feature),line)

def indexAndEncode(processedData,features):
    
    encodedFinal = processedData
    for feature in features:
        
        stringIndexer = StringIndexer(inputCol=feature, outputCol=feature+"Index")
        model = stringIndexer.fit(encodedFinal) # Input data-frame is the cleaned one from above
        indexed = model.transform(encodedFinal)
        encoder = OneHotEncoder(dropLast=False, inputCol=feature+"Index", outputCol=feature+"Vec")
        encodedFinal = encoder.transform(indexed)

    return encodedFinal


def clustering(data,clusterNum,allFeatures):
     
    res = []
    
    model = KMeans.train(data.map(lambda item : item[0]), clusterNum ,10)
    
    #get partition of current data set 
    clusters = model.predict(data.map(lambda item : item[0])) 
    
    #     index each row, the format is (index, cluster)
    labels = clusters.zipWithIndex().map(lambda (v,i) : (i,v)) 
    
    #join by index to let each row map to a cluster
    labeledData = labels.join(data.zipWithIndex().map( lambda (v,i) : (i,v)))
    
    #records in each cluster 
    clusteredData = labeledData.map(lambda f : f[1]).groupByKey()
    
    #convert into cluster id, record number, and records
    ids = clusteredData.map(lambda f :(f[0],len(f[1]),f[1])).collect()
    
    for a in range(0,len(ids)) :
        clust = ids[a][0]
        size  = ids[a][1]
        newPoints = clusteredData.context.parallelize(ids[a][2])
        
        
        child = {"name": str(size) , "clusterId":str(clust)}
        
        for index in allFeatures:
            feature = newPoints.map(lambda item: item[1][index]).map ( lambda x : (x,1)).reduceByKey(lambda a, b: a + b).collect()
            strBuilder = ""
            for item  in feature:
                strBuilder = strBuilder +  item[0] + ":" + str(item[1]) + ","
            strBuilder = strBuilder[:-1]
            child[index] = strBuilder 
        
        if ids[a][1] > 100:
            child["children"] = clustering(newPoints,clusterNum,allFeatures)
            res.append(child)
        else:
            child["size"] = str(random.randint(500,1000))
            res.append(child)
            
    return res



   
if __name__ == "__main__":
    
#     ./spark-submit --master local[11] \
#     /home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/src/clustering/sparkClustering.py \
#     /home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/resource/source/demo.csv 5 \
#     /home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/resource/dependency-files \
#     "/user/longgu/output"


#     srcFile = "../../resource/source/demo.csv"
    dataFile     = str(sys.argv[1]) #data file
#     "/home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/resource/output/conf.json"
    confFile     = str(sys.argv[2]) #data file
#     clusterNum = 5
    clusterNum   = int(sys.argv[3]) #cluster number
#     srcFile      = str(sys.argv[3]) #static file to show web page
    output       = str(sys.argv[4]) #target file path
    
    #read json file from HDFS
    cat = subprocess.Popen(["hadoop", "fs", "-cat", confFile], stdout=subprocess.PIPE)
     
    #concenate string to JSON 
    jsonStr = ''
    for line in cat.stdout:
        jsonStr = jsonStr + line
    #load and parse Json
    conf = json.loads(jsonStr)
    
    allFeatures = conf['feature']
    categoricalFeatures = conf['categoricalFeature']
    
    originalFeature = []
    for cf in allFeatures:
        if cf not in categoricalFeatures:
            originalFeature.append(cf)
    
    
    sc = SparkContext()   
    sqlContext = SQLContext(sc)
    
    rawData = sc.textFile(dataFile)
    header = rawData.first()
    rawData_withoutHeader = rawData.filter(lambda x : (x != header) and ",," not in x)
    
    
    df = rawData_withoutHeader.map(lambda item : item.split(",")).toDF(header.split(","))
    dataSet = df.select(allFeatures)
    encodeDataSet = indexAndEncode(dataSet,categoricalFeatures)
      
    data = encodeDataSet.rdd.map(lambda line : parseRowOneHotRegression(line, categoricalFeatures,originalFeature))
    
    res = []
    child = {"name": str(data.count()) , "clusterId":"Initial Data"}
    
    for index in allFeatures:
        feature = data.map(lambda item: item[1][index]).map ( lambda x : (x,1)).reduceByKey(lambda a, b: a + b).collect()
        strBuilder = ""
        for item  in feature:
            strBuilder = strBuilder +  item[0] + ":" + str(item[1]) + ","
        strBuilder = strBuilder[:-1]
        child[index] = strBuilder
        
    child["children"] = clustering(data,clusterNum,allFeatures)   
    res.append(child)
    
    temp = tempfile.NamedTemporaryFile()
    try:
        json.dump(res[0], temp)
        temp.seek(0)
        
        subprocess.check_call(["hadoop","fs","-put","-f",temp.name, output]) 
        subprocess.check_call(["hadoop","fs","-rm",output+"/results.json"])      
        subprocess.check_call(["hadoop","fs","-mv",output+"/"+temp.name.split("/")[2], output+"/results.json"])
        
        print temp.read()
        print 'temp:', temp
        print 'temp.name:', temp.name
    finally:
        # Automatically cleans up the file
        temp.close()



'''
Created on 7 Feb 2017

@author: xuepeng
'''
import json
from pyspark.context import SparkContext
from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.sql.context import SQLContext
import subprocess
from pyspark.mllib.linalg import Vectors

def parseRowOneHotRegression(line, allFeatures, categoricalFeatures,originalFeature):
     
    feature = []
    strFeature = ''
    
    for af in allFeatures:
        strFeature = strFeature + str(line[af])+','
       
    for of in originalFeature:
        feature.append(line[of])
        
    for f in categoricalFeatures:
        feature.extend(line[f+'Vec'].toArray())
         
    return  (Vectors.dense(feature),strFeature[:-1])

def indexAndEncode(processedData,features):
    
    encodedFinal = processedData
    for feature in features:
        
        stringIndexer = StringIndexer(inputCol=feature, outputCol=feature+"Index")
        model = stringIndexer.fit(encodedFinal) # Input data-frame is the cleaned one from above
        indexed = model.transform(encodedFinal)
        encoder = OneHotEncoder(dropLast=False, inputCol=feature+"Index", outputCol=feature+"Vec")
        encodedFinal = encoder.transform(indexed)

    return encodedFinal


if __name__ == "__main__":

    #read json file from HDFS
    cat = subprocess.Popen(["hadoop", "fs", "-cat", "/home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/resource/output/conf.json"], stdout=subprocess.PIPE)
     
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
    print originalFeature
     
    sc = SparkContext("local[10]", "clusteringReport")
    sqlContext = SQLContext(sc)
    dataFile = "../../resource/source/demo.csv"
        
    rawData = sc.textFile(dataFile)
    header = rawData.first()
    rawData_withoutHeader = rawData.filter(lambda x : (x != header) and ",," not in x)
        
    df = rawData_withoutHeader.map(lambda item : item.split(",")).toDF(header.split(","))
      
    dataSet = df.select(conf['feature'])
    dataSet.show()
      
    encodeDataSet = indexAndEncode(dataSet,conf['categoricalFeature'])
      
    encodeDataSet.show()
     
    print conf['categoricalFeature']
    print conf['categoricalFeature']
     
    processedData = encodeDataSet.map(lambda line : parseRowOneHotRegression(line, allFeatures, categoricalFeatures,originalFeature)).collect()
    
    for i in range(10):
        print processedData[i][0]
        print processedData[i][1]
    
#     processedData.show()
     
#     print len(processedData)
    

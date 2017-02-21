'''
Created on 17 Jan 2017

@author: xuepeng
'''
''' hello world, it is a test of VI command by Guodong '''
from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans
from pyspark.mllib.linalg import Vectors
import random
import sys
import tempfile
import subprocess


def dataPreprocess(line,ethnicities,payors,admissions):
     
    values = line.split(",")
        
    label     = values.pop(0)
    ethnicity = values.pop(0)
    payor     = values.pop(0)
    admission = values.pop(0)
    vector = map(lambda x: float(x), values)
    
    newEthnicityFeatures = [0.0] * len(ethnicities)
    newEthnicityFeatures[ethnicities[ethnicity]] = 1.0
    
    newPayorFeatures = [0.0] * len(payors)
    newPayorFeatures[payors[payor]] = 1.0
    
    newAdmissionFeatures = [0.0] * len(admissions)
    newAdmissionFeatures[admissions[admission]] = 1.0
     
    vector.extend(newAdmissionFeatures)
    vector.extend(newPayorFeatures)
    vector.extend(newEthnicityFeatures)
         
    originalStr = label + "," + ethnicity + "," + payor +"," + admission
         
    return (Vectors.dense(vector), originalStr)
    
    
def vectorization(normalizedData):

    ethnicities = normalizedData.map(lambda item : item.split(",")[1]).distinct().zipWithIndex().collect()
    ethnicities = dict((key, value) for (key, value) in ethnicities)
    payors      = normalizedData.map(lambda item : item.split(",")[2]).distinct().zipWithIndex().collect()
    payors = dict((key, value) for (key, value) in payors)
    admissions  = normalizedData.map(lambda item : item.split(",")[3]).distinct().zipWithIndex().collect()
    admissions = dict((key, value) for (key, value) in admissions)

    return normalizedData.map(lambda item : dataPreprocess(item,ethnicities,payors,admissions))

def clustering(data,clusterNum):
     
    strBuilder = ""
    
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
           
        statisticEthnicity  = newPoints.map(lambda item: item[1].split(",")[1]).map ( lambda x : (x,1)).reduceByKey(lambda a, b: a + b).collect()
        statisticPayor      = newPoints.map(lambda item: item[1].split(",")[2]).map ( lambda x : (x,1)).reduceByKey(lambda a, b: a + b).collect()
        statisticAdmission  = newPoints.map(lambda item: item[1].split(",")[3]).map ( lambda x : (x,1)).reduceByKey(lambda a, b: a + b).collect()
            
        strBuilder = strBuilder + "{\"name\":"+ str(size) + ",\"clusterId\":" + str(clust) + ",\"eth\":{"
          
        for item in statisticEthnicity:
            strBuilder = strBuilder + "\"e" +item[0] + "\":" + str(item[1]) + ","
          
          
        strBuilder = strBuilder +"},\"payor\":{"
                
        for item in statisticPayor:
            strBuilder = strBuilder + "\"p" + item[0] + "\":" + str(item[1]) +","
          
                
        strBuilder = strBuilder +"},\"adm\":{"

        for item in statisticAdmission:
            strBuilder = strBuilder +"\"a" + item[0] + "\":" + str(item[1]) + ","
         
           
        if ids[a][1] > 100:
            strBuilder = strBuilder +"},\"children\":[" + clustering(newPoints,clusterNum) + "]},"
           
        else:
            strBuilder = strBuilder + "},\"size\":" + str(random.randint(500,1000)) + "},"
    
      
    return strBuilder

def readData(dataFile):
    
#     demoFile = "../../resource/source/demo.csv"  # Should be some file on your system
    
sc = SparkContext("local[10]", "clusteringReport")
    rawData = sc.textFile(dataFile)
    header = rawData.first()
    rawData_withoutHeader = rawData.filter(lambda x : (x != header) and ",," not in x)

    return vectorization(rawData_withoutHeader)
   
if __name__ == "__main__":
    
#     ./spark-submit --master local[11] \
#     /home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/src/clustering/sparkClustering.py \
#     /home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/resource/source/demo.csv 5 \
#     /home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/resource/dependency-files \
#     "/user/longgu/output"


#     srcFile = "../../resource/source/demo.csv"
    dataFile     = str(sys.argv[1]) #data file
#     clusterNum = 5
    clusterNum   = int(sys.argv[2]) #cluster number
#     srcFile      = str(sys.argv[3]) #static file to show web page
    output       = str(sys.argv[3]) #target file path
    
    
    sc = SparkContext("local[10]", "clusteringReport")
    rawData = sc.textFile(dataFile)
    header = rawData.first()
    rawData_withoutHeader = rawData.filter(lambda x : (x != header) and ",," not in x)
    data = vectorization(rawData_withoutHeader)
    


    statisticEthnicity  = data.map(lambda item: item[1].split(",")[1]).map ( lambda x : (x,1)).reduceByKey(lambda a, b: a + b).collect()
    statisticPayor      = data.map(lambda item: item[1].split(",")[2]).map ( lambda x : (x,1)).reduceByKey(lambda a, b: a + b).collect()
    statisticAdmission  = data.map(lambda item: item[1].split(",")[3]).map ( lambda x : (x,1)).reduceByKey(lambda a, b: a + b).collect()
  
        
    strBuilder = ""
    strBuilder = strBuilder + "{\"name\":" + str(data.count()) + ",\"clusterId\": \"Initial Data\",\"eth\":{"
      
    for item  in statisticEthnicity:
        strBuilder = strBuilder + "\"e" + item[0] + "\":" + str(item[1]) + ","
      
    strBuilder = strBuilder + "},\"payor\":{"
      
    for item in statisticPayor:
        strBuilder = strBuilder + "\"p" + item[0] + "\":" + str(item[1]) + ","
     
    strBuilder = strBuilder + "},\"adm\":{"
     
    for item in statisticAdmission:
        strBuilder = strBuilder + "\"a" + item[0] + "\":" + str(item[1]) + ","
     
    strBuilder = strBuilder + "},\"children\":["
       
    strBuilder = strBuilder + clustering(data,clusterNum) + "]}"
    strBuilder = strBuilder.replace(",]", "]").replace(",}", "}")
    

    temp = tempfile.NamedTemporaryFile()
    try:
        temp.write(strBuilder)
        temp.seek(0)
        
        subprocess.check_call(["hadoop","fs","-put","-f",temp.name, output])        
        subprocess.check_call(["hadoop","fs","-mv",output+"/"+temp.name.split("/")[2], output+"/results.json"])
        
        print temp.read()
        print 'temp:', temp
        print 'temp.name:', temp.name
    finally:
        # Automatically cleans up the file
        temp.close()


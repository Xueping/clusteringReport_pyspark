'''
Created on 13 Jan 2017

@author: xuepeng
'''

from pyspark.mllib.clustering import KMeans
import random

from clustering.dataProcessing import readData
from html.generateHtmlZip import zipFile
import sys


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
   
if __name__ == "__main__":
    
#     srcFile = "../../resource/source/demo.csv"
    srcFile = str(sys.argv[1])
#     clusterNum = 5
    clusterNum = int(sys.argv[2])
        
    data = readData(srcFile)
    
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
    
    zipFile(strBuilder)

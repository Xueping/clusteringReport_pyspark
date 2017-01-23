'''
Created on 17 Jan 2017

@author: xuepeng
'''

from pyspark import SparkContext
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.clustering import KMeans
import random
import sys
import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root,dirs, files in os.walk(path):
        for f in files:
            ziph.write(os.path.join("dependency-files/", f))
            
def zipFile(jsonStr,srcFile,output):     
    message = """   
    <html>
        <head>
            <meta http-equiv="Content_Type" content="text/html; charset=UTF-8" />
            <link type="text/css" rel="stylesheet" href="./dependency-files/style.css" />
            <link type="text/css" rel="stylesheet" href="./dependency-files/bootstrap.min.css" />
            <script type="text/javascript" src="./dependency-files/d3.layout.js.download"></script>
            <script type="text/javascript" src="./dependency-files/d3pie.js"></script>
            <script type="text/javascript" src="./dependency-files/jquery.js"></script>
            <script type="text/javascript" src="./dependency-files/d3.min.js"></script>
        </head>
        <body>
            <div id="header">Offline Web-based Interactive Clustering Analysis Report</div>
            <div id="body"></div>
            <div id="popup">
                <div class="row">
                    <div class="col-md-4" id="pie_gender"></div>
                    <div class="col-md-4" id="pie_age"></div>
                    <div class="col-md-4" id="pie_freq"></div>
                </div>
            </div>
            <script type="text/javascript">var flare = '"""+ jsonStr +"""' </script>
            <script type="text/javascript" src="./dependency-files/clusterReport.js"></script>
        </body>
    </html>
    """
    if os.path.exists(output + '/zipfile_writestr.zip'):
        os.remove(output + '/zipfile_writestr.zip')
    
    zf = zipfile.ZipFile(output + '/zipfile_writestr.zip', 
                     mode='a',
                     compression=zipfile.ZIP_DEFLATED, 
                     )
    try:        
        zf.writestr('offline_clustering_report.html', message)
        zipdir(srcFile, zf)
    finally:
        zf.close()   


def readData(dataFile):
    
#     demoFile = "../../resource/source/demo.csv"  # Should be some file on your system
    sc = SparkContext("local[10]", "clusteringReport")
    rawData = sc.textFile(dataFile)
    header = rawData.first()
    rawData_withoutHeader = rawData.filter(lambda x : (x != header) and ",," not in x)

    return vectorization(rawData_withoutHeader)
    
    
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
   
if __name__ == "__main__":
    
#     ./spark-submit --master local[11] \
#     /home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/src/clustering/sparkClustering.py \
#     /home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/resource/source/demo.csv 5 \
#     /home/xuepeng/Documents/workspace-sts/clusteringReport_pyspark/resource/dependency-files \
#     /home/xuepeng/output


#     srcFile = "../../resource/source/demo.csv"
    dataFile     = str(sys.argv[1]) #data file
#     clusterNum = 5
    clusterNum   = int(sys.argv[2]) #cluster number
    srcFile      = str(sys.argv[3]) #static file to show web page
    output       = str(sys.argv[4]) #target file path
    
        
    data = readData(dataFile)
     
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
    
    zipFile(strBuilder,srcFile,output)

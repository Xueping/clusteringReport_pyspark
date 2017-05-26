from pyspark.context import SparkContext
from pyspark.mllib.clustering import KMeans
import subprocess
from time import time

import numpy as np


def generateTestFile(localFolder,HDFS_folder, numFeatures, numRows):
        
    testFile = np.random.randn(numRows, numFeatures)
    np.savetxt(localFolder+"hadoop_test_file.csv", testFile, delimiter=",",fmt="%10.2f")
    subprocess.check_call(["hadoop","fs","-put","-f",localFolder+"hadoop_test_file.csv", HDFS_folder]) 
    

if __name__ == "__main__":
    
    numClusters   = 5 #cluster number
    localFolder   = "/home/xuepeng/data/doh_hadoop_test/"
    HDFS_folder = "/home/xuepeng/output/"
    numFeatures = 100
    numRows = 1000000
    
    
    #Step 1 -- generate testing Data and put the data into HDFS
    generateTestFile(localFolder,HDFS_folder,numFeatures, numRows)
    
    sc = SparkContext("local[20]", "Hadoop_test") 
    #Step 2 - Spark Clustering with single big data file
    
    startTime = time()
    dataFile = HDFS_folder+"hadoop_test_file.csv"
    rawData = sc.textFile(dataFile)
    data = rawData.map(lambda item : item.split(","))
    model = KMeans.train(data, numClusters ,10)
    endTime = time()
    
    print 'Spent {} seconds in clustering {} rows with {} features.'.format((endTime - startTime),numRows,numFeatures)
    
    print model.centers

    
    
    
    
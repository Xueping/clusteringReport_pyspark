'''
Created on 13 Jan 2017

@author: xuepeng
'''

from pyspark import SparkContext
from pyspark.mllib.linalg import Vectors


def readData(srcFile):
    
#     demoFile = "../../resource/source/demo.csv"  # Should be some file on your system
    sc = SparkContext("local[10]", "clusteringReport")
    rawData = sc.textFile(srcFile)
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
    
#     print originalStr
         
    return (Vectors.dense(vector), originalStr)
    
    
def vectorization(normalizedData):

    ethnicities = normalizedData.map(lambda item : item.split(",")[1]).distinct().zipWithIndex().collect()
    ethnicities = dict((key, value) for (key, value) in ethnicities)
    payors      = normalizedData.map(lambda item : item.split(",")[2]).distinct().zipWithIndex().collect()
    payors = dict((key, value) for (key, value) in payors)
    admissions  = normalizedData.map(lambda item : item.split(",")[3]).distinct().zipWithIndex().collect()
    admissions = dict((key, value) for (key, value) in admissions)

    return normalizedData.map(lambda item : dataPreprocess(item,ethnicities,payors,admissions))
           

    
if __name__ == '__main__':
    readData()

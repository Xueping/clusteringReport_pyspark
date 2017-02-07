'''
Created on 7 Feb 2017

@author: xuepeng
'''
# from pyspark.context import SparkContext
# from pyspark.sql.context import SQLContext
# 
# 
# sc = SparkContext("local[10]", "clusteringReport")
# sqlContext = SQLContext(sc)
# dataFile = "../../resource/source/demo.csv"
# 
# rawData = sc.textFile(dataFile)
# header = rawData.first()
# rawData_withoutHeader = rawData.filter(lambda x : (x != header) and ",," not in x)
# 
# df = rawData_withoutHeader.map(lambda item : item.split(",")).toDF(header.split(","))
# df.select("subject_id", "ethnicity_itemid").show()

for index in range(1,8):
    print index
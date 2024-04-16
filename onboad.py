import os
import py4j
import math
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import numpy as np
from pyspark.streaming import StreamingContext
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time

spark = SparkSession.builder.config("spark.driver.memory", "6G").getOrCreate()


def convert_acc(x): 
    x = int(x,16) 
    if x>127: 
        x = x-256 
    return np.float64(x*0.01536)

def transform_data(accData):
    if accData is None:
        return np.array([[0], [0], [0]])
    if(len(accData) == 0):
        return np.array([[0], [0], [0]])
    if(len(accData) == 162):
         # Get the magnetometer values
         mx = convert_acc(accData[0:4]) 
        
         my = convert_acc(accData[4:8]) 
         
         mz = convert_acc(accData[8:12]) 
         
         # Get the accelerometer values
         rest = accData[12:]
         for i in range(0, len(rest), 6): 
             x = convert_acc(rest[i:i+2]) 
             y = convert_acc(rest[i+2:i+4]) 
             z = convert_acc(rest[i+4:i+6]) 

             # Calculate the angles
             if z == 0:
                 z = 1
             phi = math.atan(y/z)
             theta = math.atan(-x/(y*math.sin(phi)+z*math.cos(phi)))
             psi = math.atan((mz*math.sin(phi) - my*math.cos(phi))/(mx*math.cos(theta) + my*math.sin(theta)*math.sin(phi) + mz*math.sin(theta)*math.cos(phi)))

             Rx = np.array([[1,0,0], [0,math.cos(phi),math.sin(phi)], [0,-math.sin(phi),math.cos(phi)]])
             Ry = np.array([[math.cos(theta),0,-math.sin(theta)], [0,1,0], [math.sin(theta),0,math.cos(theta)]])
             Rz = np.array([[math.cos(phi),math.sin(phi),0], [-math.sin(phi),math.cos(phi),0], [0,0,1]])

             R = Rx.dot(Ry).dot(Rz)
             R = np.linalg.inv(R)
             
             # Apply rotation matrix and store the values
             A = np.array([[x], [y], [z]]) 
             B = np.dot(R, A)
             
             x,y,z = B[:,0] 

             return np.array([[x], [y], [z]])   
 

    return np.array([[0], [0], [0]])

def sendRow(row):
    jsondata = {"deviceID": row["deviceID"], "timestamp": str(row["timeStamp"]), "accData": str(transform_data(row["accData"])), "gps_speed": row["gps_speed"]}
    time.sleep(0.030)
    publish.single("ortus/oboard/" + str(row["deviceID"]), json.dumps(jsondata), hostname="localhost")


file_location = "./data/allVehicles.csv.gz"
file_type = "csv"
infer_schema = "true"
first_row_is_header = "true"
delimiter = ","

pattern = "yyyy-MM-dd HH:mm:ss"

df = spark.read.format(file_type) \
    .option("inferSchema", infer_schema) \
    .option("header", first_row_is_header) \
    .option("sep", delimiter) \
    .load(file_location)

# Failed attempts to sort the data by timestamp
#dfSorted = df.sort(unix_timestamp(df["timeStamp"], 'yyyy-MM-dd HH:mm:ss').cast("timestamp").asc())

# dfSorted = df.withColumn("timeStamp", unix_timestamp(df["timeStamp"], pattern)).orderBy(col("timeStamp"))

df.foreach(lambda x: sendRow(x))



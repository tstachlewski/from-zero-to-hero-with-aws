
#wget http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.0.4.zip#md5=3df394d89300db95163f17c843ef49df
#unzip mysql-connector-python-2.0.4.zip
#cd mysql-connector-python-2.0.4
#sudo python3 setup.py install


import mysql.connector
import os

mydb = mysql.connector.connect(
  host="MY-ENDPOINT",
  user="USER",
  password="PASSWORD"
)


mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE bidata")
mycursor.execute("USE bidata")
mycursor.execute("CREATE TABLE people ( id INTEGER, age INTEGER, firstname VARCHAR(255), lastname VARCHAR(255), country VARCHAR(255), sex VARCHAR(255), numberofkids INTEGER, revenue DOUBLE, leavingincity VARCHAR(255), likemusic VARCHAR(255), likecinema VARCHAR(255), bankbalance DOUBLE, happinnessratio DOUBLE, height INT, weight INT )")
mycursor.execute("COMMIT");

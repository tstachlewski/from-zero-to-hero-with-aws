import mysql.connector
import os

mydb = mysql.connector.connect(
  host="ENDPOINT",
  user="USER",
  password="PASSWORD"
)


mycursor = mydb.cursor()
mycursor.execute("USE bidata")

directory = os.fsencode("data")
    
for file in os.listdir(directory):
    filename = "data/" + os.fsdecode(file)
    print(filename);
    

    with open(filename) as f:
        for line in f:
            line = line.strip()
            attributes = line.split(",")
            mycursor.execute("INSERT INTO people VALUES ('" + attributes[0] + "','" + attributes[1] + "','" + attributes[2] + "','" + attributes[3] + "','" + attributes[4] + "','" + attributes[5] + "','" + attributes[6] + "','" + attributes[7] + "','" + attributes[8] + "','" + attributes[9] + "','" + attributes[10] + "','" + attributes[11] + "','" + attributes[12] + "','" + attributes[13] + "','" + attributes[14] + "')");
    
            
        
    mycursor.execute("COMMIT");
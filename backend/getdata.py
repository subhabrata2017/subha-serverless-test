import json
import os
import pymysql

endpoint = os.environ['endpoint']
dbname = os.environ['dbname']
username = os.environ['username']
dbPassword = os.environ['dbPassword']
tableName = os.environ['tableName']

response = {
    "success": False,
    "data": []
}

try:
    connection = pymysql.connect(host=endpoint, user=username, passwd=dbPassword, db=dbname, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
except pymysql.MySQLError as e:
    print('Error in DB ', e)
    response = {
        "success": False,
        "data": []
    }

def getData():
    
    cursor = connection.cursor()

    if event["rawPath"] == "/getusers":
        cursor.execute("SELECT * FROM "+tableName )
    else:
        cursor.execute("SELECT * FROM "+tableName+" WHERE empId="+event["pathParameters"]["empId"] )

    rows = cursor.fetchall()
    payload = []
    content = {}
    for row in rows:        
        content = {'empId': row['empId'], 'name': row['first_name']+' '+row['last_name'] , 'designation': row   ['designation']}
        payload.append(content)
        content = {}

    if not payload:
        response = {
            "success": True,
            "data": []
        } 
    else:
        response = {
            "success": True,
            "data": payload
        }       
    connection.commit()        
    return response    

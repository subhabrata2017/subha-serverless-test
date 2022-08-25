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
    connection = pymysql.connect(host=endpoint, user=username, passwd=dbPassword, db=dbname, connect_timeout=5)
except pymysql.MySQLError as e:
    print('Error in DB ', e)
    response = {
        "success": False,
        "data": []
    }

def setData(event, context):
    payload = json.loads(event['body']) 
    cursor = connection.cursor()
    sql = "INSERT INTO "+tableName+" (first_name, last_name, designation) VALUES (%s, %s, %s)"

    try:
        cursor.execute(sql,(payload['first_name'], payload['last_name'], payload['designation']))
        response = {
            "success": True,
            "body": json.dumps("User "+payload['first_name']+" registered successfully")
        }
    except:
        response = {
            'statusCode': 400,
            'body': json.dumps('Error saving the data')
        }
    connection.commit()

    return response
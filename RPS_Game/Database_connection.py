"""
importing the database connector and adding the connections to connect database.
Class and the method calls in the main file.
"""
import mysql.connector

class MysqlDB:
    def getConnection():
        con = mysql.connector.connect(host='localhost',
                                      database='RPS_Info',
                                      user='root',
                                      password='Priyathars@14'
                                      )
        return con

    getConnection()



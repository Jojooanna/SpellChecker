import pymysql

connection = pymysql.connect(host='localhost', user='wpdbuser', password='wpdbpassword', db= 'wpdb' )
cursor = connection.cursor()
sql = 'CREATE DATABASE spelling'
cursor.execute(sql)

commonwords = '''CREATE TABLE common (
       id INT(3) PRIMARY,
       word VARCHAR(50) DEFAULT
       )
       '''
cursor.execute(commonwords)
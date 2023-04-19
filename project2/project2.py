
import mysql.connector as msc
from mysql.connector import Error

try: 
    connection = msc.connect(host = 'localhost',
                                       database = 'project2',
                                       user = 'root',
                                       password = '') #Password OMITTED, as it's a personall password
    if connection.is_connected():
        dbInfo = connection.get_server_info()
        print("Connected to MySQL Server Version: ", dbInfo)
        cursor = connection.cursor()
        cursor.execute("select database(); ")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        
        print("\n")

        #################################################################################################################################################

        #first query  -- print all entries in project2.publishers table
        query = ('SELECT * FROM project2.publishers')
        cursor.execute(query)
        print("first query  -- print all entries in project2.publishers table")
        for x in cursor:
            print(x)
        
        print("\n")

        #################################################################################################################################################

        # #second query -- create table projec2.customers with schema custID,custName,zip,city,state; PK custID
        # query = ('CREATE TABLE project2.customers (custID INT(5), custName VARCHAR(50), zip VARCHAR(10), city VARCHAR(30), state VARCHAR(30))')
        # cursor.execute(query)

        # #checking second query
        print("second query -- create table projec2.customers with schema custID,custName,zip,city,state; PK custID")
        cursor.execute('SHOW TABLES') #testing if table was succesfully created
        for x in cursor:
            print(x)

        print("\n")

        #################################################################################################################################################

        # # third query -- inserting values into customers.
        query = 'INSERT IGNORE INTO project2.customers (custID, custName, zip, city, state) VALUES (%s, %s, %s, %s, %s)'
        newCust = [
            (1,'STEPHEN WALTHER', '92399', 'Yucaipa', 'California'),
            (2,'JAMES GOODWILL', '92373', 'Redlands', 'California'),
            (3,'CALVIN HARRIS', '92318', 'Loma Linda', 'California'),
            (4,'MARTIN GARRIX', '92501', 'Riverside', 'California'),
            (5,'PAMELA REIF', '92240', 'Palm Springs', 'California')
        ]

        cursor.executemany(query, newCust)
        connection.commit()
        
        #checking solution
        print("third query -- inserting values into customers.")
        cursor.execute('SELECT * FROM project2.customers') #testing if table was succesfully created
        for x in cursor:
            print(x)

        print("\n")

        #################################################################################################################################################

        # #fourth query --  Form  a  query  to  print  the  names  of  those  who  appear  in  both  “author” and  “customer.” 
        query = 'SELECT c.custName \
        FROM project2.customers AS c, project2.authors AS a \
        WHERE c.custName = a.aName'

        cursor.execute(query)
        print("fourth query --  Form  a  query  to  print  the  names  of  those  who  appear  in  both  “author” and  “customer.”")
        #check the returned results.
        for x in cursor: 
            print (x)

        print("\n")
        #################################################################################################################################################

        # #fifth query -- Form a query to find subjects in which the minimum price is $400 and maximum price is $550.
        query = 'SELECT s.sName \
                 FROM project2.subjects AS s, (SELECT t.subID FROM project2.titles AS t WHERE (t.price >= 400 AND t.price <= 550)) AS res \
                 WHERE  s.subID = res.SUBID'
        cursor.execute(query)
        #check the returned results.
        print("fifth query -- Form a query to find subjects in which the minimum price is $400 and maximum price is $550.")
        for x in cursor: 
            print (x)
        
        print("\n")
        #################################################################################################################################################

        # #Sixth Query -  Form a query to change the price of title 1001 to the price of the most recently published book.
        # #BEFORE: project2.titles We are going to check the table before.
        cursor.execute('SELECT * FROM project2.titles')
        print('Before project2.titles\n')
        for x in cursor:
            print(x)
        print('\n')

        
        query = 'UPDATE project2.titles AS t, (SELECT titles.price FROM project2.titles ORDER BY pubDate DESC LIMIT 1 ) AS res \
                 SET t.price = res.price \
                 WHERE t.titleID = 1001;'
        # cursor.execute(query)
        #AFTER:  project2.titles, most recent book is PRO VB NET on 2005-06-15
        #check the returned results.
        print('Sixth Query -  Form a query to change the price of title 1001 to the price of the most recently published book.')
        cursor.execute('SELECT * FROM project2.titles')
        for x in cursor: 
            print (x)

        print("\n")

        #################################################################################################################################################

        # #Seventh query: Form a query to find titles published by the publisher whose name contains ‘T’. 
        # #By looking at publishers, the only publishers that we need to output are pubID 3, and 4. 

        #solution
        query = "SELECT t.title \
                 FROM project2.titles AS t, (SELECT publishers.pubID \
							                 FROM project2.publishers \
							                 WHERE (publishers.pname REGEXP '^T')) AS res \
                 WHERE t.pubID = res.pubID"
        cursor.execute(query)

        # Checking the solution.
        print("Seventh query: Form a query to find titles published by the publisher whose name contains ‘T’.")
        for x in cursor:
            print(x)

        print("\n")
        #################################################################################################################################################
        
        # #8th query: Insert  a  row  into  titleauthors  for  title  ‘java.comp.ref’ and author  'DAVAID HUNTER.' 
        # #creating a table where we extract results titleID for JAVA COMP REF and auID DAVAID HUNTER"
        queryDh = 'SELECT t.titleID, a.auID \
                 FROM project2.titles AS t \
                 NATURAL JOIN project2.authors AS a \
                 WHERE t.title = "JAVA COMP. REF" AND a.aName = "DAVAID HUNTER"'

        # cursor.execute(queryDh)
        # #fetching results
        res = cursor.fetchall()
        #insert query, NULL by default
        query = 'INSERT IGNORE INTO project2.titleauthors (titleID, auID, importance) VALUES (%s, %s, NULL)'
        cursor.executemany(query, res)
        connection.commit()

        #check solution
        print("QUERY 8: Insert  a  row  into  titleauthors  for  title  ‘java.comp.ref’ and author  'DAVAID HUNTER.'")
        cursor.execute('SELECT * FROM project2.titleauthors')
        for x in cursor:
            print(x)

        print("\n")

        #################################################################################################################################################
        # # 9th query: Form  a  query  to  find  author  names  who  have  written  any  title  with  author 'HERBERT SCHILD.'
        query = "SELECT a.aName \
                FROM project2.titleauthors AS tc, \
                (SELECT ta.titleID, ta.auID \
                FROM project2.titleauthors AS ta, (SELECT auID\
                                                    FROM project2.authors\
                                                    WHERE aName = 'HERBERT SCHILD') AS tb\
                WHERE ta.auID = tb.auID) AS res, project2.authors AS a\
                WHERE tc.titleID = res.titleID AND tc.auID != res.auID AND tc.auID = a.auID"
        cursor.execute(query)
        #checking solution
        res = cursor.fetchall()
        print("9th query: Form  a  query  to  find  author  names  who  have  written  any  title  with  author 'HERBERT SCHILD.'")
        for x in res: 
            print(x)
        print("\n")
        #################################################################################################################################################
        # Form a query to decrease the price of all the books published before 2004 by 30% and decrease the price of all the books published after 2004 by 15%. 
        # BEFORE update:

        print("PROJECT 2 BEFORE PRICE ADJUSTMENT:")
        cursor.execute("SELECT * FROM project2.titles")
        # CHECKING THE SOLUTION
        for x in cursor:
            print(x)
        print("\n")
        query = "UPDATE project2.titles\
                SET titles.price = CASE\
                WHEN YEAR(titles.pubDate) < 2004 THEN (titles.price * .70)\
                WHEN YEAR(titles.pubDate) > 2004 THEN (titles.price * .85)\
                END"
        cursor.execute(query)

        print("Form a query to decrease the price of all the books published before 2004 by 30 and decrease the price of all the books published after 2004 by 15%.")
        cursor.execute("SELECT * FROM project2.titles")
        # CHECKING THE SOLUTION
        for x in cursor:
            print(x)


except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
import MySQLdb
import base64

class DBConnect:
    def __init__(self):
        hostname="remotemysql.com"
        username="XMOhqXsSa4"
        password="QbmL0ZttoO"
        database="XMOhqXsSa4"
        self.db_connection = MySQLdb.connect(hostname, username, password, database)
        # cursor = self.db_connection.cursor()

    def insertIntoTypes(self, types):
        query = f'''INSERT INTO types (`rs`,`rr`,`rm`,`ri`,`rt`,`ls`,`lr`,`lm`,`li`,`lt`)
        VALUES ('{types[0]}','{types[1]}','{types[2]}','{types[3]}','{types[4]}','{types[5]}','{types[6]}','{types[7]}','{types[8]}','{types[9]}')'''

        cursor = self.db_connection.cursor()
        cursor.execute(query)
        types_id = cursor.lastrowid
        self.db_connection.commit()
        cursor.close()
        return types_id

    def insertIntoRidgecount(self, ridgecount):
        query = f'''INSERT INTO ridgecount (rs,rr,rm,ri,rt,ls,lr,lm,li,lt)
        VALUES ({ridgecount[0]},{ridgecount[1]},{ridgecount[2]},{ridgecount[3]},{ridgecount[4]},
        {ridgecount[5]},{ridgecount[6]},{ridgecount[7]},{ridgecount[8]},{ridgecount[9]})'''

        cursor = self.db_connection.cursor()
        cursor.execute(query)
        rcID = cursor.lastrowid
        self.db_connection.commit()
        cursor.close()
        return rcID

    def insertIntoImages(self, images):
        img_blobs = []
        for img in images:
            with open(img, 'rb') as imgFile:
                img = imgFile.read()
                img_blobs.append(str(base64.b64encode(img))[1:])

        query = f'''INSERT INTO images(rs ,rr ,rm ,ri ,rt ,ls ,lr ,lm ,li ,lt )
        VALUES({img_blobs[0]},{img_blobs[1]},{img_blobs[2]},{img_blobs[3]},{img_blobs[4]},{img_blobs[5]},{img_blobs[6]},{img_blobs[7]},{img_blobs[8]},{img_blobs[9]})'''

        cursor = self.db_connection.cursor()
        cursor.execute(query)
        imageID = cursor.lastrowid
        self.db_connection.commit()
        cursor.close()
        return imageID

    def insertData(self, details):
        imageID = self.insertIntoImages(details['images'])
        rcID = self.insertIntoRidgecount(details['ridgecounts'])
        typesID = self.insertIntoTypes(details['types'])
        query = f'''INSERT INTO users(`NAME`,`DOB`,`GENDER`,`imageID`,`ridgeCountID`,`typeID`)
        VALUES ('{details["name"]}','{details["dob"]}','{details["gender"]}', '{imageID}','{rcID}','{typesID}')'''
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        id = cursor.lastrowid
        self.db_connection.commit()
        cursor.close()
        self.db_connection.close()
        return id

    def getDetails(self, rowID):
        row = str(rowID)
        query = f"SELECT * FROM users where ID='{row}';"
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        return cursor.fetchone()

from mysql.connector import errorcode
from mysql import connector
import base64


def connect_db(conn_details):
    try:
        db = connector.connect(**conn_details)
    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        print(err)
    else:
        return db


def get_names_from_file(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())
    return lines


def insert_into_images(cursor, filenames):
    img_blobs = []
    for file in filenames:
        # read image into variable
        with open(file, 'rb') as f:
            img = f.read()
            img_blobs.append(str(base64.b64encode(img))[1:])
        # print(img_blobs[i] is not None)

    # store images in db
    # imagetb_columns = ['l1','l2','l3','l4','l5','r1','r2','r3','r4','r5']
    query = f'''INSERT INTO images
(`rs`,`rr`,`rm`,`ri`,`rt`,`ls`,`lr`,`lm`,`li`,`lt`)
VALUES({img_blobs[0]},{img_blobs[1]},{img_blobs[2]},{img_blobs[3]},{img_blobs[4]},{img_blobs[5]},{img_blobs[6]},{img_blobs[7]},{img_blobs[8]},{img_blobs[9]})'''
    # query = f'''INSERT INTO images (rs) VALUES ({img_blobs[0]})'''
    # query2 = f'SELECT * FROM FINGERPRINTS.IMAGES'
    try:
        cursor.execute(query)
        images_id = cursor.lastrowid
    except Exception as e:
        print(f'Could not insert images into the table.')
        print(e)
        return None
    else:
        return images_id


def insert_into_types(cursor, filenames):
    # Change code to call matching module on each image
    # for i in filename:
        # match(filename)

    # STUB
    types = ['A','A','R','A','A','A','A','R','R','R']

    query = f'''INSERT INTO types (`rs`,`rr`,`rm`,`ri`,`rt`,`ls`,`lr`,`lm`,`li`,`lt`)
VALUES ('{types[0]}','{types[1]}','{types[2]}','{types[3]}','{types[4]}','{types[5]}','{types[6]}','{types[7]}','{types[8]}','{types[9]}')'''

    try:
        cursor.execute(query)
        types_id = cursor.lastrowid
    except Exception as e:
        print(f'Could not insert types into the table.')
        print(e)
        return None
    else:
        return types_id


def insert_into_ridgecount(cursor, filenames):
    # Change code to call ridge_count module on each image
    # for i in filename:
        # count_ridges(filename)

    # STUB
    rc = [10,9,8,9,11,10,11,10,10,11]

    query = f'''INSERT INTO ridgecount (`rs`,`rr`,`rm`,`ri`,`rt`,`ls`,`lr`,`lm`,`li`,`lt`)
VALUES ({rc[0]},{rc[1]},{rc[2]},{rc[3]},{rc[4]},{rc[5]},{rc[6]},{rc[7]},{rc[8]},{rc[9]})'''

    try:
        cursor.execute(query)
        rc_id = cursor.lastrowid
    except Exception as e:
        print(f'Could not insert ridge counts into the table.')
        print(e)
        return None
    else:
        return rc_id

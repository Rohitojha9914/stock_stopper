import psycopg2
import pandas as pd


conn = psycopg2.connect(
   database="stock", user='rohit', password='1234', host='localhost', port= '5432'
)


cursor = conn.cursor()
postgreSQL_select_Query = "select * from listedcompany"

cursor.execute(postgreSQL_select_Query)
data = cursor.fetchall()
print(data[0][2])

 
# # read by default 1st sheet of an excel file
# df = pd.read_excel('stock.xlsx')

# for index, row in df.iterrows():
#     print(row['id'], row['symbol'], row['company_name'])



def insert_listedcompany():
    sql = """INSERT INTO listedcompany(id, company_name, symbol) VALUES(%s, %s, %s ) """
    conn = None

    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect( database="stock", user='rohit', password='1234', host='localhost', port= '5432')


        # create a new cursor
        cur = conn.cursor()
        
        # execute the INSERT statement
        df = pd.read_excel('stock.xlsx')
        for index, row in df.iterrows():
            print(row['id'], row['symbol'], row['company_name'])

            cur.execute(sql, (row['id'], row['company_name'], row['symbol'],))
        # get the generated id back

            conn.commit()
            # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# def insertAllStock():

# insert_listedcompany()
            


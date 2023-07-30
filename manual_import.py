import psycopg2

file = "all_Bitcoin_addresses_ever_used_sorted.txt"
host="localhost"
dbname="btc"
user="YOUR_USERNAME"
password="YOUR_PASSWORD"
tbl_name="tempaddr"
main_tbl="addresses"
conn_string = "host=%s dbname=%s user=%s password=%s" % (host, dbname, user, password)

def upload_to_db(file):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('opened database')
    my_file = open(file)
    print('file opened in memory')
    #upload to db
    SQL_STATEMENT = """
    COPY %s FROM STDIN WITH
        CSV
        HEADER
        DELIMITER AS ','
    """
    cursor.copy_expert(sql=SQL_STATEMENT % tbl_name, file=my_file)
    print('file copied to db')
    cursor.execute("grant select on table %s to public" % tbl_name)
    conn.commit()
    print("committed")
    cursor.execute("INSERT INTO {} SELECT address FROM {} ON CONFLICT DO NOTHING;".format(main_tbl, tbl_name))
    print("inserted into main table")
    conn.commit()
    cursor.execute("truncate {};".format(tbl_name))
    print('file {} imported to db?'.format(file))
    conn.commit()
    cursor.close()
    return

upload_to_db(file)
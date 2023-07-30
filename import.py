from urllib.request import urlopen
from os.path import basename
from lxml import html
import requests
import psycopg2

file = ""
url = 'http://alladdresses.loyce.club/daily_updates/'
lastfile = 'import.log'
host="localhost"
dbname="btc"
user="YOUR_USERNAME"
password="YOUR_PASSWORD"
tbl_name="tempaddr"
main_tbl="addresses"
conn_string = "host=%s dbname=%s user=%s password=%s" % (host, dbname, user, password)

# adds last imported file to import.log
def append_new_line(file_name, text_to_append):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text_to_append)

def download_file(link):
    data = requests.get(url+link)
    with open(link, 'wb') as newfile:
        newfile.write(data.content)

# DB stuff, gets a local filename as parameter
def upload_to_db(file):
    print("downloading file")
    download_file(file)
    print("file downloaded")
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
    print("truncating temp table")
    cursor.execute("truncate {};".format(tbl_name))
    filename = file.split('.')[0]
    date = filename[len(filename) -8:]
    append_new_line(lastfile,date)
    print("appending last date to import.log")
    os.remove(file)
    print("file {} deleted".format(file))
    print('file {} imported to db?'.format(file))
    conn.commit()
    cursor.close()
    return

# gets last line of file import.log to compare with the last available dump
def get_last_insert():
    with open(lastfile, "rb") as filelast:
        filelast.seek(-2, 2)
        while filelast.read(1) != b'\n':
            filelast.seek(-2, 1)
        last_line = filelast.readline().decode()
    return last_line

# returns filename to download
def check_new_data():
    response = urlopen(url)
    webpage = html.fromstring(response.read())
    links=[]
    last_line = get_last_insert()
    for link in webpage.xpath('//a/@href'):
        if "freshly" in link:
            links.append(link)
    for link in links:
        #print(url+link)
        filename = link.split('.')[0]
        date = filename[len(filename) -8:]
        if int(last_line) < int(date):
            print("importing {} as last imported was {}".format(date, last_line))
            upload_to_db(link)
        else:
            print("not importing {}".format(date))

check_new_data()
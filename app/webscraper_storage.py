import os
import mysql.connector
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
load_dotenv()


# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



def extract_item():
    url = os.getenv("URL")
    conn = mysql.connector.connect(
        host='localhost',
        user='postgres',
        password='postgres',
        database='test_schema'
    )
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html')
    text_content = soup.get_text()
    title = soup.title.string
    process_item(url,text_content,title,conn)


def process_item(url,content,title,conn):
    cur = conn.cursor()
    cur.execute(""" insert into harry_potter (id,url,content, title) values (%s,%s,%s,%s)""",
        (1,
         url,
         content,
         title))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    extract_item()
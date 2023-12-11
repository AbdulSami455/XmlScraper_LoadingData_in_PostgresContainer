#!/usr/bin/env python3

import sys
import psycopg2
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <fname>")
    sys.exit(1)

fname = sys.argv[1]

processed_pages = 0
#total_pages = 17_434_651
total_pages = 10000
xml = ""
in_page = False

# функция подключения к БД
db = psycopg2.connect(host="localhost", port=5440,  user="wiki", database="wiki")
cursor = db.cursor()
db.autocommit=True 


cursor.execute('create table if not exists ' +
  'articles(id serial primary key, title varchar(128), content text);')

cursor.execute("CREATE OR REPLACE FUNCTION make_tsvector(title TEXT, content TEXT) \
   RETURNS tsvector AS $$ \
BEGIN \
  RETURN (setweight(to_tsvector(title),'A') || \
    setweight(to_tsvector(content), 'B')); \
END \
$$ LANGUAGE 'plpgsql' IMMUTABLE;")

#функция пагинации
def process_page(page_xml):
    global processed_pages, insert
    doc = BeautifulSoup(f"<page>{page_xml}</page>", 'xml')
    title = doc.page.title.string[:127]
    content = doc.page.revision.findAll('text')[0].string
    processed_pages += 1
    print(f"Processing page {processed_pages} of {total_pages} " +
          f"({processed_pages * 100 / total_pages}%) with title '{title}'")

#    print("insert into articles (title, content) values (%s, %s)",  (title, content))
    cursor.execute('insert into articles (title, content) values (%s, %s);', (title, content))
count=0

#парсинг 
with open(fname) as f:
    for line in f:
       if line.strip() == '<page>':
           xml = ""
           in_page = True
           continue
       elif line.strip() == '</page>':
           process_page(xml)
           in_page = False

       if in_page:
           xml += line
       count += 1;
       if total_pages < count: break

cursor.execute("create index if not exists idx_fts_articles on articles " +
  "using gin((setweight(to_tsvector('russian', title),'A') ||" +
  "setweight(to_tsvector('russian', content), 'B')));")
#cursor.execute("create index if not exists idx_fts_articles on articles " +
#  "using gin((setweight(to_tsvector(title),'A') ||" +
#  "setweight(to_tsvector(content), 'B')));")

if db:
    cursor.close()
    db.close()
    print("PostgreSQL connection is closed")


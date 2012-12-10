from __future__ import print_function
from bs4 import BeautifulSoup
import urllib2
import json

class Book:
  title = ""
  link = ""
  score = ""

  genres = []

  def __str__(self):
    return self.title + str(self.genres)

books = []

f = urllib2.urlopen('http://www.goodreads.com/list/show/1.Best_Books_Ever')

soup = BeautifulSoup(f)

def get_genres(link):
  genre_list = []
  booklink = urllib2.urlopen(link)
  booksoup = BeautifulSoup(booklink)

  genres = booksoup.find_all("a")
  for g in genres:
    if g.get("href") is None: continue

    if "genre" in g.get("href"):
      genre_list.append(g.contents[0])

  return genre_list

print("[")

for tr in soup.find_all("tr"):
  bk = {}

  scores = tr.find("span", class_="minirating").contents[1].split(" ")

  bk['title'] = tr.contents[3].contents[3].get("title")
  bk['score'] = float(scores[1])
  bk['ratings'] = int(scores[5].replace(",", ""))
  partial_link = tr.find("a", class_="bookTitle").get("href")

  link = "http://www.goodreads.com/" + partial_link
  bk['genres'] = get_genres(link)

  print(json.dumps(bk), ",")


print("]")

#for link in soup.find_all("a", class_="bookTitle"):
#  print link
#  print link.get('href')

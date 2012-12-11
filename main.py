from __future__ import print_function
from bs4 import BeautifulSoup
import sys
import re
import urllib2
import json

def get_info(link):
  genre_list = []
  booklink = urllib2.urlopen(link)
  booksoup = BeautifulSoup(booklink)

  rating_dist = booksoup.find_all("span", id="rating_graph")
  nums = [int(x) for x in re.findall(r'\d+', str(rating_dist[0].script))]

  genres = booksoup.find_all("a")
  for g in genres:
    if g.get("href") is None: continue

    if "genre" in g.get("href"):
      genre_list.append(g.contents[0])

  grantscore = float(nums[0])/float(nums[1]) if nums[1] != 0 else 0

  return (genre_list, grantscore)

print("var bigdata = [")

def dump_page(page):
  f = urllib2.urlopen('http://www.goodreads.com/list/show/1.Best_Books_Ever?page=' + str(page))

  soup = BeautifulSoup(f)

  books = 0

  for tr in soup.find_all("tr"):
    books += 1

    sys.stderr.write("book " + str(books) + "\n")
    bk = {}

    scores = tr.find("span", class_="minirating").contents[1].split(" ")

    bk['title'] = tr.contents[3].contents[3].get("title")
    bk['score'] = float(scores[1])
    bk['ratings'] = int(scores[5].replace(",", ""))
    partial_link = tr.find("a", class_="bookTitle").get("href")

    link = "http://www.goodreads.com/" + partial_link
    bk['genres'], bk['grantscore'] = get_info(link)

    print(json.dumps(bk), ",")

for x in range(1, 10):
  sys.stderr.write("=================== page " + str(x) + "======================" + "\n")
  dump_page(x)

print("]")

#for link in soup.find_all("a", class_="bookTitle"):
#  print link
#  print link.get('href')

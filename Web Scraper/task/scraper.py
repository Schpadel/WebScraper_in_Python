import re
import string
import requests
import string
import os
from bs4 import BeautifulSoup

number_of_pages = int(input("Please enter the number of pages to search: "))
type_of_articles = input("Please enter the type of article to extract: ")

for i in range(1, number_of_pages + 1):
    os.mkdir("Page_" + str(i))
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=" + str(i)
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")

    articles = soup.find_all("article")

    for article in articles:
        spans = article.find_all("span", {"data-test": "article.type"})
        for span in spans:
            if span.text.strip() == type_of_articles:
                link = article.find("a", {"data-track-action": "view article"})
                print(link["href"])  # link to article content found when type == type_of_articles
                request_article = requests.get("https://www.nature.com" + link["href"])
                soup_article = BeautifulSoup(request_article.content, "html.parser")
                article_title = soup_article.find("h1").text
                translation_table = article_title.maketrans("", "", string.punctuation)  # remove spaces and so on in title to use as file name
                article_title = article_title.translate(translation_table)
                article_title = article_title.replace(" ", "_")
                article_body = soup_article.find("div", {"class": re.compile('.*article.*body|.*article__.*teaser')})
                article_body = article_body.text.strip()
                encoded_content = article_body.encode("UTF-8")
                file = open(os.getcwd() + "\\Page_" + str(i) + "\\" + article_title + ".txt", 'wb')
                file.write(encoded_content)
                print("Saved article with the name: " + article_title + " in the folder: " + "Page_" + str(i))
                file.close()

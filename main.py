import http.cookiejar
import urllib.request
import bs4
import re
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.jewelryshows.org/en/trade/exhibitor_directory.php";
head = "https://www.jewelryshows.org/en/trade/"
searchlist = "https://www.jewelryshows.org/en/trade/exhibitor_directory.php?page="
max = 61
begin = 2

response = urllib.request.urlopen(url);

request = urllib.request.Request(url)
#模拟Mozilla浏览器进行爬虫
request.add_header("user-agent","Mozilla/5.0")
response = urllib.request.urlopen(request)
print (response.getcode())
html_doc = response.read()
print (len(html_doc))
email_container=[]
name_container = []

soup = BeautifulSoup(html_doc,"html.parser",from_encoding="utf-8")
links = soup.find_all('tr')
temp = []
for link in links:
    test = link.get("href")
    if test!= None:
        temp.append(test)

while begin < max:
    target = (searchlist+str(begin))
    begin+=1
    response2 = urllib.request.urlopen(target)
    request2 = urllib.request.Request(target)
    request2.add_header("user-agent","Mozilla/5.0")
    response2 = urllib.request.urlopen(request2)
    html_doc2 = response2.read()
    soup2 = BeautifulSoup(html_doc2,"html.parser",from_encoding="utf-8")
    links2 = soup2.find_all('tr')
    for link in links2:
        test = link.get("href")
        if test != None:
            temp.append(test)

for item in temp:
    reponse1 = urllib.request.urlopen(head+item)
    request1 = urllib.request.Request(head+item)
    request1.add_header("user-agent","Mozilla/5.0")
    response1 = urllib.request.urlopen(request1)
    html_doc1 = response1.read()
    soup1 = BeautifulSoup(html_doc1,"html.parser",from_encoding="utf-8")
    required_div = soup1.find_all("div", attrs="field")
    temp_name = required_div[0].get_text()
    for item in required_div:
        if item.find("a") != None:
            email_container.append(item.find('a').get("href"))
            name_container.append(temp_name)
            break


print(email_container)
print(len(email_container))
print(name_container)
print(len(name_container))
df = pd.DataFrame(email_container)
df.to_excel(excel_writer = "/home/pianist/crawler_test/email.xlsx")
df = pd.DataFrame(name_container)
df.to_excel(excel_writer = "/home/pianist/crawler_test/main.xlsx")


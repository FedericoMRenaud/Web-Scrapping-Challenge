from flask import Flask, render_template
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
from flask_pymongo import PyMongo

app=Flask(__name__)

@app.route("/scrape")
def echo():
        return render_template("template.html")

#Chromedriver
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#URL FOR TITLE AND P
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)

# Retrieve page with the requests module
response = requests.get(url)

# results are returned as an iterable list
news_title = soup.find("div","a", class_="content_title")
news_title=news_title.text.replace("\n","")

#Retrieve p from url
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
news_p = soup.find('div', class_='article_teaser_body').text

#Read 2nd URL
url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url2)

#Scrap image url
html_image = browser.html
soup = BeautifulSoup(html_image, 'html.parser')
image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
first_url = 'https://www.jpl.nasa.gov'
image_url = first_url +image_url

#Read 3rd URL
url3 = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url3)

#Mars weather scrapped from twitter page
mars_weather="InSight sol 455 (2020-03-08) low -95.4ºC (-139.8ºF) high -13.0ºC (8.5ºF)"

url4 = 'https://space-facts.com/mars/'

#Pandas DF From 3rd URL
mars_facts = pd.read_html(url4)
mars_df = mars_facts[0]

mars_df.columns = ['Factor','Value']
mars_df.set_index('Factor', inplace=True)
mars_df.to_html()

#Visit fifth url
url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url5)

#Scrap hemisphere urls from fifth url
hemisphere_image_urls = []
links = browser.find_by_css("a.product-item h3")
for item in range(len(links)):
    hemisphere = {}
    browser.find_by_css("a.product-item h3")[item].click()
    
    search = browser.find_link_by_text("Sample").first
    hemisphere["img_url"] = search["href"]

    hemisphere["title"] = browser.find_by_css("h2.title").text
    hemisphere_image_urls.append(hemisphere)

    browser.back()
 
 
@app.route("/")
def echo():
        return render_template("template.html", news_title=news_title, news_p=news_p, image_url=image_url, mars_weather=mars_weather, mars_df=mars_df, hemisphere_image_urls=hemisphere_image_urls)

if __name__=="__main__":
     app.run(debug=True)
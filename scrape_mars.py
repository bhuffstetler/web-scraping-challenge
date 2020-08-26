# Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import time
import pandas as pd



executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser('chrome', **executable_path, headless=False)
mars_dict = {} # --- create dictionary

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

hemispheres = []

def scrape():
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Wait for the page/page elements to load.
    time.sleep(1)
    # Visit the NASA Mars News Site.
    

    # Scrape page into soup.
    html = browser.html
    soup = bs(html, "html.parser")

    first_article = soup.find('ul', class_='item_list')

    # Get latest news title and paragraph text.
    news_title = first_article.find('div', class_='content_title').text
    news_p = first_article.find('div', class_="article_teaser_body").text
    print(f"Latest news title: {news_title}.")
    print(f"Latest news paragraph text: {news_p}")
    mars_dict["news_title"]=news_title
    mars_dict["news_p"]=news_p

    #    Visit the url for JPL Featured Space Image.
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Wait for page/page elements to load.


    # Scrape page into soup.
    html = browser.html
    soup = bs(html, "html.parser")

    # Get image url for featured image.
    featured_image_base_url = "https://www.jpl.nasa.gov"
    featured_image_relative_path = soup.find('li', class_='slide').a['data-fancybox-href']
    featured_image_url = featured_image_base_url + featured_image_relative_path
    print(f"Featured image url: {featured_image_url}")
    mars_dict["featured_image_url"]=featured_image_url 

    # In[6]:


    #    Visit the Mars Weather twitter account.
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Wait for the page/page elements to load.
    time.sleep(8)

    # Scrape page into soup.
    html = browser.html
    soup = bs(html, "html.parser")

    # Get latest Mars weather tweet.
    mars_weather_tweet = soup.find(attrs={"data-testid" : "tweet"})
    mars_weather_tweet_text = mars_weather_tweet.text

    mars_weather_list = mars_weather_tweet_text.split("InSight")
    mars_weather = mars_weather_list[1]

    print(f"Latest Mars weather tweet: {mars_weather}")
    mars_dict["mars_weather"]=mars_weather

    # In[7]:


    # Visit url for mars facts.
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    # Wait for page/page elements to load.
    time.sleep(1)

    # Scrape page into soup.
    html = browser.html
    soup = bs(html, "html.parser")

    # Get Mars facts table using pandas.
    tables = pd.read_html(url)
    tables


    # In[8]:


    # Convert table for site to pandas dataframe.
    df = tables[0]
    df.columns = ["Measurement", "Value"]
    df.set_index("Measurement", inplace=True)
    df.head()


    # In[9]:


    # Convert pandas dataframe to a html string.
    html_table = df.to_html()
    html_table


    # In[10]:


    # Remove any new line characters from the html string.
    html_table.replace('\n', '')


    # In[11]:


    # Save the html string to a file.
    df.to_html('web-scraping-challenge')
    mars_dict["html_table"]=html_table

    # In[12]:

    # Visit url for images of Mar's hemispheres.
    base_url = "https://astrogeology.usgs.gov"
    hemisphere_list_url = base_url + "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_list_url)

    # Wait for the page/page elements to load.
    time.sleep(1)

    # Scrape page into soup.
    html = browser.html
    soup = bs(html, "html.parser")

    # Get hemisphere name and image url for the full resolution image.
    hemispheres = soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    for hemisphere in hemispheres:
        link_text = hemisphere.find('h3').text
        splitted = link_text.split('Enhanced')
        title = splitted[0]
        browser.click_link_by_partial_text(link_text)
        hemisphere_page_html = browser.html
        soup = bs(hemisphere_page_html, "html.parser")
        downloads = soup.find('div', class_="downloads")
        img_url = downloads.a["href"]
        hemisphere_dict = { "title": title, "img_url": img_url }
        hemisphere_image_urls.append(hemisphere_dict)
        mars_dict["hemisphere_image_urls"]=hemisphere_image_urls

        browser.back()

    mars_dict.update({"Hemispheres": hemisphere_image_urls})

    return mars_dict

    browser.quit()




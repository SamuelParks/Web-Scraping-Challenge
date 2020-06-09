

# Dependencies
import os
from bs4 import BeautifulSoup
import datetime
import pandas as pd

#This opens and runs browsers for you with the program
from splinter import Browser

# Module used to connect Python with MongoDb
import pymongo

#To find things in a string this library is used
import re

# NOT using the Requests modules [response = requests.get(url)] because it does not reliably pull in all of the html from the page
# import requests


def scrape():
    latest_mars_data = {}

    # ### NASA Mars News

    # In[2]:


    # URL of page to be scraped
    url1 = 'https://mars.nasa.gov/news/'


    # In[3]:


    # NOT using the Requests modules [response = requests.get(url)] because it does not reliably pull in all of the html from the page


    # In[4]:


    #This starts up Splinter and the browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser1 = Browser('chrome', **executable_path, headless=False)


    # In[5]:


    browser1.visit(url1)


    # In[6]:


    html1 = browser1.html


    # In[7]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html1, 'html.parser')


    # In[8]:


    # Examine the results, then determine element that contains sought info
    print(soup.prettify())


    # In[ ]:


    browser1.quit()


    # In[9]:


    # Results are returned as an iterable list
    #This only finds the first (lateset one)

    #This corrects for a tag issue
    news_titles_with_links = soup.find_all(class_='content_title')
    news_titles_with_links = news_titles_with_links[1]


    # In[10]:


    
    news_p = soup.find(class_='article_teaser_body')


    # In[11]:

    news_title = news_titles_with_links.text
    news_p = news_p.text

    # news_p = news_p.text


    # In[12]:


    news_title


    # In[13]:


    news_p


    # ### JPL Mars Space Images - Featured Image

    # In[14]:


    #This starts up Splinter and the browser

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser2 = Browser('chrome', **executable_path, headless=False)


    # In[15]:


    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser2.visit(url2)


    # In[16]:


    html2 = browser2.html


    # In[17]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup2 = BeautifulSoup(html2, 'html.parser')


    # In[ ]:


    browser2.quit()


    # In[18]:


    # results are returned as an iterable list
    image_pull = soup2.find_all(class_='carousel_item')


    # In[19]:


    #Turning it into a string so that I can get the url below
    image_pull_string =  str(image_pull[0])


    # In[20]:


    str(image_pull[0])


    # In[21]:


    #Extracting the url as closely as possible
    featured_image_url=re.search('url(.*)>', image_pull_string)


    # In[22]:


    #Removing the excess characters from the string that weren't part of the url
    featured_image_url=featured_image_url.group(0)[5:-5]


    # In[23]:


    # Base URL added to make an bsolute URL
    base_featured_image_url = f"https://www.jpl.nasa.gov{featured_image_url}"
    print(base_featured_image_url)


    # ### Mars Weather from Twitter

    # In[ ]:


    # NOTE: The Twitter section has been removed from the assignment due to rapid changes in the Twitter html code


    # In[24]:


    # #This starts up Splinter and the browser
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser3 = Browser('chrome', **executable_path, headless=False)

    # url3 = 'https://twitter.com/marswxreport?lang=en'
    # browser3.visit(url3)

    # html3 = browser3.html


    # In[25]:


    # # Create BeautifulSoup object; parse with 'html.parser'
    # soup3 = BeautifulSoup(html3, 'html.parser')


    # In[26]:


    # # The sol in the line below is the phrase in the tweets that indicates were the information is for this specific account.

    # twitter_text= re.compile(r'sol')
    # mars_weather=soup3.find('span', text=twitter_text).text
    # print(mars_weather)


    # In[ ]:


    # browser3.quit()


    # ### Mars Facts

    # In[27]:


    # We can use the read_html function in Pandas to automatically scrape any tabular data from a page.
    url_Mars_Facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_Mars_Facts)
    Mars_Facts_df = tables[0]

    Mars_Facts_df.columns = ["Description", "Value"]
    Mars_Facts_df.set_index('Description', inplace=True)
    Mars_Facts_df.head()

    
    # In[28]:


    #Changes the table to an html string
    html_table = Mars_Facts_df.to_html()

    #You may have to strip unwanted newlines to clean up the table. This line will do that.
    #This line does not see to have an effect in this instance though.
    html_table.replace('\n', '')

    html_table


    # ### Mars Hemisphere

    # In[42]:


    #This starts up Splinter and the browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser4 = Browser('chrome', **executable_path, headless=False)

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser4.visit(url4)

    html4 = browser4.html


    # In[43]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup4 = BeautifulSoup(html4, 'html.parser')


    # In[44]:


    # This creates the empty list with the required name from the instructions
    hemisphere_image_urls = []                                                   

    #This pulls our the first parts we are interested in 
    product_section = soup4.find('div', class_='result-list')   


    # In[45]:


    # Isolates hemisphere information
    hemisphere_info = product_section.find_all('div', class_='item')                        
    hemisphere_info


    # In[ ]:





    # In[46]:


    #This loop gets the title info and image urls for each hemiphere

    for element in hemisphere_info:
        title = element.find('div', class_='description')
        
        #This isolates just the text you want for the title
        title_text = title.a.text                      
        title_text = title_text.replace(' Enhanced', '')
        
        #This uses the title text to find the button to click and automatically clicks it
        browser4.click_link_by_partial_text(title_text)      
        
        #This records the html from the new page that you moved to 
        new_page_html = browser4.html
        #Makes BeautifulSoup objest from it
        new_page_soup = BeautifulSoup(new_page_html, 'html.parser')
        
        #This finds the link in the downloads section that you want to use and record
        image_html = new_page_soup.find('div', class_='downloads').find('ul').find('li')
        image_url = image_html.a['href']
        
        #This adds the information to the dictionary in the format the instructions give
        hemisphere_image_urls.append({'title': title_text, 'img_url': image_url})
        
        #This automatically makes Splinter click back one page
        browser4.back()


    # In[ ]:


    browser4.quit()

    time_pulled = datetime.datetime.now()

    latest_mars_data = {
    "news_title": news_title,
    "news_paragraph": news_p,
    "base_featured_image_url": base_featured_image_url,
    # Mars Weather was removed from the assignment due to changes with Twitter
    # "weather": mars_weather,
    "facts_table": html_table,
    "hemisphere_urls": hemisphere_image_urls,
    "time_pulled": time_pulled
    }
    return latest_mars_data
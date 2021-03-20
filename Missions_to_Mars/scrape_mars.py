from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": "C:/Install/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# execute all scraping code and return one Python dictionary
def scrape():
    browser = init_browser()
    mars_data = {}

    # ******************************
    #     NASA Mars News Site
    # ******************************

    # Scrape the NASA Mars News Site
    news_url="https://mars.nasa.gov/news/"
    
    # use splinter to navigate the site
    browser.visit(news_url)
    time.sleep(1)
    
    # use browser to pull html
    html = browser.html

    # parse html with BeautifulSoup
    soup = bs(html, "html.parser")

    # collect the latest News Title and Paragraph Text
    news_title = soup.find('div', class_='list_text').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    
    # *****************************************
    #   JPL Mars Space Images - Featured Image
    # *****************************************

    # get url
    jpl_url = "https://www.jpl.nasa.gov/images?search=&category=Mars"

    # use splinter to navigate the site
    browser.visit(jpl_url)
    time.sleep(1)

    # find the first image and click on it to go to the next page
    browser.find_by_css('.BaseImage').click()
    time.sleep(2)

    # grab the html at the new page
    html = browser.html

    # parse html with BeautifulSoup
    soup = bs(html, "html.parser")

    # find the link to the largest size image and assign the url string to a variable 
    featured_image_url = soup.find('a', class_='BaseButton')['href']


    # ******************************
    #     Mars Facts
    # ******************************

    # Visit the Mars Facts webpage
    facts_url = "https://space-facts.com/mars/"

    # read html tabular data from url into dataframe
    tables=pd.read_html(facts_url)

    # use index numbers to get to the right df
    table_df=tables[0]

    # generate html table from dataframe
    mars_facts = table_df.to_html(header=False, index=False)

    # strip unwanted newlines to clean up the table
    mars_facts = mars_facts.replace('\n','')


    # ******************************
    #     Mars Hemispheres
    # ******************************

    # Visit the USGS Astrogeology site
    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # use splinter to navigate the site
    browser.visit(astro_url)
    time.sleep(2)

    # obtain url for high resolution image and title for each of 4 Mars's hemispheres
    all_items = browser.find_by_css('.item') 

    hemisphere_image_urls=[]

    for item in range(len(all_items)):
        #img_dict={}

        # find the image thumbnail and click on it to go to the next page
        browser.find_by_css('.thumb')[item].click()

        # grab the html at the new page
        html = browser.html

        # parse HTML with BeautifulSoup
        soup = bs(html,'html.parser')

        # find image title
        title = soup.find('h2', class_='title').text

        # find image url
        img_url = soup.find('div', class_='downloads').find('a')['href']
        
        # append the dictionary to a list
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        
        # return to the previous page
        browser.back()


    # Store all scraped data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "mars_facts": mars_facts,
        "hemispheres": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
  

#!/usr/bin/env python
# coding: utf-8


# Import Panda.  Scrape the table below using Pandas () from https://galaxyfacts-mars.com/
import pandas as pd

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Setup Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things.
# 
# - One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). 
# As an example, ul.item_list would be found in HTML as \<ul class="item_list">. 
#     
# - Secondly, we're also telling our browser to wait one second before searching for components. 
# The optional delay is useful because sometimes dynamic pages take a little while to load, especially 
# if they are image-heavy.
#     
#     

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


slide_elem


# Begin Scraping
slide_elem.find('div', class_='content_title')


# #### We've added something new to our .find() method here: .get_text(). 
# - When this new method is chained onto .find(), only the text of the 
# element is returned. 


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### In the below cell: 
# 1. We're creating a new DataFrame from the HTML table. The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
# 
# 2. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
# 
# 3. Then, it turns the table into a DataFrame.


# Read the HTML table using Pandas
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


df.to_html()


# End Browser session
browser.quit()


#####################  START CHALLENGE   #####################


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
       
browser.visit(url)
#browser.is_element_present_by_css('div.list_text', wait_time=1)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemi_soup = soup(html, 'html.parser')

hemis = hemi_soup.find_all('h3')

for hemi in hemis:
    if 'Hemisphere' in hemi.text :
        title = hemi.text
        
        # Get Title Full Images
        imglink = browser.links.find_by_partial_text(title)
        imglink.click()
        
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        img = img_soup.find("ul") 
        img_href = img.find("a").get("href")
        img_url = f'https://marshemispheres.com/{img_href}'
        
        # Store data in dictionary
        hemispheres  = {}
        hemispheres  = {'img_url': img_url, 'title': title }
        # Store data in list
        hemisphere_image_urls.append(hemispheres)
        
        # Go back to original page
        browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()


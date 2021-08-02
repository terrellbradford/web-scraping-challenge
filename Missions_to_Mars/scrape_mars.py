# Importing Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time as tm
import pandas as pd


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    tm.sleep(1)

    #Scraping Featured Image
    html = browser.html
    soup = bs(html, "html.parser")

    featured = soup.find('img', class_='headerimage fade-in')['src']

    featured_image_url = image_url + featured

    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    tm.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    news = soup.find('div', class_='list_text')

    news_title = news.find(class_='content_title').text
    news_p = news.find(class_='article_teaser_body').text


    # Creating Mars Data Tables
    # URL Path to Mars Facts
    facts_url = "https://galaxyfacts-mars.com"

    table = pd.read_html(facts_url)

    df = table[1]
    header = df.iloc[0]
    facts_df = df[1:]
    facts_df.columns = header

    facts = facts_df.to_html(index=False)

    table2 = pd.read_html(facts_url)

    df2 = table2[0]
    header = df2.iloc[0]
    facts2_df = df2[1:]
    facts2_df.columns = header

    facts2 = facts2_df.to_html(index=False)

    # URL Path 
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)

    # Creating Dictionary of hemisphere_image_urls
    hemisphere_image_urls = []

    # For Loop Grab the Title and Image Path
    for x in range(0, 4):

        html = browser.html
        soup = bs(html, "html.parser")

        hemi_links = browser.links.find_by_partial_text('Hemisphere Enhanced')

        hemi_links[x].click()

        html = browser.html
        soup = bs(html, "html.parser")

        tm.sleep(1)

        hemi_image = soup.find('img', class_='wide-image')['src']
        img_title_clean = soup.find('h2', class_='title').text.strip('Enhanced').rstrip()

        img_url = hemi_url + hemi_image

        # Appending Dictionary to List
        hemisphere_image_urls.append({"Title": img_title_clean, "img_url": img_url})

        browser.links.find_by_partial_text('Back').click()

        tm.sleep(1)

    browser.quit()
        

    # Storing Data into Dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "facts": facts,
        "facts2": facts2,
        'featured': featured_image_url,
        "hemisphere_image_one": hemisphere_image_urls[0]['img_url'],
        "hemisphere_image_two": hemisphere_image_urls[1]['img_url'],
        "hemisphere_image_three": hemisphere_image_urls[2]['img_url'],
        "hemisphere_image_four": hemisphere_image_urls[3]['img_url'],
        "hemisphere_title_one": hemisphere_image_urls[0]['Title'],
        "hemisphere_title_two": hemisphere_image_urls[1]['Title'],
        "hemisphere_title_three": hemisphere_image_urls[2]['Title'],
        "hemisphere_title_four": hemisphere_image_urls[3]['Title'],
    }

    # Return Results
    return mars_data
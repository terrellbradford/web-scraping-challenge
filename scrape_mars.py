from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    news = soup.find('div', class_='list_text')

    news_title = news.find(class_='content_title').text
    news_content = news.find(class_='article_teaser_body').text

    news_data = {
        'title': news_title,
        'content': news_content
    }

    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    featured = soup.find('img', class_='headerimage fade-in')['src']

    featured_image_url = image_url + featured

    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)

    time.sleep(1)

    hemi_image_urls = []

    for x in range(0, 4):

        html = browser.html
        soup = bs(html, "html.parser")

        hemi_links = browser.links.find_by_partial_text('Hemisphere Enhanced')

        hemi_links[x].click()

        html = browser.html
        soup = bs(html, "html.parser")

        time.sleep(1)

        hemi_image = soup.find('img', class_='wide-image')['src']
        hemi_title = soup.find('h2', class_='title').text.strip('Enhanced').rstrip()

        img_url = hemi_url + hemi_image

        hemisphere = {
                'title': hemi_title,
                'img_url': img_url
            }
            
        hemi_image_urls.append(hemisphere)

        browser.links.find_by_partial_text('Back').click()

        time.sleep(1)

    browser.quit()

    facts_url = "https://galaxyfacts-mars.com/"

    table = pd.read_html(facts_url)

    df = table[0]
    header = df.iloc[0]
    facts_df = df[1:]
    facts_df.columns = header

    facts = facts_df.to_html()

    mars_data = {
        'news': news_data,
        'featured': featured_image_url,
        'facts': facts,
        'hemispheres': hemi_image_urls
    }

    return mars_data
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

news_title, news_paragraph = mars_news(browser)

# Run all scraping functions and store results in dictionary
data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "last_modified": dt.datetime.now()
}

# Create a mars_news function
def mars_news(broswer):
    # Visit the mars nasa new site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        ### Article scraping

        # Begin scraping
        # Article title
        slide_elem.find("div", class_='content_title')

        # Get just the text from the title
        # Use the parent element to find the first 'a' tag and save it as a 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Scrape the article summary
        slide_elem.find("div", class_='article_teaser_body').get_text()

        # Save the paragraph to a variable
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    # Return the function
    return news_title, news_p

### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click it
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Add error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    # Return the image
    return img_url


### Mars Facts

def mars_facts():
    try:
        # Set up the code to scrape the entire table
        df = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseExeption:
        return None

    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)

    # Return and convert the DF back to html for later use
    return df.to_html()

# End the browsing session
browser.quit()

# Signal that the function is complete
return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
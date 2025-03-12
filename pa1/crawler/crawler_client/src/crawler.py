from collections import deque
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

base = "https://www.bloomberg.com"
article = base + "/news/articles"
visited = set()


# A set discards duplicates automatically and is more efficient for lookups
articles = set()

to_crawl = deque()
to_crawl.append(base)

def crawl_link(input_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/bin/chromedriver")  # Ensure correct path
    browser = webdriver.Chrome(service=service, options=chrome_options)
    print(input_url)
    browser.get(input_url)
    elems = browser.find_elements(by=By.XPATH, value="//a[@href]")

    # this part was the issue, before this line there was 
    # `to_crawl.append()` which was prematurely adding links 
    # to the visited list so those links were skipped over without
    # being crawled
    visited.add(input_url)

    for elem in elems:

        # checks for errors
        try:
            url_element = elem.get_attribute("href")
        except StaleElementReferenceException as err:
            print(err)
            continue

        # checks to make sure links aren't being crawled more than once
        # and that all the links are in the propper domain
        if base in url_element and all(url_element not in i for i in [visited, to_crawl]):

            to_crawl.append(url_element)

            # this checks if the link matches the correct url pattern
            if article in url_element and url_element not in articles:

                articles.add(url_element)
                print(str(url_element))
                with open("result.txt", "a") as outf:
                    outf.write(str(url_element) + "\n")
    
    browser.quit() # guarantees the browser closes completely


while len(to_crawl):
    # popleft makes the deque a FIFO instead of LIFO.
    # A queue would achieve the same thing.
    url_to_crawl = to_crawl.popleft()

    crawl_link(url_to_crawl)
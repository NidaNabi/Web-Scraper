"""
Requirements: use pip install
Selenium
browserstack-sdk
browserstack-local

"""
#import the modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import requests
import re
from collections import Counter


# Folder to save images
image_dir = r"C:\Users\Nida Nabi\Downloads\browserstack\images"
os.makedirs(image_dir, exist_ok=True)

# Initialize browser
browser = webdriver.Chrome()
browser.get("https://elpais.com/")
print("Homepage Title:", browser.title)


def get_article_content(url):
    browser.execute_script(f"window.open('{url}');")
    browser.switch_to.window(browser.window_handles[1])
    try:
        content = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/article[1]/div[2]/p[1]"))
        ).text
    except:
        content = "Content not found"    
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    return content

def download_image(image_url, file_name):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            path = os.path.join(image_dir, file_name)
            with open(path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Image saved to {path}")
        else:
            print("Failed to download image:", image_url)
    except Exception as e:
        print(f"Error downloading image: {str(e)}")

import requests

def translate_to_english(text):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": "es|en"  
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["responseData"]["translatedText"]
        else:
            print("Translation API error:", response.text)
            return text
    except Exception as e:
        print("Translation failed:", str(e))
        return text

try:
    opinion_tab = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="csw"]/div[1]/nav/div/a[2]'))
    )
    
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", opinion_tab)
    time.sleep(1)
    
    browser.execute_script("arguments[0].click();", opinion_tab)
    print("\nNavigated to Opinion section")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "article.c.c-d.c--m"))
    )
    
    # Get first 5 articles
    articles = browser.find_elements(By.CSS_SELECTOR, "article.c.c-d.c--m")[:5]
    print(f"\nFound {len(articles)} opinion articles:")
    
    translated_titles = []

    for i, article in enumerate(articles, 1):
        try:
            # Scroll to find articles
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", article)
            time.sleep(0.5)
            
            # Extract data
            title = article.find_element(By.CSS_SELECTOR, "h2.c_t a").text
            url = article.find_element(By.CSS_SELECTOR, "h2.c_t a").get_attribute("href")
            translated_title = translate_to_english(title)
            translated_titles.append(translated_title)

            print(f"\nARTICLE {i}:")
            print(f"Original Title: {title}")
            print(f"Translated Title: {translated_title}")
            print(f"Link: {url}")
            content = get_article_content(url)

            print(f"Content: {content}...")
            print("-" * 80)
            #find and download img
            try:
                img_elem = article.find_element(By.CSS_SELECTOR, "img")
                img_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
                if img_url:
                    img_ext = img_url.split(".")[-1].split("?")[0]
                    file_name = f"article_{i}.{img_ext}"
                    download_image(img_url, file_name)
                else:
                    print("No image URL found.")
            except NoSuchElementException:
                print("No image element found.")
            
        except Exception as e:
            print(f"\nError processing article {i}: {str(e)}")
            continue
    


    # Analyze repeated words in translated titles
    all_words = []
    for t in translated_titles:
        words = re.findall(r'\b\w+\b', t.lower()) 
        all_words.extend(words)

    # Count and print repeated words
    word_counts = Counter(all_words)
    print("\nRepeated Words (more than twice) in Translated Titles:")
    for word, count in word_counts.items():
        if count > 2:
            print(f"{word}: {count}")

except Exception as main_error:
    print("\nMajor error occurred:", str(main_error))

finally:
    time.sleep(2)
    browser.close()
    print("\nBrowser closed. Scraping completed.")


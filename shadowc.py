from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sys

if len(sys.argv) < 2:
    print("Error: No chapter number provided.")
    sys.exit(1)

chap = sys.argv[1]

comment = sys.argv[2] if len(sys.argv) > 2 else ""

with open('ChromeLocation.txt', 'r') as file:
    fst = file.readline().strip()
    code = file.readline().strip()


PATH = fst
service = Service(PATH)

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")


driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://undergroundnovels.com/")
    search = driver.find_element(By.ID, "account_number")
    search.send_keys(code)
    search.send_keys(Keys.RETURN)

    driver.get("https://undergroundnovels.com/chapter/" + chap)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')

    if comment:
        commenting_id = driver.find_element(By.NAME, 'comment')
        scrolling = driver.find_element(By.CSS_SELECTOR, "button.bg-blue-600.text-white")
        driver.execute_script("arguments[0].scrollIntoView(true);", commenting_id)
        commenting_id.send_keys(comment)
        
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-blue-600.text-white"))
            )
            button.click()
            print("Comment posted successfully!")
        except Exception as e:
            print("Trying some else")
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Post Comment')]"))
            )
            button.click()
            print(e)
        finally:
            driver.get("https://undergroundnovels.com/chapter/" + chap)
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            driver.close()
            
    comments_section = soup.find_all(class_="comments-section")
    for comments in comments_section:
        comments.decompose()

    relevant_text = ''
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        relevant_text += tag.get_text() + '\n'

    with open("Chapter " + chap + ".txt", "w", encoding="utf-8", errors='ignore') as out:
        out.write(relevant_text)

    print(f"Chapter {chap} content saved successfully!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
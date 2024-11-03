from email.message import EmailMessage
import ssl
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sys

# Check if a chapter number was provided
if len(sys.argv) < 2:
    print("Error: No chapter number provided.")
    sys.exit(1)

# Get the chapter number from the command-line argument
chap = sys.argv[1]


with open('PxyList.txt', 'r') as file:
    fst = file.readline().strip()
    code = file.readline().strip()

PATH = fst

service = Service(PATH)

driver = webdriver.Chrome(service=service)

driver.get("https://undergroundnovels.com/")
search = driver.find_element(By.ID, "account_number")
search.send_keys(code)
search.send_keys(Keys.RETURN)
driver.get("https://undergroundnovels.com/chapter/" + chap)
page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')

comments_section = soup.find_all(class_="comments-section")

#comment = input("Comment: ")
if False:
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
        driver.close()

for comments in comments_section:
    comments.decompose()

relevant_text = ''
for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
    relevant_text += tag.get_text() + '\n'

if True:
    with open("Chapter " + chap + ".txt", "w", encoding="utf-8", errors='ignore') as out:
        out.write(relevant_text)


if (False):
    file_path = 'New Proj ideas.txt'
    line1, line2, line3 = None, None, None
    with open(file_path, 'r') as file:
        line1 = file.readline().strip()
        line2 = file.readline().strip()
        line3 = file.readline().strip()

    email_sender = line2
    email_password = line1
    email_receiver = line3

    em_obj = EmailMessage()
    em_obj['From'] = email_sender
    em_obj['To'] = email_receiver
    em_obj['Subject'] = f'SS chapter {chap}'
    em_obj.set_content(relevant_text)

    con = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=con) as smtp:
            smtp.login(email_sender, email_password) 
            smtp.sendmail(email_sender, email_receiver, em_obj.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

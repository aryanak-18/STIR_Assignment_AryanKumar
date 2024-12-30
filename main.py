from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from pymongo import MongoClient
import requests
from requests.auth import HTTPProxyAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

mongoLink = os.getenv("MONGOLINK")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
xpassword = os.getenv("XPASSWORD")

class ProxyConfig:
    def __init__(self):
        self.proxy_host = 'open.proxymesh.com'
        self.proxy_port = '31280'
        self.username = f'{username}'
        self.password = f'{password}'
        
    @property
    def proxy_url(self):
        return f"http://{self.proxy_host}:{self.proxy_port}"
    
    def get_auth(self):
        return HTTPProxyAuth(self.username, self.password)

options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

def get_public_ip(proxy_config):
    try:
        proxies = {
            'http': proxy_config.proxy_url,
            'https': proxy_config.proxy_url
        }
        # response = requests.get(
        #     "https://httpbin.org/ip",
        #     proxies=proxies,
        #     auth=proxy_config.get_auth(),
        #     timeout=45
        # )
        # return response.json()['origin']
        response = requests.get("http://whatismyip.akamai.com/", proxies=proxies, timeout=30)
        return response.text.strip()

    except requests.exceptions.RequestException as e:
        print(f"Error checking IP: {e}")
        return "XXX.XXX.X.XXX"


proxy_config = ProxyConfig()
ip_address = get_public_ip(proxy_config)
print(f"IP Address used for request: {ip_address}")



driver.get("https://x.com/login")
driver.maximize_window()
time.sleep(10)

username = driver.find_element("name", "text")
username.send_keys("aryan14092002")

next_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]")
next_button.click()
time.sleep(3)

password = driver.find_element("name","password")
password.send_keys(f"{xpassword}")

login_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"]')
login_button.click()
time.sleep(6)

trending = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/section/div/div")
children = trending.find_elements(By.XPATH, "./*")

first_trend = children[2].find_element(By.TAG_NAME, 'span')
first_trend_name = first_trend.text

first_five_children = children[3:7]
names=[]
names.append(first_trend_name)
time.sleep(2)

for index, child in enumerate(first_five_children, 1):
    span_el = child.find_elements(By.TAG_NAME, "span")
    name = span_el[1].text
    names.append(name)
print(names)



client = MongoClient(f"{mongoLink}")
db = client["trending_data"]
collection = db["trends"]

date_time = datetime.now()
print(date_time, ip_address)

collection.insert_one({"trends": names, "date_time": date_time, "ip_address": ip_address})
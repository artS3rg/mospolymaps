from selenium import webdriver
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

setik = set()
for i in range(111, 1000):
    driver = webdriver.Chrome()
    driver.get("https://rasp.dmami.ru/")
    sleep(0.5)
    num_group = str(i) #ввод пользователя из тг ботика 222-121 191-331
    WebDriverWait(driver, 0.7).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div > div.header-container > div.header.not-print > div.header-search.search > input"))).send_keys(f"{num_group}")
    sleep(1.5)
    page = driver.page_source
    with open("index.html", "w", encoding="utf-8") as load_html:
        load_html.write(page)
    with open("index.html", encoding="utf-8") as load_html:
        src = load_html.read()

    soup = BeautifulSoup(src, "lxml")
    groups = soup.find_all("div", class_="col-xs-6")
    for j in groups:
        setik.add(j.text)

print(setik)
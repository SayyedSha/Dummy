from selenium import webdriver
from selenium.webdriver.common.by import By
from db_con import get_review_summary
import re
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
# conn = con2()
# cursor = conn.cursor()


driver= webdriver.Edge()
driver.maximize_window()
# driver = webdriver.Chrome()
url = f"https://www.google.com/search?q=werq+labs&sxsrf=AB5stBgPduxXVm-0SzcQ6rAQ4Rd4hMU8Ow%3A1689814822665&source=hp&ei=Joe4ZKG-JufkseMPu8W_mAw&iflsig=AD69kcEAAAAAZLiVNgY4WXKLAn5Tz7c_RzuH65WwbDL1&gs_ssp=eJzj4tVP1zc0LC7IrUrLSck1YLRSNagwTko1TzZMMU81NzFJszRKsTKoSDUzTDYwNkoxTE1LNTFJSvXiLE8tKlTISUwqBgCG7hPr&oq=w&gs_lp=Egdnd3Mtd2l6IgF3KgIIADINEC4YrwEYxwEYigUYJzIEECMYJzIHECMYigUYJzIHEAAYigUYQzIHEAAYigUYQzIHEAAYigUYQzILEAAYgAQYsQMYgwEyCxAAGIAEGLEDGIMBMgsQABiABBixAxiDATINEAAYigUYsQMYgwEYQ0iCCFAAWABwAHgAkAEAmAGcAaABnAGqAQMwLjG4AQPIAQD4AQE&sclient=gws-wiz"
driver.get(url)

block= driver.find_element(By.CSS_SELECTOR,'#rhs > div > div > div.I6TXqe')
print(block)

#Scrapping values of ratings and reviews
values = block.find_element(By.XPATH,'//*[@class="osrp-blk"]/div[1]/div[2]/div[2]').text.replace('\n'," ")
Rating  = values.split(" ")[0] 
total_review  = values.split(" ")[1]
print(f'Rating : '+ Rating + '\n'+f'Total_review : '+total_review)

map_block=block.find_element(By.XPATH,'//*[@class="osrp-blk"]/div[1]/div[1]/div')
map=map_block.find_element(By.XPATH,'//*[@id="lu_map"]').click()
time.sleep(5)#wait for page load

review_block=driver.find_element(By.CSS_SELECTOR,"#QA0Szd > div > div > div.w6VYqd > div:nth-child(2)")
review_div=review_block.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]').click()
time.sleep(5)#wait for page load

R = driver.find_element(By.CSS_SELECTOR,"#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf")
print(R.text)

R1=R.find_element(By.CSS_SELECTOR,"div:nth-child(8)")
print(R1.text)

Rlist=R.find_elements(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[9]')


for i in Rlist:
    try:
        i.find_element(By.XPATH,'//*[@class="MyEned"]/span[2]/button').click()
        review=i.find_elements(By.XPATH,'//*[@class="MyEned"]/span')
        
    except:
        
        name=i.find_elements(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[9]/div/div/div/div[2]/div[2]/div[1]/button/div[1]')
        review=i.find_elements(By.XPATH,'//*[@class="MyEned"]/span')

response = BeautifulSoup(driver.page_source, 'html.parser')
# reviews = response.find_all('div', class_='m6QErb')
re_b = response.find_all('div',class_='jftiEf fontBodyMedium')
print(re_b)
review_set =get_review_summary(re_b)
print(review_set)

def get_review_summary(result_set):
    rev_dict = {
        'Reviewer_name':[],
        'Review Rate': [],
        'Review Time': [],
        'Review Text' : []}
    for result in result_set:
        review_name=result.find('div',class_='d4r55').text
        review_rate = result.find('span', class_='kvMYJc')["aria-label"]
        review_time = result.find('span',class_='rsqaWe').text
        review_text = result.find('span',class_='wiI7pd').text
        rev_dict['Reviewer_name'].append(review_name)
        rev_dict['Review Rate'].append(review_rate)
        rev_dict['Review Time'].append(review_time)
        rev_dict['Review Text'].append(review_text)
    import pandas as pd    
    return(pd.DataFrame(rev_dict))

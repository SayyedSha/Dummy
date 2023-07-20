from selenium import webdriver
from selenium.webdriver.common.by import By
from db_con import get_review_summary,con2
import re
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

conn = con2()
cursor = conn.cursor()

driver = webdriver.Chrome()
driver.maximize_window()
url = f"https://www.google.com/search?q=DR.JOHN+FOX&hl=en&biw=1536&bih=763&sxsrf=AB5stBgPpR_2kcqGVNSxGEpAk5I00Jg7RA%3A1689845712005&ei=z_-4ZI3-POS02roPxuK2-AI&ved=0ahUKEwjNoY7r_ZyAAxVkmlYBHUaxDS8Q4dUDCA8&uact=5&oq=DR.JOHN+FOX&gs_lp=Egxnd3Mtd2l6LXNlcnAiC0RSLkpPSE4gRk9YMgUQABiABDIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHkjXC1CCBFiCBHABeAGQAQCYAcYBoAHGAaoBAzAuMbgBA8gBAPgBAvgBAcICChAAGEcY1gQYsAPiAwQYACBBiAYBkAYD&sclient=gws-wiz-serp"
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
# print(R.text)

R1=R.find_element(By.CSS_SELECTOR,"div:nth-child(8)")


Rlist=R.find_elements(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[9]')


for i in Rlist:
    try:
        i.find_element(By.XPATH,'//*[@class="MyEned"]/span[2]/button').click()
        review=i.find_elements(By.XPATH,'//*[@class="MyEned"]/span')
        
    except:
        
        name=i.find_elements(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[9]/div/div/div/div[2]/div[2]/div[1]/button/div[1]')
        review=i.find_elements(By.XPATH,'//*[@class="MyEned"]/span')

response = BeautifulSoup(driver.page_source, 'html.parser')

reviews = response.find_all('div',class_='jftiEf fontBodyMedium')

review_set =get_review_summary(reviews)
merged_lists = [list(t) for t in zip(review_set['Reviewer_name'], review_set['Review Rate'], review_set['Review Time'], review_set['Review Text'])]


for item in merged_lists:
    cursor.callproc('sp_dummy_insert',tuple(item))
    conn.commit()
    time.sleep(3)

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
        review_text = result.find('span',class_='wiI7pd')
        if review_text:
            r_text=review_text.text
        else:
            r_text=""
        rev_dict['Reviewer_name'].append(review_name)
        rev_dict['Review Rate'].append(review_rate)
        rev_dict['Review Time'].append(review_time)
        rev_dict['Review Text'].append(r_text) 
    return(rev_dict)

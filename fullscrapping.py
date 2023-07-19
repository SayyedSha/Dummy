from selenium import webdriver
from selenium.webdriver.common.by import By
from db_con import con2
import re
import time
import undetected_chromedriver as uc

conn = con2()
cursor = conn.cursor()


driver= webdriver.Chrome()
driver.maximize_window()
# driver = webdriver.Chrome()
url = f"https://www.google.com/search?q=dr.+PHILLIP+ROSENBERG&bih=763&biw=1536&hl=en&sxsrf=AB5stBhBeRuL3fyumHSye2cDIK7OBqxmDw%3A1688713086355&ei=frenZIqeFeyK4-EP2M-g6AY&ved=0ahUKEwiK1Y69gvz_AhVsxTgGHdgnCG0Q4dUDCA8&uact=5&oq=dr.+PHILLIP+ROSENBERG&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIICAAQFhAeEAoyBggAEBYQHjIGCAAQFhAeOgoIABBHENYEELADSgQIQRgAUMUEWMUEYJwLaAFwAHgAgAHeAYgB3gKSAQUwLjEuMZgBAKABAqABAcABAcgBCA&sclient=gws-wiz-serp&bshm=lbse/1"
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

reviews=[]
R = driver.find_element(By.CSS_SELECTOR,"#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf")
# print(R.text)

# R1=R.find_element(By.CSS_SELECTOR,"div:nth-child(8)")
# print(R1.text)

Rlist=R.find_elements(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[9]')


for i in Rlist:
    try:
        i.find_element(By.XPATH,'//*[@class="MyEned"]/span[2]/button').click()
        review=i.find_elements(By.XPATH,'//*[@class="MyEned"]/span')
        
    except:
        
        name=i.find_elements(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[9]/div/div/div/div[2]/div[2]/div[1]/button/div[1]')
        review=i.find_elements(By.XPATH,'//*[@class="MyEned"]/span')
        print("here")
for j in review:
    print(j.text)

for k in name:
    print(k.text)


# Find the match using regex
pattern = r'q=([^&]+)'
match = re.search(pattern, url)
if match:
    searched_value = match.group(1).replace('+',' ')
    print(searched_value)
else:
    print("No search value found in the URL.")

# Define the regex pattern to extract the platform
pattern = r"https?://(?:www\.)?([^/?]+)"

matches = re.findall(pattern, url)

platform = matches[0] if matches else None

print("Platform:", platform)

#finding if client is registered in client_table
# cursor.callproc('SP_client_tale_get_by_name',[searched_value])
# result = list(cursor.stored_results())[0].fetchall()
# cursor.nextset()

# if len(result)==0:
#     cursor.callproc('Sp_client_tale_insert_user',[searched_value])
#     conn.commit()


# #finding is the searching platform registered or not
# cursor.callproc('SP_client_tale_get_by_name',[searched_value])
# result2 = list(cursor.stored_results())[0].fetchall()
# cursor.nextset()
# cl_id=result2[0][0]

# cursor.callproc('sp_scrapping_detail_get_by_client_id',[cl_id])
# cl_result= list(cursor.stored_results())[0].fetchall()
# cursor.nextset()

# if len(cl_result)==0:
#     cursor.callproc('SP_scrapping_detail_insert',[cl_id,platform,url])#inserting scrapping details into table
#     conn.commit()


# #finding Inserting ratings and review in db
# cursor.callproc('sp_scrapping_detail_get_by_client_id',[cl_id])
# cl_result= list(cursor.stored_results())[0].fetchall()
# cursor.nextset()
# org_id=cl_result[0][0]

# cursor.callproc('SP_rating_review_get_by_org_id',[org_id])
# org_res= list(cursor.stored_results())[0].fetchall()
# cursor.nextset()

# if len(org_res)==0:
#     cursor.callproc('SP_rating_review_insert',[org_id,Rating,total_review])
#     conn.commit()
#     print("No old entry found so inserting it as new")
# elif int(org_res[0][0]<int(total_review)):
#     cursor.callproc('SP_rating_review_insert',[org_id,Rating,total_review])
#     conn.commit()
#     print("Total Total Count of Review is Increased")
# else:
#     print("Total Count of Review is same")
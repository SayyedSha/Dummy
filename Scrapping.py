from selenium import webdriver
from selenium.webdriver.common.by import By


#Setting Driver
scrap = webdriver.Edge()
scrap.get("https://www.google.com/search?q=werq+labs&source=hp&ei=EGWqZN6YFMKCoAS_4qy4Cg&iflsig=AD69kcEAAAAAZKpzIIyjzjMgNCvGUH9gWI-o-KkQdplT&gs_ssp=eJzj4tVP1zc0LC7IrUrLSck1YLRSNagwTko1TzZMMU81NzFJszRKsTKoSDUzTDYwNkoxTE1LNTFJSvXiLE8tKlTISUwqBgCG7hPr&oq=Wer&gs_lcp=Cgdnd3Mtd2l6EAMYADINCC4QrwEQxwEQigUQQzIHCAAQigUQQzIHCAAQigUQQzIHCAAQigUQQzIICAAQgAQQsQMyEQguEIAEELEDEIMBEMcBEK8BMgsIABCABBCxAxCDATIFCAAQgAQyCAgAEIAEELEDMgsILhCABBCxAxCDAToLCC4QigUQsQMQgwE6DQgAEIoFELEDEIMBEEM6CwguEIAEEMcBEK8BUABYqgNg6gxoAHAAeACAAZMBiAGtA5IBAzAuM5gBAKABAQ&sclient=gws-wiz")

#sreaching by selector
block= scrap.find_element(By.CSS_SELECTOR,'#rhs > div > div > div.I6TXqe')
print(block)

# rating = block.find_element(By.XPATH,'//*[@class="osrp-blk"]/div[1]/div[2]/div[2]/div/div/span[1]')
# print(rating.text)

#Scrapping values of ratings and reviews
values = block.find_element(By.XPATH,'//*[@class="osrp-blk"]/div[1]/div[2]/div[2]').text.replace('\n'," ")
Rating  = values.split(" ")[0]
total_review  = values.split(" ")[1]
print(f'Rating : '+ Rating + '\n'+f'Total_review : '+total_review)



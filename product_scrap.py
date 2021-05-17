from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.chrome.options import Options
import csv
from bs4 import BeautifulSoup
import requests

## read csv
products = []
skus = []
with open("upwork_online store inventory-Master.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=",")
    for row in readCSV:
        products.append(row[1])
        skus.append(row[0])
    
products = products[1:]
skus = skus[1:]

## automation using selenium
with open("results.csv","w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SKU", "Product Name", "Product Description","External Image URL","Wordpress Media Library URL"])
    
    for j in range(453,len(products)-1):
        try:
            product = products[j]
            opt = Options()
            opt.add_argument("--headless")

            driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),options=opt)
            driver.get("http://www.google.com")

            que=driver.find_element_by_xpath("//input[@name='q']")
            que.send_keys(product + " in amazon")
            que.send_keys(Keys.RETURN)

            g = driver.find_elements_by_class_name("g")
            
            for i in g:
                dp = i.find_element_by_tag_name("a")
                if "/dp/" in dp.get_attribute("href"):
                    dp_url = dp.get_attribute("href")

                    headers = {
                        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                        'Accept': "*/*",
                        'Cache-Control': "no-cache",
                        'Postman-Token': "79e06af2-466b-452b-9a96-52d7c40db592,10995fe3-eae8-42c7-87c4-178a04c03334",
                        'Host': "www.amazon.com",
                        'Accept-Encoding': "gzip, deflate",
                        'Connection': "keep-alive",
            #             'cache-control': "no-cache",
                        'cache-control': 'no-cache',
                        'content-encoding': 'gzip',
                        'content-type': 'text/html'
                        }
                    try:
                        response = requests.get(dp_url,headers=headers)
                        soup = BeautifulSoup(response.content,'html5lib')
                        # print(soup.prettify())
                        desc = soup.find("div",id="productDescription")
                        if not desc:
                            continue
                        i = 0
                        while desc.text[i] == " " or desc.text[i] == "\r" or desc.text[i] == "\t" or desc.text[i] == "\n":
                            i += 1
                        start = i
                        i = len(desc.text)-1
                        while desc.text[i] == " " or desc.text[i] == "\r" or desc.text[i] == "\t" or desc.text[i] == "\n":
                            i -= 1
                        end = i+1
                        description = desc.text[start:end].replace("\t","").replace("\n","")
                        print(product,dp_url)
                        print(description)
                        
                        img = soup.find("img", id="landingImage")
                        external_url = img['data-a-dynamic-image'].split('"')[1]
                        data_list = [["SKU", "Product Name", "Product Description","External Image URL","Wordpress Media Library URL"]]
                        writer.writerow([skus[0], product, description, external_url, "https://websitename.com/wp-content/uploads/sites/2/2020/04/"+product+".jpg"])
                        break
                    except:
                        continue
        except:
            continue        

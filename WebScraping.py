'''import selenium
from selenium import webdriver


print('PROGRAM BEGINS')

#so driver doesnt open in dev mode
Coptions= webdriver.ChromeOptions()

Coptions.add_argument('--log-level=3')
Coptions.add_experimental_option('excludeSwitches', ['enable-logging'])
webd = webdriver.Chrome('chromedriver.exe', options=Coptions)


"""my_element_id = 'something123'
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
your_element = WebDriverWait('chromedriver.exe', options=Coptions,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.presence_of_element_located((By.ID, my_element_id)))"""

webd.get('https://webscraper.io/test-sites/e-commerce/static')
obj=webd.find_element_by_xpath('//*[@id="side-menu"]/li[2]/a')
obj.click()
obj = webd.find_element_by_xpath('//*[@id="side-menu"]/li[2]/ul/li[1]/a')
obj.click()


ListOfLinks=[]

condition=True
while condition:
    ProductsOnPage=webd.find_elements_by_class_name('thumbnail')
    for product in ProductsOnPage:
        h4=product.find_elements_by_tag_name('h4')[-1]
        a=h4.find_element_by_tag_name('a')#tag a
        ListOfLinks.append(a.get_property('href'))
        
    try:
        obj=webd.find_elements_by_class_name('page-link')[-1]#last one > in pagelink
        #print(obj.get_attribute('aria-label'))
        if obj.get_attribute('aria-label')=='Next »':
             obj.click()
        else:
             condition=False
    except:
        condition=False

        
        
       # webd.back()

print(ListOfLinks)'''


from selenium import webdriver #the web driver is what we use to interact with the webpage
from selenium.webdriver.common.keys import Keys # allows keyboard interactioms to be made like enter

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from bs4 import BeautifulSoup
from tabulate import tabulate
from prettytable import PrettyTable
from tqdm import tqdm

path = "chromedriver.exe" # location of chromdriver- needed for web driver

driver = webdriver.Chrome(path)
entry= input('Enter Product Whose price you would like to compare: ')
#entry = 'spiderman ps4'
#SecondHand = True
ch = input('''Allow second hand items? Enter
y for yes
n for no: ''').lower()

if ch == 'y':
    SecondHand = True
else:
    SecondHand = False
entry= entry.lower()
output=[]
#AMAZON

'''   
'''
def check_ad(xpath):
    try:
        ad_button= driver.find_element_by_xpath(xpath)
        ad_button.click()
    finally:
        return None

def check_relevant(output,item_text, price, item_link, url=''):

    
    temp = ''
    for i in price:
        if i.isdigit():
            temp = temp + i
    price= int(temp)


    flag = 1
    for word in entry.split():
        if word not in item_text.lower().split():
            flag = 0
            break
    if flag ==1:
        
        output.append([item_text, price, url + item_link])

def sort_output(output):
    for i in range(len(output)-1):
        for j in range(len(output) - 1 - i):
            if output[j][1] > output[j+1][1]:
                output[j+1], output[j] = output[j], output[j+1]
    for i in range(20):
        if i >= len(output):
            driver.quit()
            break
        print(i+1,')')
        print('NAME:', output[i][0])
        print('PRICE: Rs.', output[i][1])
        print('LINK:', output[i][2])
        
            
        print('\n \n')




     
    
#AMAZON does not work :(
"""
driver.get("https://www.amazon.in/")
search_bar_amazon = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]') #finds search bar
search_bar_amazon.send_keys(entry) # text that is entered in search bar
search_bar_amazon.send_keys(Keys.RETURN) # hits enter i.e gets us to new page
print(driver.current_url)
page = requests.get(driver.current_url)
soup = BeautifulSoup(page.text, 'html.parser')# use to get based on data-component tag
results= soup.find_all('div',{'data-component-type':'s-search-result'})

#for i in range(1,30):
#    results.append(soup.find('div', {'data-index':str(i)}) )
prices = driver.find_elements_by_class_name('a-price-whole')
i=0
#print(results)

for result in results:
    item_text=result.h2.a.text
    item_link = result.h2.a['href']
    
    price= prices[i].text
    check_relevant(output, item_text,price,item_link,'www.amazon.in')
    i += 1
    #print('________________________________________________')
"""
#Flipkart:

driver.get('https://www.flipkart.com/')
xpath_ad = '/html/body/div[2]/div/div/button'
check_ad(xpath_ad)
    

search_bar_flipkart = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input')
search_bar_flipkart.send_keys(entry)
search_bar_flipkart.send_keys(Keys.RETURN)
check_ad(xpath_ad)

page = requests.get(driver.current_url)
soup = BeautifulSoup(page.text, 'html.parser')
results = soup.find_all('a',{'class':'_2cLu-l'})
prices = soup.find_all('div', {'class':'_1vC4OE'})
#print(r.text)
i=0
for r in results:
    item_text = r.text
    item_link =  r['href']
    item_price = prices[i].text
    check_relevant(output, item_text, item_price , item_link, 'www.flipkart.com')

    # item_link)
    i +=1



#snapdeal
driver.get('https://www.snapdeal.com/')
search_bar_snapdeal = driver.find_element_by_xpath('//*[@id="inputValEnter"]')
search_bar_snapdeal.send_keys(entry)
search_bar_snapdeal.send_keys(Keys.RETURN)
page = requests.get(driver.current_url)
soup = BeautifulSoup(page.text, 'html.parser')
results = soup.find_all('p',{'class':'product-title'})
price   = soup.find_all('span',{'class':'lfloat product-price'})
images  = soup.find_all('div',{'class':'product-tuple-image'})
for i in range(len(results)):
    item_text = results[i].text
    item_price = price[i].text
    item_link = images[i].find('a',{'target':'_blank'})['href']
    #print(item_text, item_price, item_link)
    check_relevant(output, item_text, item_price , item_link)

#OLX
if SecondHand:
    driver.get('https://www.olx.in/')
    search_bar_olx = driver.find_element_by_xpath('//*[@id="container"]/header/div/div/div[2]/div/div/div[2]/div/form/fieldset/div/input')
    search_bar_olx.send_keys(entry)
    search_bar_olx.send_keys(Keys.RETURN)
    page = requests.get(driver.current_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    results = soup.find_all('span',{'data-aut-id':'itemTitle'})
    price   = soup.find_all('span',{'data-aut-id':'itemPrice'})
    links=[]
    for box in soup.find_all('li',{'data-aut-id':'itemBox'}):
        links.append(box.find('a')['href'])
    url = 'www.olx.in'    


    print(len(results))
    for i in range(len(results)):
        item_text = results[i].text
        item_price = price[i].text
        item_link  = links[i]
        check_relevant(output,item_text, item_price, item_link, url)

sort_output(output)


'''
for record in output:
    for value in record:
        print(value)
    print('\n \n ')'''
    


#time.sleep(15)
driver.quit()# closes window

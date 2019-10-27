import time
from selenium import webdriver
#import chromedriver_binary
#https://qiita.com/memakura/items/20a02161fa7e18d8a69

#driver = webdriver.Chrome()
driver = webdriver.Chrome(executable_path='.\\chromedriver_win32\\chromedriver.exe')
driver.get('https://www.google.com/')
time.sleep(5)
search_box = driver.find_element_by_name("q")
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)
driver.quit()
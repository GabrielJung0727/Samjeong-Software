import numpy as np
import pandas as pd
from selenium import webdriver as wb
# HTML요소에 접근하기 위한 방법을 제공하는 라이브러리
from selenium.webdriver.common.by import By
# 키보드 값을 제공하는 라이브러리
from selenium.webdriver.common.keys import Keys
#실행 시간을 딜레이주는 라이브러리
import time
# 특정 조건이 충족될 때까지 기다리는데 사용되는 모듈
from selenium.webdriver.support.ui import WebDriverWait as wait
# webdriverWait익 기다리는 조건을 정의하는데 사용되는 모듈
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm as tq # 타카둠 : for 문의 시간을 확인

driver = wb.Chrome()
driver.get('https://www.gmarket.co.kr/n/best')
wait = wait(driver,10)

titles = [] # 상품명을 담아줄 리스트
prices = [] # 가격을 담아줄 리스트
for i in range(1,13) : # li태그의 group 개수가 12개! 그래서 1~12까지 group{} 포매팅 지정
    # CSS 선택자를 활용하여 카테고리 group 요소 가져오기
    item = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,f"#categoryTabG > li.group{i}")))
    # wait : driver 객체를 가짐과 동시에 최대 10초까지 기다려줌!
    # .until() : 대기 조건 지정
    # EC.presence_of_element_located() : 해당 요소가 나타날 때까지!!   
    # driver에게 "#categoryTabG > li.group{i}" CSS 선택자를 가진 요소가 로드될 때까지
    # 기다리라고 지시하고, 해당 요소가 로드되면 가져와!   
    item.click()
    # time.sleep(1) # 화면이 움직이는 시간이므로, 1초 stop!
    # group마다 상품들의 개수가 다를 수 있음!
    # 각각의 길이를 담아줄거임
    time.sleep(0.5)
    length = len(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a.itemname"))))    
    # 각각의 title과 price를 담아 처음 생성해두었던 title과 price를 담자!
    for j in tq(range(length)) : 
        title = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a.itemname")))[j].text
        price = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.s-price > strong > span")))[j].text
        titles.append(title)
        prices.append(price)   
driver.close()

t = pd.Series(titles)
p = pd.Series(prices)
pd.concat([t,p],axis=1)
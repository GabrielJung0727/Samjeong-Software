import time  # 시간 지연을 위해 사용
import re  # 정규표현식 처리용
import argparse  # 명령줄 인자 처리용
import datetime  # 날짜 및 시간 처리용
import pandas as pd  # 데이터프레임 처리용
import matplotlib.pyplot as plt  # 시각화용
import seaborn as sns  # 통계 시각화용
from selenium import webdriver  # 웹 자동화 처리
from selenium.webdriver.common.by import By  # 요소 탐색 방법 정의
from selenium.webdriver.chrome.options import Options  # 크롬 실행 옵션 설정
from selenium.webdriver.support.ui import WebDriverWait  # 요소가 나타날 때까지 대기
from selenium.webdriver.support import expected_conditions as EC  # 특정 조건 대기
import chromedriver_autoinstaller  # 크롬 드라이버 자동 설치
from fake_useragent import UserAgent  # 랜덤 User-Agent 설정

# ------------------------------
# Argparse 설정 (명령줄에서 지역과 페이지 수 입력받기)
# ------------------------------
parser = argparse.ArgumentParser(description="당근마켓 중고 노트북 가격 수집기")
parser.add_argument('--region', type=str, default='신당동', help='검색할 지역명')
parser.add_argument('--max_page', type=int, default=3, help='최대 페이지 수')
args = parser.parse_args()

# ------------------------------
# Selenium 설정 (헤드리스 + 랜덤 User-Agent)
# ------------------------------
chromedriver_autoinstaller.install()  # 드라이버 자동 설치
ua = UserAgent()  # User-Agent 생성
options = Options()
options.add_argument('--headless')  # 창을 띄우지 않고 실행
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(f'user-agent={ua.random}')  # 무작위 user-agent 설정
driver = webdriver.Chrome(options=options)  # 크롬 드라이버 실행

# 지역 파라미터 URL 구성
region_param = args.region.replace(' ', '-') + '-28'
base_url = f'https://www.daangn.com/kr/buy-sell/?in={region_param}&search=노트북'
driver.get(base_url)

# ------------------------------
# 무한 스크롤 구현 및 데이터 수집
# ------------------------------
SCROLL_PAUSE_TIME = 2  # 스크롤 대기 시간 설정

data = []  # 수집된 데이터를 저장할 리스트

for _ in range(args.max_page):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 페이지 끝까지 스크롤
    time.sleep(SCROLL_PAUSE_TIME)

    try:
        # 게시물이 로딩될 때까지 대기
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-gtm="search_article"]'))
        )
    except:
        print("\U0001F6AB 게시물이 로딩되지 않았습니다.")
        continue

    # 게시물 요소 추출
    items = driver.find_elements(By.CSS_SELECTOR, 'a[data-gtm="search_article"]')
    for item in items:
        try:
            # 제목, 가격, 지역, 링크 추출
            title = item.find_element(By.CSS_SELECTOR, 'span.lm809sh').text
            price_text = item.find_element(By.CSS_SELECTOR, 'span.lm809si').text
            region_elem = item.find_element(By.CSS_SELECTOR, 'span.lm809sj').text
            link = 'https://www.daangn.com' + item.get_attribute('href')
            data.append([title, price_text, region_elem, link])  # 리스트에 추가
        except Exception as e:
            continue

# 드라이버 종료
driver.quit()

# ------------------------------
# 데이터 전처리 함수 정의
# ------------------------------
def convert_price(price):
    price = re.sub(r'[^0-9]', '', price)  # 숫자만 추출
    return int(price) if price else None

def convert_date(text):
    now = datetime.datetime.now()
    if '일 전' in text:
        days = int(re.search(r'(\d+)일 전', text).group(1))
        return now - datetime.timedelta(days=days)
    elif '시간 전' in text:
        hours = int(re.search(r'(\d+)시간 전', text).group(1))
        return now - datetime.timedelta(hours=hours)
    else:
        return now

# ------------------------------
# 수집한 데이터를 DataFrame으로 정리
# ------------------------------
records = []
for title, price, date, link in data:
    model_match = re.findall(r'(삼성|LG|그램|레노버|ASUS|NT[0-9]+)', title)  # 모델명 추출
    model = model_match[0] if model_match else '기타'
    records.append({
        'title': title,
        'model': model,
        'price': convert_price(price),
        'date': convert_date(date),
        'url': link
    })

# DataFrame 생성 및 CSV 저장
df = pd.DataFrame(records)
print("레코드 수:", len(records))
if records:
    print("예시 레코드:", records[0])
else:
    print("레코드가 비어 있음")
    exit()

df.dropna(subset=['price'], inplace=True)  # 가격이 없는 행 제거
df.to_csv('daangn_laptops.csv', index=False)  # CSV 저장

# ------------------------------
# 시각화 및 통계 분석
# ------------------------------
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], kde=True, bins=30)  # 가격 히스토그램 + KDE
plt.title('중고 노트북 가격 히스토그램')
plt.xlabel('가격 (원)')
plt.ylabel('빈도')
plt.savefig('price_histogram.png')  # 이미지 저장

plt.figure(figsize=(10, 4))
sns.boxplot(x=df['price'])  # 박스플롯
plt.title('중고 노트북 가격 박스플롯')
plt.savefig('price_boxplot.png')  # 이미지 저장

# 평균 가격 기준 이상/이하 상품 분류
avg_price = df['price'].mean()
threshold_upper = avg_price * 1.2
threshold_lower = avg_price * 0.8

above_avg = df[df['price'] > threshold_upper]  # 평균 초과 상품
below_avg = df[df['price'] < threshold_lower]  # 평균 이하 상품

print("\n평균 가격 이상 상품:")
print(above_avg[['title', 'price', 'url']])

print("\n평균 가격 이하 상품:")
print(below_avg[['title', 'price', 'url']])

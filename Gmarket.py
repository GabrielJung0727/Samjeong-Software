# -*- coding: utf-8 -*-
# Gmarket.py: G마켓 상품 리뷰 크롤링 및 감성 분석

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from collections import Counter

class GmarketReviewCrawler:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def search_product(self, keyword: str):
        url = f"https://browse.gmarket.co.kr/search?keyword={keyword}"
        self.driver.get(url)
        time.sleep(2)

    def get_top_product_links(self, top_n: int = 3) -> list[str]:
        elems = self.driver.find_elements(By.CSS_SELECTOR, 'div.box__component-itemcard a')
        return [e.get_attribute('href') for e in elems[:top_n]]

    def crawl_reviews(self, product_url: str) -> list[dict]:
        self.driver.get(product_url)
        time.sleep(2)
        # 리뷰 탭 클릭
        try:
            tab = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="#itemReview"]')))
            tab.click()
            time.sleep(2)
        except Exception:
            return []
        # iframe으로 전환
        try:
            iframe = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe#ifrReview')))
            self.driver.switch_to.frame(iframe)
            time.sleep(1)
        except Exception:
            return []
        reviews = []
        # 리뷰 블록 수집
        blocks = self.driver.find_elements(By.CSS_SELECTOR, 'div.snb_content div.list > ul > li')
        for b in blocks:
            try:
                rating = b.find_element(By.CSS_SELECTOR, 'span.text__rating').text
                content = b.find_element(By.CSS_SELECTOR, 'p.text__review').text.strip()
                reviews.append({'rating': rating, 'content': content})
            except Exception:
                continue
        return reviews

    def close(self):
        self.driver.quit()


def perform_sentiment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    okt = Okt()
    pos_keywords = ['좋다', '만족', '최고', '추천']
    neg_keywords = ['별로', '나쁘다', '실망', '최악', '불만']

    df['sentiment'] = '중립'
    for idx, row in df.iterrows():
        tokens = okt.morphs(row['content'])
        if any(w in tokens for w in pos_keywords):
            df.at[idx, 'sentiment'] = '긍정'
        elif any(w in tokens for w in neg_keywords):
            df.at[idx, 'sentiment'] = '부정'
    return df


def generate_wordcloud(df: pd.DataFrame, sentiment: str):
    subset = df[df['sentiment'] == sentiment]
    if subset.empty:
        print(f"{sentiment} 리뷰 데이터가 없습니다.")
        return
    text = ' '.join(subset['content'])
    nouns = Okt().nouns(text)
    freq = Counter(nouns)
    wc = WordCloud(
        font_path='C:/Windows/Fonts/NanumGothic.ttf',
        background_color='white',
        width=800,
        height=600
    ).generate_from_frequencies(freq)

    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"{sentiment} 리뷰 워드클라우드")
    plt.show()


if __name__ == '__main__':
    crawler = GmarketReviewCrawler()
    crawler.search_product('무선 이어폰')

    all_reviews = []
    for link in crawler.get_top_product_links():
        reviews = crawler.crawl_reviews(link)
        all_reviews.extend(reviews)
    crawler.close()

    df = pd.DataFrame(all_reviews)
    if df.empty:
        print("리뷰를 크롤링하지 못했습니다. 셀렉터를 확인하세요.")
        exit(1)
    df.dropna(subset=['content'], inplace=True)
    df = perform_sentiment_analysis(df)

    print(df['sentiment'].value_counts())
    generate_wordcloud(df, '긍정')
    generate_wordcloud(df, '부정')

# 과제 3 : 쇼핑몰 리뷰 감성 분석 프로젝트 (Review Sentiment Analysis)

이 프로젝트는 쿠팡 또는 G마켓 등 국내 온라인 쇼핑몰의 상품 리뷰 데이터를 수집하고,  
자연어 처리 기반으로 **긍정/부정 감성 분석**을 수행하는 웹 크롤링 기반 데이터 분석 프로젝트입니다.

## 🔧 사용 기술

- Python 3.9+
- Selenium, BeautifulSoup
- pandas, matplotlib, seaborn
- KoNLPy (한글 형태소 분석)
- Transformers (감성 분류 모델)
- WordCloud (시각화)

## ⚙️ 프로젝트 실행 방법

1. 가상환경 생성  
```bash
python -m venv venv```

2. 가상환경 활성화
```Windows: venv\Scripts\activate```

```macOS/Linux: source venv/bin/activate```

3. 의존성 설치
```pip install -r requirements.txt```

4. Jupyter Notebook 실행
```jupyter notebook```

5. notebooks/01_environment_check.ipynb 열기

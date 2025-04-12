# config.py - 공통 설정 관리

import os

# 경로 관련 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 감성 분류에 사용할 키워드 파일
POSITIVE_KEYWORDS_PATH = os.path.join(DATA_DIR, 'positive_words.txt')
NEGATIVE_KEYWORDS_PATH = os.path.join(DATA_DIR, 'negative_words.txt')

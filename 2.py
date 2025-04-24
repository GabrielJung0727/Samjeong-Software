import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 로딩
df = pd.read_csv("daangn_laptops.csv")

# 가격 분포 시각화 (히스토그램 + KDE)
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], kde=True, bins=30)
plt.title('중고 노트북 가격 분포 (히스토그램 + KDE)')
plt.xlabel('가격 (원)')
plt.ylabel('빈도')
plt.tight_layout()
plt.savefig('2_price_distribution.png')
plt.show()

# 박스플롯으로 이상치 확인
plt.figure(figsize=(10, 4))
sns.boxplot(x=df['price'])
plt.title('중고 노트북 가격 분포 (박스플롯)')
plt.tight_layout()
plt.savefig('2_price_boxplot.png')
plt.show()

# 평균 기준 이상/이하 필터링
avg_price = df['price'].mean()
threshold_upper = avg_price * 1.2
threshold_lower = avg_price * 0.8

above_avg = df[df['price'] > threshold_upper]
below_avg = df[df['price'] < threshold_lower]

print("\n▶ 평균 가격:", round(avg_price, 2))
print("▶ 평균 초과 상품 수:", len(above_avg))
print("▶ 평균 이하 상품 수:", len(below_avg))

# 필터링된 데이터 저장
above_avg.to_csv("above_average_laptops.csv", index=False)
below_avg.to_csv("below_average_laptops.csv", index=False)
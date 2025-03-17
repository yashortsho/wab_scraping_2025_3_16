import requests
from bs4 import BeautifulSoup

# 네이버 뉴스 URL
url = "https://news.naver.com"

# 웹페이지 요청
response = requests.get(url)

# 정상 응답인지 확인
if response.status_code != 200:
    print("페이지 로드 실패!")
    exit()

# HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 뉴스 제목 가져오기
news_titles = soup.find_all("a", class_="news_tit")  # <a> 태그 중 뉴스 제목이 있는 것 찾기

# 출력
for title in news_titles:
    print(title.text)  # 기사 제목 출력

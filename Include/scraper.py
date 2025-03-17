import requests  # 웹페이지 요청을 위한 라이브러리
from bs4 import BeautifulSoup  # HTML을 분석하는 라이브러리

# 1. 웹페이지 요청 (HTML 코드 가져오기)
url = "https://www.oddsportal.com/"  # 크롤링할 웹사이트 주소
response = requests.get(url)  # 해당 웹사이트의 HTML 가져오기

# 2. 응답이 정상인지 확인
if response.status_code == 200:
    print("페이지 로드 성공!")
else:
    print("페이지 로드 실패:", response.status_code)
    exit()  # 프로그램 종료

# 3. HTML 파싱 (분석)
soup = BeautifulSoup(response.text, "html.parser")  # HTML을 파싱(분석)

# 4. 페이지 제목 가져오기
title = soup.title.text  # <title>태그의 텍스트 가져오기
print("페이지 제목:", title)

# 5. 모든 링크 가져오기
links = soup.find_all("a")  # <a> 태그(링크) 모두 찾기
for link in links:
    href = link.get("href")  # 링크 주소 가져오기
    text = link.text.strip()  # 링크의 텍스트 가져오기
    print(f"링크: {href} | 텍스트: {text}")

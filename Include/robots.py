import requests

# 크롤링할 사이트의 robots.txt URL
site = "https://www.oddsportal.com"  # 네이버 예제
robots_url = site + "/robots.txt"

# robots.txt 가져오기
response = requests.get(robots_url)

# 응답 확인
if response.status_code == 200:
    print(f"{site}의 robots.txt 내용:\n")
    print(response.text)  # robots.txt 출력
else:
    print("robots.txt를 가져올 수 없습니다.")

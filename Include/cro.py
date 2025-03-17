from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Chrome WebDriver 자동 다운로드 및 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 웹페이지 열기
driver.get("https://www.google.com")

# 실행 확인 후 브라우저 닫기
print(driver.title)  # 웹페이지 제목 출력
driver.quit()

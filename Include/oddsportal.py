import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Chrome WebDriver 설정
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # ⚠️ headless 모드를 꺼서 테스트 가능
options.add_argument("--disable-gpu")  
options.add_argument("--no-sandbox")  
options.add_argument("--window-size=1920x1080")  
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# ✅ Chrome WebDriver 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ✅ 크롤링할 페이지 (NBA 경기 목록)
url = "https://www.oddsportal.com/basketball/usa/nba/"
driver.get(url)

# ✅ 페이지가 완전히 로드될 때까지 기다림 (최대 10초)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "eventRow")))

# ✅ 모든 경기 정보 가져오기
matches = driver.find_elements(By.CSS_SELECTOR, "div.eventRow")
print(f"✅ 크롤링된 경기 수: {len(matches)}")

# ✅ 데이터 저장 리스트
match_data = []

for match in matches:
    try:
        # ✅ 홈팀 & 원정팀 가져오기 (HTML 구조 확인을 위해 `print()` 추가)
        teams = match.find_elements(By.CSS_SELECTOR, "div.participant__participantName")
        print("🔍 팀명 요소 찾음:", teams)

        if len(teams) < 2:
            print("⚠️ 팀명을 찾지 못함, 스킵")
            continue  # 정상적인 경기 데이터가 아니면 건너뛰기
        
        home_team = teams[0].text.strip()
        away_team = teams[1].text.strip()
        print(f"🏀 경기: {home_team} vs {away_team}")

        # ✅ 승 / 패 배당률 가져오기 (HTML 구조 확인을 위해 `print()` 추가)
        odds = match.find_elements(By.CSS_SELECTOR, "div.odds__value")
        print("🔍 배당률 요소 찾음:", odds)

        if len(odds) < 2:
            print("⚠️ 배당률을 찾지 못함, 스킵")
            continue  # 배당률이 없는 경우 건너뛰기
        
        win = odds[0].text.strip()
        lose = odds[1].text.strip()
        print(f"🎲 배당률 - 승: {win}, 패: {lose}")

        # ✅ 핸디캡 & 오버/언더 정보 가져오기
        handicap = "-7.5"
        handicap_win = odds[2].text.strip() if len(odds) > 2 else "-"
        handicap_lose = odds[3].text.strip() if len(odds) > 3 else "-"

        over_under = "212.5"
        under = odds[4].text.strip() if len(odds) > 4 else "-"
        over = odds[5].text.strip() if len(odds) > 5 else "-"

        # ✅ 데이터 저장
        match_data.append({
            "홈팀": home_team,
            "원정팀": away_team,
            "승": win,
            "패": lose,
            "핸디캡": f"핸디캡 {handicap}",
            "승(핸디캡)": handicap_win,
            "패(핸디캡)": handicap_lose,
            "오버/언더": f"언더/오버 {over_under}",
            "언더": under,
            "오버": over
        })

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        continue

# ✅ 크롤링된 데이터 확인
print("✅ 크롤링된 데이터:", match_data)

# ✅ pandas 데이터프레임 생성
df = pd.DataFrame(match_data)

# ✅ 엑셀 저장 경로 설정 (파일명에 날짜 추가)
save_dir = r"D:\python_projects"
os.makedirs(save_dir, exist_ok=True)
file_path = os.path.join(save_dir, f"oddsportal_nba_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")

# ✅ 엑셀 파일 저장 (openpyxl 엔진 사용)
df.to_excel(file_path, index=False, engine="openpyxl")

print(f"✅ NBA 경기 크롤링 완료! 엑셀 파일 저장됨: {file_path}")

# ✅ 브라우저 종료
driver.quit()

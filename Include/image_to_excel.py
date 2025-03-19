import pytesseract
from PIL import ImageGrab
import pandas as pd

# Tesseract-OCR 실행 경로 설정 (필요할 경우)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 📸 스크린샷 캡처 (화면 전체)
screenshot = ImageGrab.grab()

# 🔍 OCR로 텍스트 추출
text = pytesseract.image_to_string(screenshot, lang="eng")
text = pytesseract.image_to_string(screenshot, lang="kor+eng")


# 📝 텍스트를 줄 단위로 나누기
lines = text.split("\n")

# 📊 DataFrame으로 변환
df = pd.DataFrame({"Extracted Text": lines})

# 💾 엑셀 파일로 저장
df.to_excel("extracted_text.xlsx", index=False)

print("✅ OCR 완료! 'extracted_text.xlsx' 파일로 저장됨.")

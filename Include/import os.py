import pytesseract
import cv2
import numpy as np
import pandas as pd
from PIL import Image

# 📌 Tesseract-OCR 설치 경로 (경로 확인 후 수정)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 📌 OCR 실행할 이미지 파일
image_path = "screenshot.png"  # OCR할 스크린샷 파일 경로

# 📌 이미지 전처리 함수
def preprocess_image(image_path):
    # 이미지 불러오기
    image = cv2.imread(image_path)

    # 그레이스케일 변환 (흑백)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러 적용 (노이즈 제거)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # 이진화 (흑백 대비 강화)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

# 📌 OCR 실행 함수
def extract_text_from_image(image):
    # OCR 실행 (영어 + 한글 지원)
    text = pytesseract.image_to_string(Image.fromarray(image), lang="eng+kor")

    # 특수문자 및 공백 정리
    clean_text = text.strip()
    clean_text = "\n".join([line.strip() for line in clean_text.split("\n") if line.strip()])
    clean_text = clean_text.replace("\n\n", "\n")

    return clean_text

# 📌 엑셀로 저장 함수
def save_text_to_excel(text, output_file="extracted_text.xlsx"):
    # 데이터 프레임 변환
    df = pd.DataFrame({"Extracted Text": text.split("\n")})

    # 엑셀 저장
    df.to_excel(output_file, index=False)

    print(f"✅ OCR 완료! '{output_file}' 파일로 저장됨.")

# 📌 실행 코드
if __name__ == "__main__":
    processed_image = preprocess_image(image_path)  # 이미지 전처리
    extracted_text = extract_text_from_image(processed_image)  # OCR 실행
    save_text_to_excel(extracted_text)  # 엑셀 저장

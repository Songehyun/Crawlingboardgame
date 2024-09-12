import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from beautifulsoup import BeautifulSoup

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # 필요한 경우만 사용

# ChromeDriver 경로 설정 (수동 설치한 경우 경로 지정)
driver_path = r"C:\Users\Administrator\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # 경로를 정확하게 설정해주세요
service = Service(driver_path)

# WebDriver 실행
driver = webdriver.Chrome(service=service, options=chrome_options)

# 파일 저장 경로 설정
output_file_path = r'C:\Users\Administrator\Desktop\ollama\board.md'
if not os.path.exists(os.path.dirname(output_file_path)):
    os.makedirs(os.path.dirname(output_file_path))

# 파일에 데이터를 추가하는 함수
def save_to_file(content):
    with open(output_file_path, 'a', encoding='utf-8') as f:
        f.write(content)
        f.write("\n\n")

# 각 사이트에서 지정된 내용을 크롤링하는 함수
def crawl_site(url, element_identifier, identifier_type="class"):
    driver.get(url)
    try:
        if identifier_type == "class":
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, element_identifier)))
        elif identifier_type == "id":
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, element_identifier)))
        
        # 페이지 소스 가져오기
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        
        # 지정된 요소의 내용을 가져오기
        if identifier_type == "class":
            content = soup.find(class_=element_identifier)
        elif identifier_type == "id":
            content = soup.find(id=element_identifier)

        if content:
            save_to_file(content.get_text())
            print(f"{url} - 데이터가 저장되었습니다.")
        else:
            print(f"{url} - 지정된 요소를 찾을 수 없습니다.")
    
    except Exception as e:
        print(f"{url} - 페이지 로딩 중 오류 발생: {e}")

# 크롤링 대상 사이트
sites = [
    {"url": "https://elflee.tistory.com/256", "identifier": "area_view", "type": "class"},
    {"url": "https://boardlife.co.kr/bbs_detail.php?tb=board_knowhow&bbs_num=634", "identifier": "bbs-review-wrapper", "type": "id"},
    {"url": "https://m.blog.naver.com/ktojja/222189765788", "identifier": "se-main-container", "type": "class"},
    {"url": "https://blog.naver.com/zentnet/222621446904", "identifier": "post-view222621446904", "type": "id"}
]

# 각 사이트 크롤링 실행
for site in sites:
    crawl_site(site["url"], site["identifier"], site["type"])

# 브라우저 종료
driver.quit()

print(f"크롤링 완료. 모든 데이터가 {output_file_path}에 저장되었습니다.")

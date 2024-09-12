import requests
from bs4 import BeautifulSoup

# 크롤링할 웹 페이지 URL
url = 'https://n.news.naver.com/mnews/article/014/0005240429?sid=101'

# requests 라이브러리를 사용하여 웹 페이지의 HTML 내용을 가져옴
response = requests.get(url)

# 웹 페이지의 HTML 내용을 문자열로 변환
html_content = response.text

# Beautiful Soup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')

# 원하는 데이터 추출
# 예: 웹 페이지의 모든 제목(h1 태그) 가져오기
# 예: 웹 페이지의 모든 단락(p 태그) 가져오기
paragraphs = soup.find_all('article')

print('===')

# 추출된 데이터 출력
for paragraph in paragraphs:
    print(paragraph.text)
    
    
    # 최종 결과 저장
with open("./test2.txt", "w", encoding="utf-8") as file:
    file.write( paragraph.text + '\n\n')
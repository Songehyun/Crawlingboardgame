import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

def scrape_board_data(post_number):
    url = f"https://boardlife.co.kr/bbs_detail.php?tb=board_community&bbs_num={post_number}"
    
    try:
        # Selenium을 사용하여 페이지 로드
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 브라우저 창을 띄우지 않고 실행
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(3)  # 페이지가 로드될 시간을 줍니다.

        # 페이지 소스 가져오기
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 게시글 제목
        title_element = soup.find(class_="contents-board-title")
        title = title_element.get_text(strip=True) if title_element else "No title"

        # 게시글 정보
        info_element = soup.find(class_="board-info")
        info = info_element.get_text(strip=True) if info_element else "No info"

        # 게시글 내용 - '개 게임 전체보기' 이후의 텍스트만 추출
        contents_element = soup.find(class_="contents-board-contens")
        if contents_element:
            contents = contents_element.get_text(strip=True)
            if '개 게임 전체보기' in contents:
                contents = contents.split('개 게임 전체보기', 1)[-1].strip()
        else:
            contents = "No contents"

        # 댓글 작성자와 댓글 내용 분리
        comment_list = []
        
        # 댓글 작성자: 'nick info' 클래스를 가진 요소 찾기
        comment_names = soup.find_all('div', class_=["nick", "info"])
        
        # 댓글 내용: 'comment-list-user-text' 클래스를 가진 요소 찾기
        comment_texts = soup.find_all('div', class_="comment-list-user-text")

        print(f"\nPost Number: {post_number}")
        if comment_names and comment_texts:
            print("Comments found:")
            for name, text in zip(comment_names, comment_texts):
                comment_name = name.get_text(strip=True)
                comment_text = text.get_text(strip=True)
                print(f"Comment by: {comment_name}")
                print(f"Content: {comment_text}\n")
                comment_list.append({
                    "commentName": comment_name,
                    "comment": comment_text
                })
        else:
            print("No comments found.")
        
        driver.quit()

        return {
            "post_number": post_number,
            "title": title,
            "info": info,
            "contents": contents,
            "comments": comment_list
        }
    
    except Exception as e:
        print(f"Failed to retrieve post {post_number}: {e}")
        return None

def save_data(scraped_data, start, end):
    filename = f'scraped_board_data_{start}_to_{end}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

def scrape_all_posts(start, end):
    scraped_data = []
    current_start = start
    for post_number in range(start, end - 1, -1):  # 57000부터 1까지 감소
        print(f"Scraping post {post_number}...")
        data = scrape_board_data(post_number)
        if data:
            scraped_data.append(data)

        # 1000개 단위로 데이터 저장
        if post_number % 1000 == 0 or post_number == end:
            save_data(scraped_data, current_start, post_number)
            scraped_data = []  # 저장 후 리스트 초기화
            current_start = post_number - 1  # 새로운 시작점 설정
        
        # 서버 과부하 방지를 위해 잠시 대기
        time.sleep(1)
    
    # 마지막으로 남은 데이터 저장 (end 포인트에서 저장되지 않았다면)
    if scraped_data:
        save_data(scraped_data, current_start, end)

if __name__ == "__main__":
    # 57000번부터 1번까지 크롤링
    start_post = 51999
    end_post = 1

    scrape_all_posts(start_post, end_post)

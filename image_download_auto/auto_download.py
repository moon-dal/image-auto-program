import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import time
import os

def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 3600:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds



artist = input('작가 이름을 입력하세요 : ')
page_start_num = int(input('페이지 시작 번호를 입력하세요 : '))
page_finish_num = int(input('페이지 끝 번호를 입력하세요 : '))
filepath = input('이미지를 저장할 폴더 경로를 입력하세요 : ')

# test
# artist = 'jean-baptiste-greuze'
# page_start_num = 2
# page_finish_num = 5
# filepath = 'C:\\Users\\Admin\\Desktop\\image_data\\Jean-Baptiste Greuze\\Raw Data'


# USB 어쩌구 에러 해결
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_argument("headless")
options.add_experimental_option("prefs", {
"download.default_directory": filepath,
"download.prompt_for_download": False,
"download.directory_upgrade": True,
"safebrowsing.enabled": True
})


for page in range(page_start_num, page_finish_num + 1):
    url = f'https://artvee.com/artist/{artist}/page/{page}/'

    # 이미지 수집 사이트 열기
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.get(url=url)

    # 로딩될 때까지 기다림
    browser.implicitly_wait(time_to_wait=20)

    # 이미지의 총 개수 세기 위해 가져옴
    res = requests.get(browser.current_url)
    h = res.text
    sp = bs(h, 'html.parser')
    img_name = sp.select('.product-element-bottom')

    for i in range(len(img_name)):
        # 다운받을 이미지 클릭
        # photo_items = browser.find_elements(By.CLASS_NAME, 'woodmart-lazy-fade.woodmart-loaded')
        photo_items = browser.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div[{i+1}]/div/div[2]/img')
        browser.execute_script('arguments[0].click();', photo_items)

        browser.refresh()
        time.sleep(1)

        # Max Size로 다운받기 버튼 클릭
        download_btn = browser.find_elements(By.CLASS_NAME, 'prem-link.gr.btn.dis.snax-action.snax-action-add-to-collection.snax-action-add-to-collection-downloads')
        download_btn[1].click()
        # time.sleep(10)

        # 이미지 이름 추출
        response = requests.get(browser.current_url)
        html = response.text
        soup = bs(html, 'html.parser')
        titles = soup.select_one('h1.product_title.entry-title > a').get_text().strip()
        
        # 파일명에 ':'이 들어가면 안되기 때문에 해당 문자가 있으면 삭제
        titles = titles.replace(':', '')

        # 이미지 다운로드가 다 됐을 때만 파일명 변경
        while True:
            if download_wait(filepath) > 0:
                old_filename = max([filepath + '\\' + f for f in os.listdir(filepath) if f.endswith('.jpg')], key=os.path.getctime)
                new_filename = os.path.join(filepath, f'{titles}.jpg')

                print(f'{titles} 다운로드 완료')
                time.sleep(3)

                f_names = os.listdir(filepath)

                try:
                    os.rename(old_filename, new_filename)
                    
                except FileExistsError: # 이미지 이름이 중복될 경우
                    name = []
                    for ff in f_names:
                        name.append(os.path.splitext(ff)[0])
                    
                    same = 0
                    for n in name:
                        if (titles == n[:len(titles)] and 
                        (n[-1] == titles[-1] or n[-2] == '#' or n[-3] == '#')):
                            same += 1
                    
                    new_filename = os.path.join(filepath, f'{titles}#{same}.jpg')
                    os.rename(old_filename, new_filename)                      

                # print(f'{new_filename} 파일명 변경 완료')

                browser.back()
                time.sleep(1)
                break
        
        # idx += 1
    
    print('-----------------------------------------------------------')
    print(f'{page}번 페이지 이미지 다운로드 완료!')
    print('-----------------------------------------------------------')
    browser.close()

print('-----------------------------------------------------------')
print(f'{artist} 작가의 이미지 모두 다운로드 완료!')

# exe 프롬프트 창 안꺼지게 하기
os.system('pause')

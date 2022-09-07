from PIL import Image
import os
from PIL import Image, ImageFile

'''
오류 발생하면 'pip install pillow' 하기
'''

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

raw_path = input('Raw Data 폴더 경로를 입력하세요 : ')
cutting_path = input('Cutting Data 폴더 경로를 입력하세요 : ')
imglist = os.listdir(raw_path)

def cutting(img): #16:9 사이즈로 자르기
    w= img.width
    h = img.height
    if w <= h: #세로가 긴사진 --> 9:16 비율로 자르기
        if w * 16/9 <= h:
            img = img.crop((0, (h - w * 16 / 9) / 2, w, h - (h - w * 16 / 9) / 2))
             #left up right down
        else:
            img = img.crop(((w - h * 9/16) / 2, 0, w -(w - h * 9/16) / 2, h))

    else:
        if h*16/9 <= w : #가로가 긴 사진 --> 16:9로 자르기
            img = img.crop(((w - h * 16 / 9) / 2, 0, w - (w - h * 16 / 9) / 2, h))
        else:
            img = img.crop((0, (h - w * 9/16) / 2, w, h - (h - w * 9/16 ) / 2))
    return img


def chg(i,img,name):
    if img.width <= img.height: #가로 세로 판별
        img = img.resize((2160,3840))
    else:
        img = img.resize((3840,2160))

    img.save(f'{cutting_path}/{name}') # 저장


i = 0
# if not os.path.exists('cutting_data'):
#     os.mkdir("cutting_data")
for file_name in imglist:
    i +=1
    img = Image.open(f'{raw_path}/{file_name}')
    chg(i,cutting(img),file_name)
    print(f'현재 {i}번째 작업을 완료하였습니다.')

print("모든 작업을 완료했습니다.")
os.system('pause')

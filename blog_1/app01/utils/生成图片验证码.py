from PIL import Image,ImageDraw,ImageFont
import random
import string
from io import BytesIO

str_all = string.digits + string.ascii_letters
#声明一个随机颜色
def random_color():
    data = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    return data

def random_code():
    width = 200
    height = 40
    img = Image.new('RGB',(width,height),color=(255,255,255)) #三个参数rgb模式、大小、颜色

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font='./font/Kowulz-Regular.ttf',size=32)

    #书写文字

    valid_code = ''
    for i in range(4):
        random_char = random.choice(str_all)
        draw.text((44 * i + 20,3),random_char,(0,0,0),font=font)
        valid_code += random_char
    print(valid_code)

    #随机生成点
    for i in range(1500):
        x , y = random.randint(0,width),random.randint(0,height)
        draw.point((x,y),random_color())

    #随机划线
    for i in range(30):
        x1,y1 = random.randint(0,200),random.randint(0, 40)
        x2, y2 = random.randint(0, 200), random.randint(0, 40)
        draw.line((x1,y1,x2,y2),fill=random_color())  #2个参数，第一个线起始坐标，第二个颜色

    #创建内存字节句柄
    f = BytesIO()
    #将图谱二进制存入f
    img.save(f,'png') #保存图片,名称和格式
    #读取句柄
    data  = f.getvalue()
    print(data)

if __name__ == "__main__":
    random_code()

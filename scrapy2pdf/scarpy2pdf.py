# -*- coding:UTF-8 -*-
import time
import requests
import pdfkit
import re
from bs4 import BeautifulSoup
import os

# 模版
html_template = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'pdfs\\')
html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'htmls\\')


confg =pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
options = {
                    'page-size': 'Letter',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': "UTF-8",
                    'no-outline': None
               }

def save_pdfs(a):

     for each in a[:1]:#数据太多只取5条
          if each.string != None:
               rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |' #存到本地 剔除特殊符号
               each.string = re.sub(rstr, "_", each.string)
               file_name =file_path + each.string + ".pdf"
               html_name = html_path + each.string + ".html"

               target = each.get('href')
               time.sleep(4) # 设置强制睡眠时间减少IP被禁的可能性
               page = requests.get(url=target)
               soup = BeautifulSoup(page.content, 'html.parser')
               article = soup.select('.rich_media_content')[0]# 选择主体部分下载
               for img in article.find_all('img'):
                              img['src'] = img['data-src'] ##！！！将所有的懒加载改成直接加载
               article = str(article)
               html = html_template.format(content=article)
               html = html.encode('utf-8')

               with open(html_name, 'wb') as f:
                    f.write(html) # 保存html格式
               try: # 保存pdf格式
                    print("html_name:%s" %html_name)
                    print("file_name:%s" %file_name)
                    pdfkit.from_file(r'C:\Users\qiang_zhang\Desktop\zhang\create_pdf\scrapy2pdf\htmls\bb.html',file_name,configuration=confg, options=options) # 转化成pdf格式
               except Exception as e:
                    print(e)




def main():
     target = 'https://mp.weixin.qq.com/s?__biz=MzI0Mjg5ODI1Ng==&mid=2247486022&idx=1&sn=5f7c9aff1e3f1847812ce92304a3affc&chksm=e9740e79de03876fffc5ca39f70c105298acf5d2329d632e69cb997f8a07ba1234f97c91464c&scene=21#wechat_redirect'
     req = requests.get(url=target)
     html = req.text
     div_bf = BeautifulSoup(html,"html.parser")
     div = div_bf.find_all('div', class_='rich_media_content')
     a_bf = BeautifulSoup(str(div[0]),"html.parser")
     a = a_bf.find_all('a')# 获得主页面的所有链接标签

     save_pdfs(a)


if __name__ == "__main__":
     main()



#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import os
import smtplib
from email.mime.text import MIMEText

# 替换成你想抓取的网址
url = "https://m.touker.com/adviser/product/viewpointDetail?articleId=83064&tgId=1770&shareId=353562935&shareUuid=ddd2FZkAz44paYwCT26Ad6ry3rpyhBhF"

# 发送 GET 请求
response = requests.get(url)

# 解析网页内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到 class 为 desc 的 <p> 标签
desc_tag = soup.find('p', class_='desc')

if desc_tag:
    # 提取文本
    text = desc_tag.get_text(strip=True)
    # 使用正则提取日期格式（如 04-10）
    match = re.search(r'\d{2}-\d{2}', text)
    if match:
        date_str = match.group()
        # 存储日期的文件路径
        date_file = 'last_date.txt'
        # 检查文件是否存在
        if os.path.exists(date_file):
            with open(date_file, 'r') as f:
                last_date = f.read().strip()
            # 对比日期
            if date_str != last_date:
                # 发送邮件通知
                sender_email = os.getenv('SENDER_EMAIL', "hxg38735@gmail.com")
                receiver_email = os.getenv(
                    'RECEIVER_EMAIL', "460646359@qq.com")
                password = os.getenv('EMAIL_PASSWORD')  # 从环境变量读取密码

                if not password:
                    print('password error')
                else:
                    msg = MIMEText(f"网格更新啦！")
                    msg['Subject'] = "网格有更新！"
                    msg['From'] = sender_email
                    msg['To'] = receiver_email

                    # 连接到 SMTP 服务器并发送邮件
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login(sender_email, password)
                    server.sendmail(
                        sender_email, receiver_email, msg.as_string())
                    server.quit()
                    print("邮件已发送")
            else:
                print("日期未更新")

        # 更新本地文件
        with open(date_file, 'w') as f:
            f.write(date_str)
        print("提取的日期是:", date_str)
    else:
        print("未找到日期格式")
else:
    print("未找到 <p class='desc'> 标签")

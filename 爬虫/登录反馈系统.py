import requests
from requests import ReadTimeout
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mail(massage):
    # 设置发送者和接收者的电子邮件地址
    sender_email = "1601235906@qq.com"
    receiver_email = "409806502@qq.com"
    # 创建 MIME 文档
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "反馈系统异常通知"
    # 添加邮件正文
    body = massage
    message.attach(MIMEText(body, "plain"))
    # 配置SMTP服务器信息
    smtp_server = "smtp.qq.com"
    smtp_port = 587  # qq的SMTP端口号为587
    # 输入你的授权码
    password = "uknbcddbcjzxgfed"
    # 登录到SMTP服务器
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # 开启安全传输模式
        server.login(sender_email, password)  # 使用授权码登录
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("已发送一封邮件")
    time.sleep(visit_interval)


def visit_website(visit_interval):
    while True:
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Host': '118.24.57.135:20080',
                   'Proxy-Connection': 'keep-alive',
                   'Referer': 'http://118.24.57.135:20080/mfs/login',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}

        t1 = time.time()
        session = requests.Session()
        url = 'http://118.24.57.135:20080/mfs/login'
        # url = 'http://118.24.57.135:20080/mfs_test/login'
        data = {"name": "18398261605", "pwd": "lps123456", "smsCode": "", "unitCode": "", "type": 0}
        try:
            response = session.post(url, headers=headers, json=data, timeout=10)
        except ReadTimeout as e:
            print('登录页访问超时。')
            mail(f'访问超时。\n错误信息：{e}')
            continue
        response.encoding = response.apparent_encoding
        status_code = response.status_code
        if status_code != 200:
            print(f'网址：{url}\nHTTP状态：{status_code}')
            mail(f'网址：{url}\nHTTP状态：{status_code}')
            continue

        cookies = response.cookies
        temp = cookies.items()[0]
        cookie = {'Cookie': f'{"=".join(temp)}'}
        headers.update(cookie)
        url = 'http://118.24.57.135:20080/mfs/auth'
        try:
            response = session.get(url, headers=headers, timeout=10)
        except ReadTimeout as e:
            print('认证页访问超时。')
            mail(f'访问超时。\n错误信息：{e}')
            continue
        response.encoding = response.apparent_encoding
        status_code = response.status_code
        if status_code != 200:
            print(f'网址：{url}\nHTTP状态：{status_code}')
            mail(f'网址：{url}\nHTTP状态：{status_code}')
            continue
        msg = response.text
        if msg.find('权限认证成功') == -1:
            print('登录失败')
            mail('登录失败')
            continue

        t2 = time.time()
        t3 = (t2 - t1) / 60
        if t3 > 30:
            print('权限认证超时')
            mail('权限认证超时')
        print('访问成功')
        time.sleep(visit_interval)


visit_interval = 30  # 每隔30秒访问一次
visit_website(visit_interval)

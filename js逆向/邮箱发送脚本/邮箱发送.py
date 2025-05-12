# """
# 5.16 根据多个key向不同的邮箱发送邮件
#
# """
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

#
#
# # 连接邮箱服务器
email_connection = smtplib.SMTP_SSL('smtp.qq.com', 465)

# 登录邮箱
email_connection.login('2480419172@qq.com', 'qikvfuibvxzpebfe')

# 准备数据
# 邮箱对象
email_send = MIMEMultipart()

# 设置邮件主题
center_obj = Header('我是小廉娃哈哈', 'utf-8').encode()
email_send['Subject'] = center_obj

# 设置邮件发送者
email_send['From'] = '2480419172@qq.com'

# 设置邮件接受者
email_send['To'] = '2480419172@qq.com'

# 添加文字内容
text_obj = MIMEText('你好，希望你能回复一下', 'plain', 'utf-8')
email_send.attach(text_obj)

# 发送邮件
email_connection.sendmail('2480419172@qq.com', '2480419172@qq.com', email_send.as_string())
# 退出邮件
email_connection.quit()
#
#
#
#
#
#

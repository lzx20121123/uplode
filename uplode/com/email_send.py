import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(subject,content):  
    # 第三方 SMTP 服务
    mail_host="smtp.qq.com" #设置服务器"smtp.qq.com", 465
    mail_user="李忠学"    #用户名
    mail_pass="ymvpgxatptntbfjg"          
    sender = '794140113@qq.com' #发件人
    receivers = 'lizhongxue@v-secure.cn','794140113@qq.com' # 接收邮件，可设置为你的QQ邮箱或者其他邮箱      
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] =  str(receivers)    
    #subject = '接口测试结果'
    message['Subject'] =  subject                                                      #Header(subject, 'utf-8')    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.close()
        print ("邮件发送成功")
    except smtplib.SMTPException as e:           
        print (e)
        print ("Error: 无法发送邮件")

if __name__ == "__main__":
    send_email('测试结果','2019-06-24-15-03: LinuxNormalbin的x64进程版包内网路径:ftp://192.168.1.6/public/Linux_Packets/release/common/bin/jingyunsd_4.0.0.3-28_c1.2210.2.1111_amd64.bin\nMD5:aacf676053f84cece7562329347e0422\n 2019-06-24-15-03: LinuxNormalbin的x64进程版包外网路径:ftp://120.133.1.35/1.Product/JY-Network Antivirus System/ClientLinux/4.0/bin/jingyunsd_4.0.0.3-28_c1.2210.2.1111_amd64.bin')
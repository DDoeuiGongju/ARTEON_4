import smtplib
from email.message import EmailMessage
import imghdr
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def emailSend(from_email, to_email, file_path):
    # SMTP_SERVER = "smtp.gmail.com"
    # SMTP_PORT = 465
    #
    # message = EmailMessage()
    # message.set_content("안녕하세요! 시연에 참여해주셔서 감사합니다. 사용자님의 이미지 보내드립니다.")
    #
    # message["Subject"] = "아르떼온 시연 이미지"
    # message["From"] = from_email
    # message["To"] = to_email
    #
    # with open(file_path, "rb") as image:
    #     image_file = image.read()
    # image_type = imghdr.what('codelion',image_file)
    # message.add_attachment(image_file,maintype='image',subtype=image_type)
    #
    # smtp = smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT)
    # smtp.login("soeui291@gmail.com","Rlarhdml2.")
    # smtp.send_message(message)
    # smtp.quit()
    send_Mail = str(input(from_email))
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login("soeui291@from_email.com","Rlarhdml2.")  # 보낼 이메일의 이메일,비번

    msg = MIMEBase('multipart', 'mixed')
    cont = MIMEText('제목', 'plain', 'utf-8')
    cont['Subject'] = 'Image'
    cont['From'] = from_email  # 보낼 사람의 이메일
    cont['To'] = to_email
    msg.attach(cont)
    path = file_path  # 보낼 이미지의 경로
    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(path, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename="%s"' % os.path.basename(path))
    msg.attach(part)
    smtp.sendmail(from_email, to_email, msg.as_string())  # 보낼 사람의 이메일
    smtp.quit()
from_email = 'soeui291@gmail.com'
to_email = 'soeui291@gmail.com'
file_path = 'lll.png'
emailSend(from_email, to_email, file_path)
#https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4PXuUjGpnUGV-rmflbSh535JLdmbaaChzrZ1FhA80fDz_Cb5mHyWO7TS-lMsMo6rrXjgCxdgTHbG5CgkipawbC0s0pZWw
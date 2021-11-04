import smtplib
from email.message import EmailMessage
import imghdr
import os

from PyQt5.QtCore import QThread


class emailTread(QThread):
    def __init__(self, send_email=None, file_path=None):
        super().__init__()
        self.send_email = send_email
        self.file_path = file_path
        print(11)

    def run(self):
        print(22)
        print(self.send_email, self.file_path)

        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 465

        message = EmailMessage()
        message.set_content("안녕하세요! 시연에 참여해주셔서 감사합니다. 이미지 보내드립니다.")

        message["Subject"] = "아르떼온 시연 이미지"
        message["From"] = "soeui291@gmail.com"
        message["To"] = self.send_email

        with open(self.file_path, "rb") as image:
            image_file = image.read()
        image_type = imghdr.what('codelion',image_file)
        message.add_attachment(image_file,maintype='image',subtype=image_type)

        smtp = smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT)
        smtp.login("soeui291@gmail.com","Rlarhdml2.")
        smtp.send_message(message)

        print('file send')
        os.remove(self.file_path)
        smtp.quit()

#https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4PXuUjGpnUGV-rmflbSh535JLdmbaaChzrZ1FhA80fDz_Cb5mHyWO7TS-lMsMo6rrXjgCxdgTHbG5CgkipawbC0s0pZWw
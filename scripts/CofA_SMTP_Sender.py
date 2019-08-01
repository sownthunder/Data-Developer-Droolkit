"""
Created on July 31, 2019

3rd and **final** version of
"CofA_AUTO_EMAIL.exe", just
this time without ANY GUI

"""


# IMPORT THE GOODS
import os, sys, time
from time import sleep
from pathlib import Path
import email, smtplib, ssl
import os.path as op
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def send_mail(send_from, send_to, subject, message, files=[],
             server="cos.smtp.agilent.com", port=587, use_tls=True): #{
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg["Bcc"] = send_from  # Recommended for mass emails

    msg.attach(MIMEText(message))

    for path in files: #{
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file: #{
            part.set_payload(file.read())
        #}
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)
    #}

    smtp = smtplib.SMTP(server, port)
    if use_tls: #{
        smtp.starttls()
    #}
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
#}

if __name__ == "__main__": #{
    # ATTEMPT THE FOLLOWING...
    try: #{
        print("RUNNING >>> " + str(sys.argv[0]))
        new_name = str(sys.atgv[1])
        date_str = str(sys.argv[2])
        file_list = [sys.argv[3]]  # ['C:/data/part ICP-079 CofA Lot# 0006479330.pdf']
        send_mail(send_from="derek.bates@non.agilent.com",
                  send_to="agilent_cofa@agilent.com",
                  subject=new_name,
                  message=date_str,
                  files=file_list)
    #}
    except: #{
        print("error")
    #}
    else: #{
        print("FIN...")
    #}
#}
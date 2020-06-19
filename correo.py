def mail(usu):
    import smtplib, os
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    os.system('fswebcam /home/pi/proyecto/Capt/image.jpg')

    fromaddr = "Recognition.RaPi@gmail.com"
    toaddr = "Recognition.RaPi@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Reconocimiento"
    body = ('Usuario %a reconocido'%usu)
    msg.attach(MIMEText(body, 'plain'))
    filename = "/home/pi/proyecto/Capt/image.jpg"
    attachment = open("/home/pi/proyecto/Capt/image.jpg", "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Python3.OPAC")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

    server.quit()

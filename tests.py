import smtplib

try:
    server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
    server.starttls()
    server.login("imadahmad97@yahoo.ca", "Ithegreat97@")
    server.sendmail(
        "imadahmad97@yahoo.ca", "imad.ahmad3245@gmail.com", "This is a test email."
    )
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print("Failed to send email:", e)

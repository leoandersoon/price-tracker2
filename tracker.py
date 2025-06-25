"""
Hepsiburada Price Tracker
-------------------------
This script checks the current price of a product on Hepsiburada.com
and sends an email alert if the product is successfully found.

Requirements:
- selenium
- geckodriver (i used it for Firefox)
- Gmail app password

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText


# ---------- CONFIGURATION ----------
FROM_EMAIL = "your_email@gmail.com"         # Your Gmail address
TO_EMAIL = "receiver_email@gmail.com"       # Where to send the alert
EMAIL_PASSWORD = "your_app_password"        # Gmail App Password
# -----------------------------------

def send_email(subject, body, to_email):
    """
    Sends an email using Gmail SMTP.
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(FROM_EMAIL, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)


def track_price(link):
    """
    Fetches the product title and price from Hepsiburada and sends an email.
    """
    driver = webdriver.Firefox()

    try:
        driver.get(link)
        wait = WebDriverWait(driver, 10)

        # Wait and extract product title
        title = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "xeL9CQ3JILmYoQPCgDcl"))
        ).text

        # Wait and extract product price
        price = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "z7kokklsVwh0K5zFWjIO"))
        ).text

        print("Product:", title)
        print("Price:", price)

        # Send email alert
        send_email(
            subject="Price Alert from Hepsiburada!",
            body=f"Product: {title}\nCurrent Price: {price}\nLink: {link}",
            to_email=TO_EMAIL
        )

    except Exception as e:
        print("Error while tracking:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    print("Hepsiburada Price Tracker")
    product_link = input("Please enter the product URL: ")
    track_price(product_link)

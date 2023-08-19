from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from getpass import getpass
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class InternetSpeedTwitterBot:
    twitter_email = os.getenv("TWTTER_E")
    twitter_password = os.getenv("TWTTER_P")
    twitter_username = os.getenv("TWTTER_USERNAME")

    def __init__(self):
        chrome_driver_path = ChromeDriverManager().install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        service = ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
    
    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"))
            ).click()
        except:
            pass
        self.driver.find_element(By.CSS_SELECTOR, "div.start-button > a[role='button']").click()
        # Wait till Internet Speed Test is over and the result is available
        while True:
            current_url = self.driver.current_url
            if "result" in current_url:
                break
        while True:
            # try-except vlock in case these is a pop up menu ==> reload the current page
            try:
                self.download_speed = self.driver.find_element(By.CSS_SELECTOR, "div[title='Receiving Time'] span.result-data-value").text
                self.upload_speed = self.driver.find_element(By.CSS_SELECTOR, "div[title='Sending Time'] span.result-data-value").text
            except:
                self.driver.get(current_url)
            else:
                break

    def tweet_at_provider(self, dowload_speed, upload_speed):
        self.driver.get("https://twitter.com/")
        wait = WebDriverWait(self.driver, 5)
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='login'"))
        ).click()
        wait.until(
            EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
        )[0].send_keys(InternetSpeedTwitterBot.twitter_email + Keys.ENTER)

        while True:
            try:
                # Look for a password input
                password_form = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
                )
            except:
                # Handle the username verification
                username_confirmation = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='text']"))
                )
                username_confirmation.send_keys(InternetSpeedTwitterBot.twitter_username + Keys.ENTER)
            else:
                password_form.send_keys(InternetSpeedTwitterBot.twitter_password + Keys.ENTER)
                break
        
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".DraftEditor-root [role='textbox']"))
        ).send_keys(f"Hey!\n\nMy Internet speed is:\nDownload - {dowload_speed}\nUpload - {upload_speed}\n\nIs it any good? Share yours!")

        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetButtonInline']"))
        ).click()

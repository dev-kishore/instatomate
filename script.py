from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Function to log in to Instagram
def login(driver, username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)

    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(10)
    
def logout(driver, username):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(5)
    more_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div[3]/span/div/a')
    more_button.click()
    time.sleep(2)
    logout_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[6]/div[1]')
    logout_button.click()
    time.sleep(5)

def get_followers(driver, username):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(5)
    followers_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a')
    followers_button.click()
    time.sleep(5)
    followers = set()
    scroll_box = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')

    last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(3)

        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
        if new_height == last_height:
            break
        last_height = new_height

    followers_elements = scroll_box.find_elements(By.XPATH, '//span[@class="_ap3a _aaco _aacw _aacx _aad7 _aade" and @dir="auto"]')
    for element in followers_elements:
        followers.add(element.text)

    return followers

def unfollow(driver, username, followers):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(5)
    following_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[3]/div/a')
    following_button.click()
    time.sleep(5)
    scroll_box = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]')

    last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)

    start_time = time.time()
    duration = 60

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(3)

        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
        if time.time() - start_time > duration or new_height == last_height:
            break
        last_height = new_height

    driver.execute_script("arguments[0].scrollTop = 0", scroll_box)
    time.sleep(5)
    following_count = len(scroll_box.find_elements(By.XPATH, '//span[@class="_ap3a _aaco _aacw _aacx _aad7 _aade" and @dir="auto"]'))
    print("Following count: ", following_count)
    for i in range(following_count):
        username_element = driver.find_element(By.XPATH, f"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[{i + 1}]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span")
        if username_element.text not in followers:
            acc_following_button = driver.find_element(By.XPATH, f"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[{i + 1}]/div/div/div/div[3]/div/button/div/div")
            acc_following_button.click()
            time.sleep(2)
            unfollow_button = driver.find_element(By.XPATH, '//button[contains(@class, "_a9--") and contains(@class, "_ap36") and contains(@class, "_a9-") and @tabindex="0" and text()="Unfollow"]')
            unfollow_button.click()
            time.sleep(6)


# Main function
def main():
    #Create .env file in same directory and provide values for USERNAME and PASSWORD
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    
    driver = webdriver.Chrome()
    try:
        login(driver, username, password)
        followers = get_followers(driver, username)
        unfollow(driver, username, followers)
    finally:
        logout(driver, username)
        driver.quit()

if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
from extras import *
from os import listdir
from time import sleep
from datetime import datetime
import threading
import multiprocessing

CONFIG = json.load(open("config.json", "r"))
playBtn = '//*[@id="screen-main"]/section[1]/div[2]/div/div[1]/div/p'


def main(token, name, *args, **kwargs):

    chrome_options = webdriver.ChromeOptions()  # create a new Chrome session
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    )
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-seccomp-filter-sandbox")

    extension_paths = [
        f"./extensions/{extension}" for extension in listdir("./extensions")
    ]  # get all the extension paths

    chrome_options.add_experimental_option(
        "useAutomationExtension", False
    )  # disable automation extension
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )  # disable automation

    # add all the extensions to the chrome options
    install_extension(chrome_options, extension_paths)

    driver = webdriver.Chrome(
        # CONFIG["chromedriver_path"]
        options=chrome_options
    )

    ACTION = ActionChains(driver)

    driver.get(f"https://littlebigsnake.com/?login_token={token}")  # open the website

    delayer(3, name=f"{name}: [+] opening window")

    print(close_external_window(driver))
    print("current page: " + driver.title)

    delayer(2, name=f"{name}: [+] setting up local storage cookies")
    driver.execute_script(f'localStorage.setItem("token", "{token}")')
    driver.execute_script(
        f'localStorage.setItem("{kwargs["local_storage_key"]}", "{kwargs["local_storage_value"]}")'
    )

    # counters friendship error
    driver.execute_script(
        f'localStorage.setItem("firstFriendGameDialogCooldown", "{datetime.now().timestamp()}")'
    )

    # counters daily reward error
    driver.execute_script(
        f'localStorage.setItem("LastNewsShowTime16", "{datetime.now().timestamp()}")'
    )

    delayer(2, name=f"{name}: [+] refreshing page")
    driver.refresh()  # refresh page
    print("refreshed the page")


    WebDriverWait(driver, 240).until(
        lambda driver: driver.find_element(By.CLASS_NAME, "current-screen-client")
    )
    
    delayer(4, name=f"{name}: [+] waiting for game to load")
    print("game loaded")

    for error in kwargs["errors_list"]:
        ACTION.reset_actions()
        print("closing: " + error["name"])
        ACTION.move_by_offset(error["x"], error["y"])
        sleep(0.3)
        ACTION.click().perform()
        sleep(2)
        print("closed: " + error["name"])

    delayer(2, name=f"{name}: [+] finished closing [extra] windows")

    leaderBoardPos = (1800, 250)  # leaderboard position 8th place
    isFirst = True  # is this the first time we are clicking the leaderboard?
    while True:
        ACTION.reset_actions()
        ACTION.move_by_offset(leaderBoardPos[0], leaderBoardPos[1])
        sleep(0.3)
        ACTION.click().perform()
        if isFirst:
            sleep(3)
            isFirst = False
        else:
            sleep(2)

        ACTION.reset_actions()
        image_name = f"screenshots/{name}.png"
        driver.save_screenshot(image_name)
        cropNScale(image_name, 3)

        delayer(30, name=f"{name}: [+] clicked leaderboard")


if __name__ == "__main__":
    errors_list = [{"name": "observe", "x": 1320, "y": 630}]
    bots_process = []  # list of bots processes

    account = {
            "token": "TEIhnCJBX7vUsjL72ca8ce2",
            "server": "na_Washington",
            "name": "Washington"
        }
        

    for account in CONFIG["accounts"]:
        bots_process.append(
            multiprocessing.Process(
                target=main,
                args=(account["token"], account["name"]),
                kwargs={
                    "local_storage_key": "server",
                    "local_storage_value": account["server"],
                    "errors_list": errors_list,
                },
            )
        )

    for process in bots_process:
        process.start()
        if len(bots_process) > 1:
            delayer(60, name=f"{process.name}: [+] started process")
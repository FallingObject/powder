from selenium.webdriver import ChromeOptions
from PIL import Image, ImageDraw, ImageFont
import json
from time import sleep


def close_external_window(
    driver, window_name: str = "Little Big Snake - Official Website"
):
    if len(driver.window_handles) > 1:
        for i in range(len(driver.window_handles)):
            try:
                child = driver.window_handles[i]
            except IndexError as e:
                child = driver.window_handles[i - 1]
                print(e)
                # return "fail"
            except Exception as e:
                # print(e)
                return "fail"

            driver.switch_to.window(child)
            if driver.title != window_name:
                print(driver.title)
                driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return "success > 1"
    else:
        driver.switch_to.window(driver.window_handles[0])
        return "success < 1"


def install_extension(chrome_options: ChromeOptions, extension_paths: list):
    for extension in extension_paths:
        try:
            chrome_options.add_extension(extension)
            print(f"extension ` {extension} ` installed")
        except Exception as e:
            print("Failed...\nretrying...")
            try:
                chrome_options.add_extension(extension)
                print(f"extension ` {extension} ` installed")
            except Exception as e:
                return f"Failed to install ` {extension} `"


def delayer(seconds: int, i=1, name="Bob"):
    while seconds > 0:
        sleep(i)
        seconds -= 1
        print(f"{seconds} seconds remaining")
    print(f"{name} is complete")


def cropNScale(_image, scale, config=json.load(open("config.json", "r"))):
    image = Image.open(_image)
    config = config["widget_cast"]
    width = image.size[0]
    image = image.crop(
        (
            width - config["width"],
            config["top"],
            width,
            config["top"] + config["height"],
        )
    )
    width, height = image.size
    image = image.resize((int(width) * scale, int(height * scale)), Image.ANTIALIAS)
    image.save(_image)

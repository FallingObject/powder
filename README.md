# powder ![icon](https://raw.githubusercontent.com/FallingObject/powder/master/logo.png)
A bot that watches for new "Lbs Game Servers" posts and sends a message to a Discord chat.



# installation 📥

## Required
> [ChromeDriver](https://chromedriver.chromium.org/downloads)🚗📚

```
$ pip install selenium

$ pip install fastapi

$ pip install uvicorn
```

## extension 📦
> [AdBlocker](https://chrome.google.com/webstore/detail/adblock-plus-free-ad-bloc/cfhdojbkjhnklbpkdaibdccddilifddb)🚫 get crx file and put in the extensions folder [crxExtractor](https://standaloneinstaller.com/online-tools/crx-downloader)🔥

# Documentations 📚

> [Selenium](https://selenium-python.readthedocs.io/installation.html)

> [FastAPI](https://fastapi.tiangolo.com)

> [Uvicorn](https://www.uvicorn.org/)


# external config
> create <mark>config.json</mark> file in the root directory of the project with the following content:
```
{
    "accounts": [
        {
            "token": "your own token",
            "server": "na_Washington",
            "name": "Washington blob"
        },
        {
            "token": "your own token",
            "server": "any other server",
            "name": "any name"
        }
    ],
    "widget_cast": {
        "top": 30,
        "left": 0,
        "width": 212,
        "height": 145
    },
    "server": {
        "host": "localhost",
        "port": 8091
    }

}
```


# run 🏃

### start the bot 🚀
    ```
    $ python3 main.py 
    ```
recommend to run at 4 accounts max 💪

### start the server 🚀

    ```
    $ python3 server.py
    ```
import time
import shutil
import os
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from selenium import webdriver
import chrome_version
import json
import urllib.request


chrmdriver_path = "C:\\Programy\\chromedriver.exe"


def prepare_fraze(fraze):
    return fraze.replace(" ", "+")


def get_add_date(title):
    try:
        splitted_title = title.split(" ")
        temu_idx = splitted_title.index("temu")
        return " ".join([splitted_title[temu_idx-2],splitted_title[temu_idx-1],splitted_title[temu_idx]])
    except:
        return None


def get_raw_title(title):
    try:
        return title.split(" Autor")[0]
    except:
        pass

def wait_for_file(path, file):
    path = path.strip("/")
    while True:
        if os.path.exists(f"{path}/{file}"):
            break
        else:
            time.sleep(2)
            continue


def remove_file(path):
    try:
        os.remove(path)
    except:
        pass


def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
    except:
        pass


def download_chromedriver():
    response = urllib.request.urlopen('https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json')
    data = json.loads(response.read())
    last_version = pd.DataFrame(data).iloc[0].channels['downloads']['chromedriver'][-1]
    chromedriver_url = last_version['url']
    user_dwnld_path = f"C:/Users/{os.getlogin()}/Downloads/"

    current_browser_version = int(chrome_version.get_chrome_version().split('.')[0])
    newest_stable = int(chromedriver_url.split('/')[4].split('.')[0])

    if current_browser_version < newest_stable:
        chromedriver_url = f'https://storage.googleapis.com/chrome-for-testing-public/{chrome_version.get_chrome_version()}/win64/chromedriver-win64.zip'

    remove_file(f"{user_dwnld_path}chromedriver-win64.zip")
    try:
        shutil.rmtree(f"{user_dwnld_path}chromedriver-win64")
    except:
        pass
    remove_file(r"C:\Programy\chromedriver.exe")

    urllib.request.urlretrieve(chromedriver_url, f"{user_dwnld_path}chromedriver-win64.zip")
    wait_for_file(user_dwnld_path,"chromedriver-win64.zip")

    shutil.unpack_archive(f"{user_dwnld_path}chromedriver-win64.zip",user_dwnld_path[:-1],"zip")
    wait_for_file(user_dwnld_path,"chromedriver-win64")

    if os.path.exists(r"C:\Programy") is False:
        os.mkdir(r"C:\Programy")
    time.sleep(1)

    copy_file(f"{user_dwnld_path}chromedriver-win64/chromedriver.exe", r"C:\Programy\chromedriver.exe")
    wait_for_file(r"C:\Programy","chromedriver.exe")

    remove_file(f"{user_dwnld_path}chromedriver-win64.zip")
    shutil.rmtree(f"{user_dwnld_path}chromedriver-win64")


def make_driver():
    download_chromedriver()
    time.sleep(1)

    try:
        service = webdriver.ChromeService(chrmdriver_path)
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument('--disable-notifications')
        driver = webdriver.Chrome(service=service, options=options)
    except:
        pass

    return driver
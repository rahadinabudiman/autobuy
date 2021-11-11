import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# cookies


def save_cookies(driver, location):
    pickle.dump(driver.get_cookies(), open(location, "wb"))


def load_cookies(driver, location, url=None):
    cookies = pickle.load(open(location, "rb"))
    driver.delete_all_cookies()
    # have to be on a page before you can add any cookies, any page - does not matter which
    driver.get("https://google.com" if url is None else url)
    for cookie in cookies:
        if isinstance(cookie.get('expiry'), float):  # Checks if the instance expiry a float
            # it converts expiry cookie to a int
            cookie['expiry'] = int(cookie['expiry'])
        driver.add_cookie(cookie)


def delete_cookies(driver, domains=None):

    if domains is not None:
        cookies = driver.get_cookies()
        original_len = len(cookies)
        for cookie in cookies:
            if str(cookie["domain"]) in domains:
                cookies.remove(cookie)
        if len(cookies) < original_len:  # if cookies changed, we will update them
            # deleting everything and adding the modified cookie object
            driver.delete_all_cookies()
            for cookie in cookies:
                driver.add_cookie(cookie)
    else:
        driver.delete_all_cookies()


# save cookies
cookies_location = "C:\\Users\\R4HA\\Documents\\r4habotcookies.txt"

# link produk
link_produk = None


def SetupSelenium():
    options = Options()
    options.add_argument("user-data-dir=/tmp/tarun")
    browser = webdriver.Chrome(chrome_options=options)
    # browser = webdriver.Chrome()
    save_cookies(browser, cookies_location)
    return browser


# input link produk
def InputData():
    global link_produk
    link_produk = input("Masukkan Link Produk : ")


# check barang jika ada
def click(browser, xpath):
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    browser.find_element_by_xpath(xpath).click()


InputData()
browser = SetupSelenium()
wait = WebDriverWait(browser, 60)

# direct login
browser.maximize_window()
browser.get("https://www.shopee.co.id/buyer/login")

# check login
wait.until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div[1]/div/ul/li[2]/div/div/div/div[1]/img')))

# direct ke produk
browser.get(link_produk)

# jika ada variant
# catatan button[1] buat ganti variant
click(browser,
      '//*[@id="main"]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[4]/div/div[3]/div/div[1]/div/button[1]')

# Beli Sekarang
click(browser,
      '//*[@id="main"]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[5]/div/div/button[2]')
wait.until(EC.invisibility_of_element_located(
    (By.XPATH, '//*[@id="main"]/div/div[3]')))

# direct ke checkout
click(browser,
      '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[7]/button[4]')

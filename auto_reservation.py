from argparse import Action
import enum
from tkinter.filedialog import Open
from selenium import webdriver
import logging
import logging.handlers
from time import sleep
import bs4
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Logの設定
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
h1=logging.handlers.RotatingFileHandler('Log.txt', maxBytes=100000, backupCount=10)
h1.setLevel(logging.DEBUG)
formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
h1.setFormatter(formatter)
logger.addHandler(h1)


def check_open(day="2022-04-18", time="15:30"):
    day = "'" + day + "'"
    time = "'" + time + "-" + "'"
    print("day", day)
    print("time", time)
    # 予約受付開始前の状態を確認
    not_open_path = "//td[@data-name_message='お電話にてお問い合わせください']"
    NotOpenElement = driver.find_elements_by_xpath(not_open_path)
    if len(NotOpenElement) < 0:
        logger.debug('-- 予約受付開始前です。 --')
        print("予約受け付け開始時間前です。")
        return None, not_open_path

    else:
        # open_path = "//tr[th[@data-sys_time = {0}]]/td[input[@value = {1}]]/span[contains(text(), '◎')]".format(time, day)
        open_path = "//tr[th[contains(text(), {0})]]/td[input[@value = {1}]]/span[contains(text(), '◎')]".format(time, day)
        logger.debug('-- open path = {} --'.format(open_path))
        OpenElement = driver.find_elements_by_xpath(open_path)
        logger.debug('-- 予約を進めます --')
        print("予約を進めます。")
        # open_path = open_path.replace("/span[contains(text(), '◎')]", "")
        # open_path = "//tr[th[contains(text(), {0})]]/td/input[@value = {1}]".format(time, day)
        return OpenElement, open_path



# def open_hour(name, start="6", end="24"):
#     logger.debug("-- 営業時間設定 --")
#     print(start)
#     print(end)
#     minutes = end - start
#     minutes = minutes / 30
#     for minute in range(1, minutes):

#     print(minutes)



logger.debug('-- WebDriverの設定 --')
# try:
# DriverManager : https://jpdebug.com/p/2615980
# Chromeの場合
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.cityheaven.net/kanagawa/A1403/A140301/afterschool/A6ShopReservation/') # お店予約ページ
# driver.get('https://www.cityheaven.net/kanagawa/A1403/A140301/afterschool/') # お店トップページ

# 参考サイト: https://tetoblog.org/2021/05/disney-scraping/
# 参考サイト２: https://qiita.com/memakura/items/20a02161fa7e18d8a693

# 待機時間の設定
logger.debug('-- 待機時間の設定 --')
wait = WebDriverWait(driver, 10) # 最大待機時間 10 秒
wait.until(EC.visibility_of_all_elements_located)
# sleep(10)

# ページ要素の取得
logger.debug('-- ページ要素の取得 --')
# button = driver.find_element_by_id('reserve_btn')
# button.click()
wait.until(EC.visibility_of_all_elements_located)

# サイトにiframeが使われているときは、iframeに出入りする必要がある。
# https://qiita.com/hondy12345/items/c7359c300c73afd11d76
# ここでiframeに入る
logger.debug('-- enter iframe --')
iframe = driver.find_element_by_id('pcreserveiframe')
driver.switch_to.frame(iframe)
# iframeから抜けるコード
# driver.switch_to.default_content()

# check_open関数で予約がopenになっているか確認
actions = ActionChains(driver)
logger.debug("-- check_open関数 --")
element, xpath = check_open()
print("element : ", element[0].text, " xpath : ", xpath)
if element != None:
    result = driver.find_element_by_xpath(xpath)
    actions.move_to_element(result)
    sleep(1)
    result.click()
    sleep(10)
    


# BeautifulSoupでtable要素を取得するパターン（今回は使わない）
# html = driver.page_source
# soup = BS(html, "html.parser")

# # カレンダーから予約のページ
# table = soup.findAll("table", {"class":"cth table table-bordered table-responsive concat_table table-fixed"})
# table = table[0]
# table = table.findAll("tr")

# for i, tr in enumerate(table):
#     print(tr.get_text())
#     tmp = tr.findAll("td")
#     for k, td in enumerate(tmp):
#         print(td.get_text())



driver.close()
# except Exception:
#     print(Exception)
#     driver.close()



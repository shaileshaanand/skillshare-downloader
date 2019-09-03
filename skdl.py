from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from getpass import getpass
import time
import wget
import sys
import string


def sanitize(text):
    return "".join(map(lambda letter: letter if letter not in "/\\:*\"\'<>|." else '-', text))


if not len(sys.argv) == 3:
    print("Usage: skdl.py <path> <course id>")
    exit()
path = Path(sys.argv[1])
if not path.exists():
    print("Error: Invalid path")
    exit()
course_id = sys.argv[2]
try:
    int(course_id)
except:
    print("Error: Invalid course id")
    exit()
email = input("Enter SkillShare Email:\n")
passw = getpass("Enter password:")

chrome_opts = Options()
chrome_opts.add_argument("--headless")
print("Opening Chrome Webdriver")
driver = webdriver.Chrome(options=chrome_opts)
course_url = "https://www.skillshare.com/home/"+course_id+"/lessons"
loginurl = "https://www.skillshare.com/login"
print("Opening Login page ...")
driver.get(loginurl)
print("Logging in ...")
driver.find_element_by_class_name("login-form-email-input").send_keys(email)
driver.find_element_by_class_name("login-form-password-input").send_keys(passw)
driver.find_element_by_class_name("btn-login-submit").click()
time.sleep(5)
print("Opening Course page ...")
driver.get(course_url)
time.sleep(5)
path = path/Path("[Skillshare] "+sanitize(driver.find_element_by_xpath(
    r'//*[@id="video-region"]/div/div[2]/div[1]/div/div/h1').text))
path.mkdir(exist_ok=True)
titles = driver.find_elements_by_class_name("session-item-title")
print(str(len(titles))+" vidoes found.\nCollecting links...")

videolinks = []
for title in titles:
    titletext = sanitize(title.text)+".mp4"
    print(" "*50, end="\r")
    print("  "+titletext+" "*30, end="\r")
    title.click()
    time.sleep(3)
    videolinks.append((driver.find_element_by_class_name(
        "vjs-tech").get_attribute("src"), titletext))

driver.close()

for link, filename in videolinks:
    print("\nDownloading "+filename+" ...")
    if not (path/Path(filename)).exists():
        wget.download(link, str(path/Path(filename)))
    else:
        print(filename+" exists, skipping ...", end="")

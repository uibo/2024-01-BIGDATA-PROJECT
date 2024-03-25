from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options = chrome_options)

JOB_URL = "https://www.linkedin.com/jobs/search/?currentJobId=3291207294&geoId=103588929&keywords=PYTHON&location=%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%20%EC%84%9C%EC%9A%B8&refresh=true"
driver.get(JOB_URL)

login = driver.find_element(By.CSS_SELECTOR, ".btn-secondary-emphasis")
login.click()

idbox = driver.find_element(By.CSS_SELECTOR, "#username")
idbox.send_keys("boui2000@naver.com")

pwbox = driver.find_element(By.CSS_SELECTOR, "#password")
pwbox.send_keys("12311231")

login_button = driver.find_element(By.CSS_SELECTOR, "#organic-div > form > div.login__form_action_container > button")
login_button.click()

apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button--top-card button") 
apply_button.click()



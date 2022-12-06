from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import json

app = Flask(__name__)

def wait_find_elements(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        lambda driver: driver.find_elements(by, value)
    )

def wait_find_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        lambda driver: driver.find_element(by, value)
    )

def login(driver, username, password):
    driver.get('https://chat.openai.com/')

    # Login
    login_button_xpath = '//button[normalize-space()="Log in"]'
    login_button = driver.find_element(By.XPATH, login_button_xpath)
    login_button.click()

    # Locate the username and password fields and send the provided credentials
    # driver.find_element(By.NAME, 'username')
    username_field = wait_find_element(driver, By.ID, 'username', 5)
    # username_field = WebDriverWait(driver, 10).until(
    #     lambda driver: driver.find_element(By.ID, 'username')
    # )
    # username_field = driver.find_element(By.ID, 'username')
    username_field.send_keys(username)

    # Locate the continue button and click it
    continue_button_xpath = '//button[normalize-space()="Continue"]'
    # continue_button = driver.find_element(By.XPATH, continue_button_xpath)
    continue_button = wait_find_element(driver, By.XPATH, continue_button_xpath)
    continue_button.click()

    # Locate the password field and send the provided password
    # password_field = driver.find_element(By.NAME, 'password')
    password_field = wait_find_element(driver, By.NAME, 'password')
    password_field.send_keys(password)

    # Locate the login button and click it
    # login_button = driver.find_element_by_xpath('//button[text()="Log in"]')
    login_button = wait_find_element(driver, By.XPATH, '//button[text()="Continue"]')
    login_button.click()

    # Accept the terms of service + onboarding stuff
    wait_find_element(driver, By.XPATH, '//button[text()="Next"]').click()
    wait_find_element(driver, By.XPATH, '//button[text()="Next"]').click()
    wait_find_element(driver, By.XPATH, '//button[text()="Done"]').click()


@app.route('/')
def home():
    response = {
        'response': 'Hello, Sam and homies'
    }
    return json.dumps(response)


@app.route('/query')
def query():
    # Open the login page of the chat site
    driver = webdriver.Chrome()

    # Get the username and password from the query parameters
    username = request.args.get('username')
    password = request.args.get('password')

    # Get the prompt from the query parameters
    prompt = request.args.get('prompt')

    # Login
    login(driver, username, password)

    # Locate the chat input field and send the prompt
    chat_input = wait_find_element(driver, By.TAG_NAME, 'textarea')
    chat_input.send_keys(prompt)
    chat_input.send_keys(Keys.ENTER)

    chat_interface_class_name = 'prose'
    response_timeout_seconds = 15
    present_prose_xpath = '(//div[@class="prose" and normalize-space()])[last()]'
    chat_responses = wait_find_elements(driver, By.XPATH, present_prose_xpath, timeout=response_timeout_seconds)

    # [element.text() for element in driver.find_elements(By.CLASS_NAME, chat_interface_class_name)]

    # WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="propse"]')))

    hydrated_responses = WebDriverWait(driver, response_timeout_seconds).until(
        lambda driver: [element.text() for element in driver.find_elements(By.CLASS_NAME, chat_interface_class_name)]
    )
    last_chat_response = hydrated_responses[len(hydrated_responses) - 1]
    response = {
        'response': last_chat_response.text
    }
    return json.dumps(response)


# Register the cleanup function to be called when the app context is torn down
# @app.teardown_appcontext
# def teardown(exception):
#     print("tearing down flask app and browsers")
#     print(exception)

#     if driver:
#         # Close the current window, but keep the browser open
#         driver.close()

#         # Tear down the browser
#         driver.quit()

if __name__ == '__main__':
     app.run_server(debug=True)

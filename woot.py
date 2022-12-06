from flask import Flask, request
from selenium import webdriver
import json

app = Flask(__name__)

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    # Open the login page of the chat site
    driver = webdriver.Chrome()
    driver.get('https://chat.openai.com/')

    # Locate the username and password fields and send the provided credentials
    username_field = driver.find_element_by_name('username')
    password_field = driver.find_element_by_name('password')
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Locate the login button and click it
    login_button = driver.find_element_by_xpath('//button[text()="Log In"]')
    login_button.click()

@app.route('/query')
def query():
    # Get the prompt from the query parameters
    prompt = request.args.get('prompt')

    # Locate the chat input field and send the prompt
    chat_input = driver.find_element_by_id('chat-input')
    chat_input.send_keys(prompt)

    # Locate the send button and click it
    send_button = driver.find_element_by_id('send-button')
    send_button.click()

    # Locate the chat response and return it as JSON
    chat_response = driver.find_element_by_class_name('chat-response')
    response = {
        'response': chat_response.text
    }
    return json.dumps(response)

if __name__ == '__main__':
    app.run()

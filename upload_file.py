import os
import re

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from googlle_drive import google_drive_connect, delete_file


# Function to extract the URL from the HTML snippet
def extract_url(html_snippet):
    start = html_snippet.find("href='") + len("href='")
    end = html_snippet.find("'", start)
    return html_snippet[start:end].replace('&amp;', '&')


# Function to handle form-based redirection
def handle_form_redirect(response, session):
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form')
    if form:
        action = form['action']
        inputs = form.find_all('input')
        data = {input['name']: input['value'] for input in inputs if input['type'] != 'submit'}
        return session.post(action, data=data)
    return response


# Function to save a file from a URL
def save_file(patient_id, file_url, file_name_c, folder_id, service, driver88):
    directory = 'Media'
    file_name = re.sub(r'/', '.', file_name_c)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Specify the path to the chromedriver.exe
    chromedriver_path = "C://Chrone/chromedriver.exe"  # Update this path

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    # Login URL and credentials
    login_url = 'https://upload.icanotes.com/idp/account/signin'
    username_str = 'clhbotgarrison'
    password_str = 'Bot@4805$CLH$'

    # Open the login page
    driver.get(login_url)

    try:
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'UserName')))
        password = driver.find_element(By.NAME, 'Password')
        username.send_keys(username_str)
        password.send_keys(password_str)
        password.send_keys(Keys.RETURN)  # Submit the form

        WebDriverWait(driver, 30).until(EC.url_changes(login_url))
        # print("Login successful or redirected")
    except Exception as e:
        print(f'Error during login: {e}')
        driver.quit()
        return

    # Check if login was successful
    if driver.current_url != login_url:
        pass
        # print('Login successful.')
    else:
        print('Failed to log in or incorrect URL.')
        driver.quit()
        return

    # Extract cookies from Selenium driver
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    try:
        # Direct download using requests session
        response = session.get(file_url)
        if response.status_code == 200:
            # Handle form-based redirection if present
            if "form" in response.text.lower():
                response = handle_form_redirect(response, session)

            content_type = response.headers.get('Content-Type')
            content_length = response.headers.get('Content-Length')
            print(f"Content Type: {content_type}, Content Length: {content_length}")

            if content_type == 'application/pdf':
                # Determine the file name from the URL

                # Save the file to the created folder
                with open(os.path.join(directory, file_name), 'wb') as file:
                    file.write(response.content)

                print(f"Downloaded and saved file: {file_name}")
                google_drive_connect(folder_id, file_name, service)
                delete_file(file_name)
            else:
                print(f"Unexpected content type: {content_type}")
                # Print out the HTML content for inspection
                # print("Response content:", response.text)
        else:
            print(f"Failed to download from URL: {file_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading file: {e}")

    # Quit the Selenium driver
    driver.quit()

    # print("Download process completed.")

# Example usage
# html_snippet = "<a href='/api/Patient/DownloadFile?PatientID=1004010688308&amp;RecordID=106105317' target='_blank' tabindex='-1' class='glyphicon glyphicon-download-alt pointer' alt='Download this document' title='Download this document'></a>"
# file_url = "https://upload.icanotes.com" + extract_url(html_snippet)
# print(extract_url(html_snippet))
# save_file("./first_dir_files", file_url)

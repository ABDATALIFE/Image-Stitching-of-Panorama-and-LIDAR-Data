import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_employee_status_dynamic(url, username, password):
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    
    # Log in to the website
    driver.find_element(By.NAME, 'Abdul Basit Aftab').send_keys(username)
    driver.find_element(By.NAME, 'bstbasit123.').send_keys(password)
    driver.find_element(By.NAME, 'submit').click()
    
    # Wait for login to complete and dashboard to load
    time.sleep(5)  # Adjust sleep time as needed
    
    # Navigate to 'Current Attendance Report'
    driver.find_element(By.LINK_TEXT, 'Current Attendance Report').click()
    
    # Wait for the attendance report to load
    time.sleep(5)  # Adjust sleep time as needed
    
    # Extract the table data
    attendance_data = []
    table = driver.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        if cols:
            employee_name = cols[0].text
            time_in = cols[1].text
            time_out = cols[2].text
            attendance_data.append({
                'Employee Name': employee_name,
                'Time In': time_in,
                'Time Out': time_out
            })
    
    driver.quit()
    return attendance_data

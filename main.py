### Import Statements ###
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime
import pandas as pd
import time


today = datetime.now()
now = datetime.now()
preference = int(input("Are you looking for today's or tomorrows schedule? 0 for today, 1 for tomorrow: "))
day = today.weekday() + 1 + preference

izban_url = "http://www.izban.com.tr/Sayfalar/SeferSaatleri.aspx?MenuId=22" # Website I'm scraping from

# Chrome driver location. Please use the Chrome driver, same as your Chrome version, and update the driver location below. 
service = Service("/Users/deringezgin/Documents/deringezgin/CS Books/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get(izban_url)
driver.maximize_window()
time.sleep(1)

# Selecting the day from the day box
select_day = driver.find_elements(by=By.CSS_SELECTOR, value="#ctl00_CPH_drpGun option")
select_day[day].click()
time.sleep(1)

# Scraping the station names and storing them
select_departure = driver.find_elements(by=By.CSS_SELECTOR, value='#ctl00_CPH_drpHareketDur option')
time.sleep(1)

stations = []
for i in range(len(select_departure)):
    try:
        select_departure = driver.find_elements(by=By.CSS_SELECTOR, value='#ctl00_CPH_drpHareketDur option')
        stations.append(select_departure[i].text)
        print(select_departure[i].text)
    except StaleElementReferenceException:
        select_departure = driver.find_elements(by=By.CSS_SELECTOR, value='#ctl00_CPH_drpHareketDur option')
        stations.append(select_departure[i].text)
        print(select_departure[i].text)

# Taking input for the user for departure station. Checking if it's in the available station list.
while True:
    departure = input("\nWhat's your departure station? Select from above: ").title()
    if departure in stations:
        departure_index = stations.index(departure)
        break
    else:
        print("Invalid entry please enter again.")
time.sleep(1)

# Taking input for the user for arrival station. Checking if it's in the available station list.
while True:
    arrival = input("\nWhat's your arrival station? Select from above: ").title()
    if arrival in stations:
        arrival_index = stations.index(arrival)
        break
    else:
        print("Invalid entry please enter again.")
time.sleep(1)

# Finding the departure station in the website and clicking.
departure_station = driver.find_element(by=By.XPATH,
                                        value=f'//*[@id="ctl00_CPH_drpHareketDur"]/option[{departure_index + 1}]')
departure_station.click()
time.sleep(1)

# Finding the arrival station in the website and clicking.
arrival_station = driver.find_element(by=By.XPATH,
                                      value=f'//*[@id="ctl00_CPH_drpVarisDur"]/option[{arrival_index + 1}]')
arrival_station.click()
time.sleep(1)

# Clicking the search button.
search_button = driver.find_element(by=By.ID, value="ctl00_CPH_Goster")
search_button.click()
time.sleep(5)

# Scraping the departure and arrival times.
normal_rows = driver.find_elements(by=By.CSS_SELECTOR, value="#ozetSeferSaatleri tr")
departure_times = []
arrival_times = []
normal_rows = normal_rows[4:]
for i in range(len(normal_rows)):
    row = normal_rows[i]
    text = row.text
    text = text.split(" ")
    departure_time = text[0]
    arrival_time = text[1]
    departure_times.append(departure_time)
    arrival_times.append(arrival_time)

# Converting the departure and arrival times into a dictionary and transforming this to a pandas dataframe
data = {
    "Departure": departure_times,
    "Arrival": arrival_times,
}

df = pd.DataFrame(data)
print(df.to_string(index=False))

if preference == 0:
    first_train_index = 0
    for i in range(len(departure_times)):
        leave = departure_times[i]
        leave = leave.split(":")
        leave_time = now.replace(hour=int(leave[0]), minute=int(leave[1]))
        if leave_time > today:
            first_train_index = i
            break

    print(
        f"\nFirst train leaving from {departure} to {arrival} leaves at {departure_times[first_train_index]} and arrives at {arrival_times[first_train_index]}")

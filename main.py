from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome()
driver.get("https://yandex.kz/pogoda/month?lat=43.273564&lon=76.914851&via=hnav")

try:
    # Wait for the elements to be present on the page
    weather_entries = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "climate-calendar__cell"))
    )

    # Create a list to store the data
    weather_data = []

    # Extract data and store it in the list
    for entry in weather_entries:
        try:
            date_element = entry.find_element(By.CLASS_NAME, "climate-calendar-day__day")
            date = date_element.text.strip()

            day_temp_element = entry.find_element(By.CLASS_NAME, "climate-calendar-day__temp-day")
            day_temp = day_temp_element.text.strip()

            night_temp_element = entry.find_element(By.CLASS_NAME, "climate-calendar-day__temp-night")
            night_temp = night_temp_element.text.strip()

            try:
                condition_element = entry.find_element(By.CLASS_NAME, "a11y-hidden")
                weather_condition = condition_element.text.strip()
            except NoSuchElementException:
                weather_condition = "N/A"

            weather_data.append([date, day_temp, night_temp, weather_condition])
        except NoSuchElementException:
            print(f"Skipping entry, could not find elements in: {entry}")

    # Save the data to a CSV file
    with open('weather_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date', 'Day Temperature', 'Night Temperature', 'Weather Condition'])
        csvwriter.writerows(weather_data)

finally:
    # Close the browser
    driver.quit()

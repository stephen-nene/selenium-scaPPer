import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from rest_framework.response import Response

def scrap_tenders(pages_to_scrape=6):
    try:
        options = Options()
        # options.add_argument('--headless')  # Commented out for visibility
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        # Initialize WebDriver
        driver = webdriver.Chrome(options=options)
        driver.get('https://tenders.go.ke/tenders')

        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[2]/div/div[2]/div/div[2]/div/table'))
        )

        # Get page title and current timestamp
        page_title = driver.title.replace(" ", "_")  # Remove spaces for a cleaner filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create the images folder if it doesn't exist
        if not os.path.exists("images"):
            os.makedirs("images")

        # Iterate to click the "next" button multiple times (6-10 pages)
        for i in range(pages_to_scrape):
            print(f"Scraping page {i+1}...")

            # Take a full-page screenshot and save it with a dynamic filename
            screenshot_filename = f"images/{page_title}_{timestamp}_page_{i+1}.png"
            driver.save_screenshot(screenshot_filename)
            print(f"Screenshot saved as {screenshot_filename}")

            # Wait for 2 seconds to simulate human browsing
            time.sleep(2)

            # Try to click the "next page" button, using the first valid selector found
            try:
                # Define the possible XPaths/CSS selectors for the "next page" button
                next_button_selectors = [
                    '/html/body/div[1]/div/div/main/div/div/div[2]/div/div[2]/div/div[3]/nav/ul/li[14]/button/span[3]/i',
                    '//*[@id="app"]/div/div/main/div/div/div[2]/div/div[2]/div/div[3]/nav/ul/li[14]/button/span[3]/i',
                    '#app > div > div > main > div > div > div.v-row.v-row--no-gutters.flex-grow-1 > div > div:nth-child(2) > div > div.d-flex.flex-column.flex-sm-row.align-center.justify-sm-space-between.py-2.px-4 > nav > ul > li.v-pagination__next > button > span.v-btn__content > i'
                ]

                next_button = None
                for selector in next_button_selectors:
                    try:
                        # Try to locate the next button using each selector
                        next_button = driver.find_element(By.XPATH, selector)
                        break  # If found, break out of the loop
                    except Exception as e:
                        continue  # Continue to try the next selector

                if next_button:
                    next_button.click()  # Click the "next" button
                    print(f"Clicked the 'next' button on page {i+1}")
                else:
                    print(f"No 'next' button found on page {i+1}. Scraping complete.")
                    break  # Exit if no next button is found

            except Exception as e:
                print(f"Error clicking the 'next' button: {e}")
                break

        # Close the driver after completing the scraping
        driver.quit()
        return Response({"message": f"Scraping completed and screenshots saved for {pages_to_scrape} pages."}, status=200)

    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({"error": "An error occurred during scraping."}, status=400)

if __name__ == "__main__":
    # Specify the number of pages you want to scrape (6 to 10 pages)
    pages_to_scrape = 6
    response = scrap_tenders(pages_to_scrape)
    print(response.data)

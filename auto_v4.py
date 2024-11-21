from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random
import string
from tkinter import *


def setup_edge_driver(acc):
    """Set up Microsoft Edge WebDriver with options"""
    try:
        options = Options()

        # Enhanced options to prevent crashes
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-popup-blocking')

        # Get current Windows username
        username = os.getenv('USERNAME')

        # Use your existing Edge profile
        user_data_dir = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data"

        # Check if the profile directory exists
        if os.path.exists(user_data_dir):
            if acc == "Default":
                # Use the Default profile as-is
                pass
            else:
                # Use the specified profile directory
                options.add_argument(f"user-data-dir={user_data_dir}")
                options.add_argument(f"profile-directory={acc}")
        else:
            print(f"Profile directory not found: {user_data_dir}")
            return None

        # Set page load strategy to none
        options.page_load_strategy = 'none'

        # Specify the exact path where msedgedriver.exe is located
        driver_path = "D:\\python\\edge_rewards\\msedgedriver.exe"

        # Verify if driver exists
        if not os.path.exists(driver_path):
            print(f"Driver not found at: {driver_path}")
            return None

        print(f"Found driver at: {driver_path}")

        # Create service object with the driver path
        service = Service(executable_path=driver_path)
        service.log_path = "edgedriver.log"

        # Initialize the driver with both service and options
        driver = webdriver.Edge(service=service, options=options)
        driver.set_page_load_timeout(30)

        return driver
    except Exception as e:
        print(f"Error setting up driver: {str(e)}")
        with open("error_log.txt", "a") as f:
            f.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}")
        return None


def set_sink_status(driver, status="approved"):
    """Set the sink status in Bing"""
    try:
        print(f"Setting sink status to: {status}")
        # Execute JavaScript to set sink status
        script = f"window.localStorage.setItem('sink_status', '{status}')"
        driver.execute_script(script)
        print("Sink status set successfully")
    except Exception as e:
        print(f"Error setting sink status: {str(e)}")
        with open("error_log.txt", "a") as f:
            f.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - Error setting sink status: {str(e)}")


def open_multiple_tabs(search_queries, acc):
    """Open multiple tabs with search queries"""
    driver = None
    try:
        print("Starting Edge setup...")
        driver = setup_edge_driver(acc)
        if driver is None:
            raise Exception("Failed to initialize driver")

        # Set sink status before performing searches
        set_sink_status(driver, "approved")

        # Open Bing in the first tab
        print("Navigating to Bing...")
        driver.get("https://www.bing.com")
        time.sleep(5)

        # Perform searches in separate tabs
        for i, query in enumerate(search_queries):
            try:
                print(f"Processing search {i + 1}: {query}")

                # Open new tab using JavaScript
                driver.execute_script("window.open('');")
                time.sleep(1)

                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

                # Navigate to Bing in the new tab
                driver.get("https://www.bing.com")

                print("Waiting for search box...")
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "q"))
                )

                print(f"Entering search query: {query}")
                search_box.clear()
                search_box.send_keys(query)
                search_box.send_keys(Keys.RETURN)

                # Wait between searches
                time.sleep(10)

            except Exception as e:
                print(f"Error processing search {i + 1}: {str(e)}")
                continue

        # Keep the browser open for viewing results
        time.sleep(7)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        with open("error_log.txt", "a") as f:
            f.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}")

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing driver: {str(e)}")


def kill_edge_processes():
    try:
        os.system("taskkill /f /im msedge.exe")
        time.sleep(2)
    except:
        pass


def generate_random_text(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


# Example usage
# if __name__ == "__main__":
#     kill_edge_processes()
#     search_queries = [generate_random_text() for _ in range(30)]
#     open_multiple_tabs(search_queries, "Default")
#     time.sleep(5)
#     for i in range(8):
#         kill_edge_processes()
#         accounts = ["Profile 1", "Profile 2","Profile 3"]
#         for acc in accounts:
#             # List of search queries for multiple tabs
#             search_queries = [generate_random_text() for _ in range(4)]
#
#             # Perform searches in multiple tabs
#             open_multiple_tabs(search_queries, acc)
#         time.sleep(900)
#     os.system("shutdown /s")

screen = Tk()
screen.title("collect your edge rewards coin in 1 click")
screen.geometry("1050x400")

welcome = Label(text="Welcome please enter matrix a,A to solve your question ", fg="red", bg="yellow")
welcome.pack()
welcome.place(x=375, y=10)

matrix_a = Label(text="Matrix a = ", fg="black")
matrix_a.pack()
matrix_a.place(x=15, y=87)

matrix_A = Label(text="Matrix A = ", fg="black")
matrix_A.pack()
matrix_A.place(x=515, y=87)

scalar = Label(text="n.a =", fg="black")
scalar.pack()
scalar.place(x=852.5, y=325.5)

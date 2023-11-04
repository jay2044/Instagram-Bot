import os
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def main():
    username = "xxx"
    password = "xxx"

    next_time = random.randint(2, 6)
    unfollow_limit = random.randint(20, 40)
    unfollow_count = 0

    print("Starting")

    # # Set the path to the GeckoDriver binary in the PATH environment variable
    # geckodriver_path = "/home/xxx/geckodriver"  # Replace with the correct path
    # os.environ["PATH"] = f"{os.environ['PATH']}:{os.path.dirname(geckodriver_path)}"

    # # Set the path to the Firefox binary using an environment variable
    # os.environ[
    #     "MOZ_HEADLESS"
    # ] = "1"  # Set this to "0" if you want to run Firefox with a visible window

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    try:
        login(driver, username, password)

        original_tab = driver.current_window_handle

        driver.execute_script("window.open('', '_blank');")

        send_text_message(driver, f"unfollowing {unfollow_limit} users")

        driver.switch_to.window(original_tab)
        driver.get(f"https://www.instagram.com/{username}/following/")

        scroll(driver)
        scroll(driver)

        start(driver, unfollow_count, unfollow_limit, next_time)

        # Close the browser
        driver.quit()

        sleep(next_time)

    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        driver.quit()
        send_text_message(driver, "error in main")


def sleep(hours):
    print(f"Next in {hours} hours.")
    time.sleep(
        hours * 3600
    )  # Convert hours to seconds and sleep until the next execution
    main()


def login(driver, username, password):
    try:
        # Open Instagram in the browser
        driver.get("https://www.instagram.com")
        # Add a delay to ensure the page is fully loaded before interacting with elements
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(username)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(password)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(Keys.RETURN)

        successful_login_url = "https://www.instagram.com/accounts/onetap/?next=%2F"
        WebDriverWait(driver, 20).until(EC.url_to_be(successful_login_url))

        print("Logged in successfully!")

    except Exception as e:
        print(f"login in failed due to {str(e)}")
        sleep(24)


def start(driver, unfollow_count, unfollow_limit, next_time):
    try:
        users = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "x1dm5mii"))
        )
        print(f"unfollowing {unfollow_limit} users")
        print(f"already unfollowed {unfollow_count} users")
        for user in users:
            if unfollow_count >= unfollow_limit:
                break

            # unfollow
            WebDriverWait(user, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_aj1-"))
            ).click()

            # confirm
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_a9-_"))
            ).click()

            time.sleep(
                random.randint(2, 5)
            )  # Add a delay to avoid rapid unfollow actions
            unfollow_count += 1
            name_of_user = user.find_element(By.CLASS_NAME, "x1rg5ohu").text
            print(f"{unfollow_count}.Unfollowed {name_of_user}")

        if unfollow_count < unfollow_limit:
            scroll(driver)
            start(driver, unfollow_count, unfollow_limit, next_time)

        print(f"Successfully unfollowed {unfollow_count} users.")
        send_text_message(
            driver,
            f"Successfully unfollowed {unfollow_count} users. Next in {next_time} hours",
        )

    except Exception as e:
        print(f"Failed to unfollow users: {str(e)}")
        send_text_message(driver, "error start")


def scroll(driver):
    scroll_amount = 500

    # Scroll in increments of the scroll amount
    scroll_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_aano"))
    )
    scroll_height = driver.execute_script(
        "return arguments[0].scrollHeight", scroll_element
    )
    current_scroll = 0
    print("scrolling")
    while current_scroll < scroll_height:
        driver.execute_script(
            f"arguments[0].scrollBy(0, {scroll_amount});", scroll_element
        )
        time.sleep(5)  # Add a delay to allow new content to load
        current_scroll += scroll_amount


def send_text_message(driver, message):
    # Replace 'direct_url' with the URL of the direct message conversation you want to send the message to
    direct_url = "https://www.instagram.com/direct/t/xxx"
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(direct_url)

    try:
        # Use WebDriverWait to wait for the "unfollow" confirmation button element to be present
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_a9_1"))
        )
        button.click()
        print("Button clicked successfully.")
    except TimeoutException:
        print("Button not found. Skipping the click action.")

    # Find the input field where you want to send the text
    input_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "x1gh3ibb"))
    )

    # Create an instance of ActionChains
    actions = ActionChains(driver)

    # Type the message in the input field
    actions.send_keys_to_element(input_field, message)

    # Perform the actions (type the message)
    actions.perform()

    # Send the message by pressing Enter (Return)
    actions.send_keys_to_element(input_field, Keys.RETURN)
    actions.perform()


if __name__ == "__main__":
    main()

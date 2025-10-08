# Import necessary libraries
import os  # Used to interact with the operating system, specifically for getting environment variables.
import time  # Provides time-related functions, used here for pausing the script.
from dotenv import load_dotenv  # Function to load environment variables from a .env file.

# Import Selenium components
from selenium import webdriver  # The main library for browser automation.
from selenium.webdriver.chrome.service import Service  # Manages the ChromeDriver service.
from selenium.webdriver.common.by import By  # Used to specify how to locate elements (e.g., by XPATH, NAME, CSS_SELECTOR).
from selenium.webdriver.common.keys import Keys  # Allows for sending keyboard keys like ENTER.
from selenium.webdriver.support.ui import WebDriverWait  # Used to wait for certain conditions before proceeding.
from selenium.webdriver.support import expected_conditions as EC  # A set of predefined conditions to use with WebDriverWait.
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException  # Specific errors to handle gracefully.

# --- CONFIGURATION ---

# Load environment variables from the .env file into the script's environment.
# This keeps your sensitive credentials out of the source code.
load_dotenv()

# Retrieve credentials from the loaded environment variables.
USERNAME = os.getenv("INSTA_USER")
PASSWORD = os.getenv("INSTA_PASS")

# Bot settings that can be easily changed.
SIMILAR_ACCOUNT = "buzzfeedtasty"  # The target account whose followers the bot will follow.
SCROLL_COUNT = 5  # The number of times to scroll down the followers list to load more users.

# --- SELECTORS (Most likely to change with Instagram updates) ---
# Storing selectors as constants makes them easier to update when Instagram changes its website structure.
# NOTE: Instagram uses dynamic, auto-generated class names. These selectors are fragile and may require frequent updates.
COOKIE_DECLINE_BUTTON = "//button[text()='Decline optional cookies']"  # XPath for the cookie decline button.
FOLLOWERS_MODAL_SCROLLABLE_DIV = "._aano"  # CSS Selector for the scrollable area within the followers pop-up.
FOLLOW_BUTTON_IN_MODAL = "//button/div/div[text()='Follow']"  # XPath for the 'Follow' button inside the followers list.
CANCEL_UNFOLLOW_BUTTON = "//button[text()='Cancel']"  # XPath for the 'Cancel' button in the unfollow confirmation dialog.


class InstaFollower:
    """A bot to follow the followers of a specific Instagram account."""

    def __init__(self):
        """Initializes the WebDriver."""
        # This setup correctly initializes the ChromeDriver service.
        service = Service()
        options = webdriver.ChromeOptions()
        # This option keeps the Chrome browser open after the script finishes, which is useful for debugging.
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=service, options=options)
        # Set up an explicit wait. The bot will wait a maximum of 15 seconds for an element to meet a condition.
        self.wait = WebDriverWait(self.driver, 15)

    def login(self):
        """Logs into Instagram and handles initial pop-ups."""
        print("Logging in...")
        # Check if credentials were loaded correctly from the .env file.
        if not USERNAME or not PASSWORD:
            raise ValueError("INSTA_USER and INSTA_PASS not found in .env file.")

        # Navigate to the Instagram login page.
        self.driver.get("https://www.instagram.com/accounts/login/")
        
        # Handle the cookie consent pop-up if it appears.
        try:
            # Wait for the decline button to be clickable and then click it.
            self.wait.until(EC.element_to_be_clickable((By.XPATH, COOKIE_DECLINE_BUTTON))).click()
        except TimeoutException:
            # If the pop-up doesn't appear within the timeout period, print a message and continue.
            print("Cookie pop-up not found. Continuing...")

        # Find the username and password input fields.
        username_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        password_input = self.driver.find_element(By.NAME, "password")
        
        # Enter the credentials and press ENTER to log in.
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.ENTER)
        
        # Wait for the home page to load by confirming the user's profile icon is present.
        # This is a reliable way to check for a successful login.
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"a[href='/{USERNAME}/']")))
        print("Login successful.")

    def find_and_follow_followers(self):
        """Navigates to the target's followers list, scrolls, and follows."""
        print(f"Navigating to {SIMILAR_ACCOUNT}'s followers...")
        # Go to the followers page of the target account.
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers")

        try:
            # Wait for the followers pop-up modal to become visible.
            modal = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, FOLLOWERS_MODAL_SCROLLABLE_DIV)))
            
            print(f"Scrolling {SCROLL_COUNT} times to load followers...")
            # Scroll down inside the modal multiple times to load more users.
            for i in range(SCROLL_COUNT):
                # Execute JavaScript to scroll to the bottom of the modal.
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                # Pause for 2 seconds to allow new followers to load before the next scroll.
                time.sleep(2)

            # Find all the 'Follow' buttons that are now visible in the list.
            follow_buttons = self.driver.find_elements(By.XPATH, FOLLOW_BUTTON_IN_MODAL)
            print(f"Found {len(follow_buttons)} users to follow.")

            # Iterate through each button and click it.
            for button in follow_buttons:
                try:
                    button.click()
                    # Pause between each follow to mimic human behavior and avoid being rate-limited by Instagram.
                    time.sleep(1.5)
                except ElementClickInterceptedException:
                    # This error occurs if you are already following the user, which opens an "Unfollow" dialog.
                    print("Already following or element blocked. Skipping.")
                    # In this case, we find the 'Cancel' button to close the dialog and continue.
                    try:
                        cancel_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, CANCEL_UNFOLLOW_BUTTON)))
                        cancel_button.click()
                    except TimeoutException:
                        # If the cancel button isn't found, just ignore and move on.
                        pass
            
            print("Finished following session.")

        except TimeoutException:
            # This error will occur if the followers list modal doesn't appear.
            print(f"Error: Could not find the followers list for {SIMILAR_ACCOUNT}. Instagram's layout may have changed.")

    def close_browser(self):
        """Closes the browser window."""
        print("Closing browser.")
        self.driver.quit()


# This block ensures the code runs only when the script is executed directly (not when imported).
if __name__ == "__main__":
    bot = InstaFollower()
    # The try...finally block is crucial for ensuring the browser closes properly.
    try:
        bot.login()
        bot.find_and_follow_followers()
    except Exception as e:
        # Catch any unexpected errors during execution and print them.
        print(f"An unexpected error occurred: {e}")
    finally:
        # This 'finally' block will run whether the script succeeds or fails.
        # It guarantees that the browser window is closed, preventing leftover processes.
        bot.close_browser()
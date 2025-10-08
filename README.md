# Py-Day52
# Instagram Follower Bot

A Python bot that uses Selenium to automatically follow the followers of a specified Instagram account.

## ⚠️ Disclaimer

This bot automates actions on Instagram, which is **strictly against their Terms of Service**. Use this script at your own risk. 

-   Your account could be **temporarily blocked** or **permanently banned**.
-   It is highly recommended to use this with a **test account**.
-   Run the bot **infrequently** and with reasonable settings to avoid detection.

The developer is not responsible for any consequences of using this script.

---

## Features

-   🔐 Securely logs into your Instagram account using credentials from a `.env` file.
-   🎯 Navigates to a target account's followers list.
-   📜 Scrolls through the follower list to load a set number of users.
-   🤖 Follows each user in the loaded list, skipping those you already follow.
-   ✅ Ensures the browser closes properly, even if errors occur.

---

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.8+**
2.  **Google Chrome** browser
3.  **ChromeDriver**: You **must** download the ChromeDriver that **exactly matches your version of Google Chrome**.
    -   Check your Chrome version by typing `chrome://settings/help` in your browser's address bar.
    -   Download the corresponding ChromeDriver from the [official site](https://googlechromelabs.github.io/chrome-for-testing/).
    -   Place the `chromedriver.exe` (or `chromedriver` on Mac/Linux) file in the **same folder** as `main.py`.

---

## 🚀 Setup and Installation

Follow these steps to set up the project on your local machine.

**1. Get the Code**
   - Download the project files and place them in a new folder.

**2. Create a Virtual Environment (Recommended)**
   - A virtual environment isolates the project's dependencies.
     ```bash
     # Create a virtual environment named 'venv'
     python -m venv venv

     # Activate it
     # On Windows:
     .\venv\Scripts\activate
     # On macOS/Linux:
     source venv/bin/activate
     ```

**3. Install Dependencies**
   - Install all the required Python packages using the `requirements.txt` file.
     ```bash
     pip install -r requirements.txt
     ```

**4. Configure Credentials**
   - Create a new file in the project folder named `.env`.
   - Open the `.env` file and add your Instagram credentials in the following format:
     ```
     INSTA_USER="YOUR_USERNAME_HERE"
     INSTA_PASS="YOUR_PASSWORD_HERE"
     ```

---

## ⚙️ Usage

**1. Configure the Bot**
   - Open the `main.py` file and adjust the settings in the `CONFIGURATION` section:
     - **`SIMILAR_ACCOUNT`**: The target account whose followers you want to follow.
     - **`SCROLL_COUNT`**: The number of times to scroll down the followers list (more scrolls = more users).

**2. Run the Script**
   - Execute the bot from your terminal:
     ```bash
     python main.py
     ```
   - The bot will open a Chrome window and begin the process. Watch the terminal for progress updates.

---

## A Note on Maintenance

Instagram frequently updates its website structure. If the bot stops working (e.g., it can't find the followers list or the follow buttons), you will likely need to update the **`SELECTORS`** constants at the top of the `main.py` file. This requires using your browser's developer tools to find the new XPath or CSS selector for the changed elements.

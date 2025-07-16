"""
This file contains examples of how to use SeleniumBase's CDP mode
without a context manager (the "with" statement).
This allows you to keep the browser open after the script finishes.
"""
from seleniumbase import Driver
from seleniumbase import sb_cdp

# Example 1: Using the Driver class
# The browser will remain open after the script finishes
# because we are not using a context manager and we are not
# calling driver.quit()
driver = Driver(uc=True)
driver.uc_open_with_reconnect("https://nowsecure.nl/#relax", 5)
driver.set_messenger_theme(theme="flat", location="top_center")
driver.post_message("The browser will not close automatically!")


# Example 2: Using sb_cdp.Chrome
# The browser will remain open after the script finishes
# because we are not using a context manager and we are not
# calling sb.driver.stop()
sb = sb_cdp.Chrome()
sb.open("https://seleniumbase.io/realworld/login")
sb.type("#username", "demo_user")
sb.type("#password", "secret_pass")
sb.click('button:contains("Sign in")')
sb.assert_text("Welcome!", "h1")
# The browser will not close automatically!
# To close the browser, you would call:
# sb.driver.stop()

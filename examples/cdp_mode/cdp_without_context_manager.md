# How to use CDP mode without a context manager

This document explains how to use SeleniumBase's CDP mode without a context manager (the `with` statement). This is useful when you want to keep the browser open after your script has finished running.

There are two main ways to do this:

## 1. Using the `Driver` class

You can import the `Driver` class from `seleniumbase` and instantiate it directly. To use CDP mode, you must pass the `uc=True` argument to the constructor.

```python
from seleniumbase import Driver

driver = Driver(uc=True)
driver.uc_open_with_reconnect("https://nowsecure.nl/#relax", 5)
driver.set_messenger_theme(theme="flat", location="top_center")
driver.post_message("The browser will not close automatically!")
```

In this example, the browser will remain open after the script finishes. This is because we are not using a context manager, and we are not calling `driver.quit()`. If you want the browser to close automatically, you can register the `driver.quit` method with the `atexit` module:

```python
import atexit
from seleniumbase import Driver

driver = Driver(uc=True)
atexit.register(driver.quit)
# ... your code here ...
```

## 2. Using `sb_cdp.Chrome`

You can also use the `sb_cdp.Chrome` class to get a CDP-only driver. This is useful when you don't need any of the WebDriver-specific features of the `Driver` class.

```python
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.open("https://seleniumbase.io/realworld/login")
sb.type("#username", "demo_user")
sb.type("#password", "secret_pass")
sb.click('button:contains("Sign in")')
sb.assert_text("Welcome!", "h1")
```

Just like with the `Driver` class, the browser will remain open after the script finishes because we are not using a context manager. To close the browser, you would call `sb.driver.stop()`.

You can find runnable examples of both of these methods in the `cdp_without_context_manager.py` file.

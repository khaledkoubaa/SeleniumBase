# Using SeleniumBase CDP Mode without a Context Manager (Manual Browser Quit)

This guide explains how to use SeleniumBase, including its CDP (Chrome DevTools Protocol) Mode, without relying on Python's `with` statement (context manager). This approach gives you manual control over the browser's lifecycle, allowing you to keep the browser open after your script has finished its automated tasks.

## Standard Usage with Context Manager

Typically, SeleniumBase is used with a `with` statement:

```python
from seleniumbase import SB

with SB(uc=True, browser="chrome", headless=False) as sb:
    sb.open("https://nowsecure.nl/")
    sb.activate_cdp_mode(sb.get_current_url())
    sb.sleep(5)
    # ... more actions ...
# Browser automatically closes here when exiting the 'with' block
```

The context manager (`with SB(...) as sb:`) ensures that resources are managed correctly, and importantly, `sb.driver.quit()` is called automatically when the block is exited, closing the browser.

## Manual Browser Lifecycle Control

If you want the browser to remain open after your script completes its primary tasks (e.g., for manual inspection, debugging, or further non-scripted interaction), you can instantiate the `SB` object directly without the `with` statement.

**Key Points:**

1.  **Initialization:** Create an instance of `SB` directly.
2.  **CDP Mode:** Activate and use CDP mode as usual.
3.  **Browser Remains Open:** If you don't call `sb.driver.quit()`, the browser window launched by SeleniumBase will stay open even after your Python script finishes.
4.  **Manual Cleanup:** You are responsible for eventually closing the browser by calling `sb.driver.quit()`. If you don't, the browser process and its associated WebDriver process might linger.

## Python Code Example

Here's how you can structure your code:

```python
from seleniumbase import SB
import time # For demonstration pauses

# 1. Initialize SB directly (not using 'with')
# You can pass any valid SB arguments here.
# uc=True is necessary for CDP mode.
# headless=False (or headless2=False for newer Chrome) is needed to see the browser.
sb = SB(uc=True, browser="chrome", headless=False, test=True)

try:
    # 2. Open a page and activate CDP mode
    url = "https://nowsecure.nl/"
    # url = "https://seleniumbase.io/demo_page" # Another option
    print(f"Opening {url}...")
    sb.open(url) # Initial open can be done with WebDriver active

    print(f"Activating CDP mode for {url}...")
    sb.activate_cdp_mode(sb.get_current_url()) # Disconnects WebDriver
    print(f"WebDriver connected: {sb.is_connected()} (should be False)")

    # 3. Perform your CDP actions
    print("Performing some CDP actions...")
    sb.cdp.highlight("body") # Flash the body element
    sb.sleep(1) # Short pause
    current_title = sb.cdp.get_title()
    print(f"Page title via CDP: {current_title}")
    sb.cdp.save_screenshot("cdp_manual_quit_page.png")
    print("Took a screenshot via CDP.")

    sb.sleep(3) # Pause for observation

    # 4. Script finishes its automated tasks
    print("-" * 30)
    print("Automated script tasks are complete.")
    print("The browser will remain open.")
    print("You can interact with it manually.")
    print("To close it, you would typically call sb.driver.quit() in your code,")
    print("or close the browser window manually (though quit() is cleaner).")
    print("-" * 30)

    # 5. Keeping the browser open
    # At this point, the script would normally end, and because we are not using
    # a 'with' statement, the browser stays open.

    # To demonstrate manual closure after a delay:
    # You could have a condition here, or an input(), or just let it run.
    # For this example, let's simulate some time passing.
    # In a real scenario, you might remove the quit() call entirely if you
    # always want to close it manually via the browser's X button.

    # keep_open_duration = 30  # seconds
    # print(f"Keeping browser open for manual inspection for {keep_open_duration} seconds...")
    # print(f"Or, press Ctrl+C in the terminal to interrupt and proceed to quit (if quit is enabled below).")
    # time.sleep(keep_open_duration)


except Exception as e:
    print(f"An error occurred: {e}")
    if hasattr(sb, 'driver'): # Check if driver was initialized
        sb.cdp.save_screenshot("cdp_manual_error.png")


finally:
    # 6. Manual browser quit (optional, based on your needs)
    # If you want to programmatically close the browser after certain conditions
    # or a delay, you would call sb.driver.quit() here.
    # If you omit this 'finally' block or the quit() call, the browser stays open
    # until you manually close its window.

    # To ensure browser closes after this script example:
    # print("Example finished. Closing the browser now via sb.driver.quit().")
    # if hasattr(sb, 'driver') and sb.driver:
    #     sb.driver.quit()

    # If you want it to stay open indefinitely after script execution,
    # comment out or remove the sb.driver.quit() call above.
    # For this specific md file's purpose (to show how to keep it open),
    # we will NOT call quit() here, letting the user manage it.
    print("\nScript execution finished. Browser remains open as sb.driver.quit() was not called in this example script's final state.")
    print("You will need to manually close the browser window.")

```

## Notes on Responsibility

*   **Resource Leaks:** When you bypass the context manager, you take on the responsibility of ensuring that browser instances and WebDriver processes are properly terminated. Failing to call `sb.driver.quit()` will leave these processes running, consuming system resources.
*   **Manual Closure:** If the script ends and `sb.driver.quit()` was not called, you'll need to manually close the browser window. This will typically also terminate the associated WebDriver process.
*   **Error Handling:** It's good practice to include `try...finally` blocks to ensure `sb.driver.quit()` can be called even if errors occur during your script, *if* you intend for the script to clean up after itself under certain conditions. If the goal is to always leave it open post-script, then this is less critical for the `quit()` part but still good for other cleanup or logging.

By instantiating `SB` directly, you gain the flexibility to control the browser's lifespan beyond the execution of your automated script, which is particularly useful for debugging or hybrid manual-automated workflows.
---
This Markdown file provides the necessary explanation and an example.

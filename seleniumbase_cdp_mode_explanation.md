# Understanding SeleniumBase CDP Mode

This document provides a comprehensive explanation of SeleniumBase CDP (Chrome DevTools Protocol) Mode, based on the exploration of its official documentation.

## 1. Core Concept of CDP Mode

SeleniumBase CDP Mode is an advanced feature designed to help automated scripts avoid detection by sophisticated anti-bot systems. It builds upon the existing **UC Mode (Undetected-Chromedriver Mode)**.

**How it Works and Why It's Effective:**

1.  **The Problem with Standard WebDriver:**
    *   Websites with robust anti-bot measures can often detect browsers being controlled by WebDriver. They look for tell-tale signs and JavaScript properties that reveal automation.

2.  **UC Mode's Approach:**
    *   UC Mode tries to hide these WebDriver-specific footprints. A key technique is to *disconnect* WebDriver from the browser at critical moments (e.g., when a CAPTCHA or bot check is anticipated).
    *   While disconnected, UC Mode might use other libraries like `PyAutoGUI` to interact with the page in a way that looks more human.
    *   After the sensitive interaction, UC Mode reconnects WebDriver.

3.  **Where CDP Mode Shines:**
    *   CDP Mode enhances UC Mode by providing a way to control the browser *even when WebDriver is disconnected*. It does this by using the Chrome DevTools Protocol directly.
    *   The Chrome DevTools Protocol is the same interface Chrome's own developer tools use. Interacting via CDP is generally less detectable as "automation."

4.  **Key Advantages of CDP Mode:**
    *   **Stealth:** By disconnecting WebDriver and using CDP, scripts can perform actions (clicking, typing, navigating) in a way that is much harder to flag as bot activity.
    *   **Continuous Control:** Offers a rich set of commands to control the browser directly through this "back channel" when WebDriver is disconnected.
    *   **Integration:** SeleniumBase allows activation within a UC Mode test, usage of `sb.cdp` methods, and the option to switch back to WebDriver control if safe. If a WebDriver method is called while disconnected, SeleniumBase attempts to use the CDP equivalent.

In essence, CDP Mode allows SeleniumBase to operate with a significantly lower profile, making it a powerful tool for automating interactions on websites with strong anti-bot defenses.

## 2. Basic Usage Pattern

1.  **Prerequisite: UC Mode:**
    *   CDP Mode operates within UC Mode. Initialize `SB` with `uc=True`.
    ```python
    from seleniumbase import SB

    with SB(uc=True) as sb:
        # Your code
    ```

2.  **Activating CDP Mode:**
    *   Use `sb.activate_cdp_mode(url)`. This navigates to the `url` (if provided and different) and **disconnects WebDriver**.
    ```python
    with SB(uc=True, test=True) as sb:
        url = "https://nowsecure.nl/"
        sb.activate_cdp_mode(url)
        # WebDriver is now disconnected. Use sb.cdp methods.
    ```
    *   If already on the page, `sb.activate_cdp_mode()` or `sb.activate_cdp_mode(sb.get_current_url())` works.

3.  **Using CDP-Specific Methods:**
    *   Interact with the browser using methods under `sb.cdp`.
    ```python
    sb.cdp.click("h1")
    if sb.cdp.is_text_visible("Example Domain", "h1"):
        print("Found text!")
    ```

4.  **Reconnecting WebDriver (Use with Caution):**
    *   To use standard WebDriver methods: `sb.reconnect()` or `sb.connect()`.
    *   **Warning:** Reconnecting makes your script vulnerable to detection again. Only do this if safe.
    ```python
    # sb.reconnect()
    # print(sb.get_title()) # WebDriver method
    ```

5.  **Disconnecting WebDriver (If Reconnected):**
    *   To return to stealthier CDP-only interaction: `sb.disconnect()`.

6.  **Checking Connection Status:**
    *   `sb.is_connected() -> bool`
    ```python
    print(f"WebDriver connected: {sb.is_connected()}")
    ```

**Summary Flow:**
1. Start with `SB(uc=True)`.
2. Call `sb.activate_cdp_mode(url)`.
3. Use `sb.cdp.*` methods.
4. (Optional, cautiously) `sb.reconnect()`.
5. (Optional, if reconnected) `sb.disconnect()`.
6. Use `sb.is_connected()` to verify.

## 3. Simple Illustrative Code Example

```python
from seleniumbase import SB

with SB(uc=True, test=True, headless=False) as sb:
    try:
        url = "https://nowsecure.nl/"
        print(f"Navigating to {url} and activating CDP mode...")
        sb.activate_cdp_mode(url)
        print(f"WebDriver connected: {sb.is_connected()} (should be False)")

        print("Waiting for 5 seconds to observe...")
        sb.sleep(5)

        if sb.cdp.is_text_visible("TLS", timeout=5):
            print("CDP: Found text 'TLS'.")
        else:
            print("CDP: Did not find text 'TLS'.")

        page_title = sb.cdp.get_title()
        print(f"CDP: Page title is: '{page_title}'")

        screenshot_name = "cdp_mode_screenshot.png"
        sb.cdp.save_screenshot(screenshot_name)
        print(f"CDP: Saved screenshot as '{screenshot_name}'")
        sb.assert_true(sb.is_element_present(f"./{screenshot_name}"))

        print("CDP mode demo complete. Pausing...")
        sb.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")
        sb.cdp.save_screenshot("cdp_error_screenshot.png")
```

## 4. Key CDP Methods and Their Uses

**Navigation & Page Information:**
*   `sb.cdp.get(url)`, `sb.cdp.open(url)`: Navigate.
*   `sb.cdp.reload()`, `sb.cdp.refresh()`: Reload.
*   `sb.cdp.go_back()`, `sb.cdp.go_forward()`: History navigation.
*   `sb.cdp.get_title() -> str`: Get page title.
*   `sb.cdp.get_current_url() -> str`: Get current URL.

**Element Interaction:**
*   `sb.cdp.click(selector, timeout=None)`: Primary click method.
*   `sb.cdp.type(selector, text, timeout=None)`: Type text.
*   `sb.cdp.press_keys(selector, text, timeout=None)`: Human-speed typing.
*   `sb.cdp.focus(selector)`: Set focus.

**Finding Elements & Text:**
*   `sb.cdp.find_element(selector, ...)`: Find a single element.
*   `sb.cdp.find_all(selector, ...)`: Find multiple elements.
*   `sb.cdp.get_text(selector) -> str`: Get visible text.
*   `sb.cdp.is_element_visible(selector) -> bool`: Check visibility.
*   `sb.cdp.is_text_visible(text, selector="body") -> bool`: Check text visibility.

**Waiting & Assertions:**
*   `sb.cdp.wait_for_element_visible(selector, timeout=None)`
*   `sb.cdp.wait_for_text(text, selector="body", timeout=None)`
*   `sb.cdp.assert_element_visible(selector, timeout=None)`
*   `sb.cdp.assert_text(text, selector="html", timeout=None)`

**GUI-Based Methods (PyAutoGUI for enhanced stealth):**
*   `sb.cdp.gui_click_element(selector)`: Click using OS-level mouse simulation.
*   `sb.cdp.gui_press_keys(keys)`: Simulate OS-level key presses.
*   **When to use:** For heavily protected elements or CAPTCHAs, when standard CDP clicks are detected. Require a visible browser window.

**Other Useful Methods:**
*   `sb.cdp.sleep(seconds)`: Essential for pacing.
*   `sb.cdp.save_screenshot(name, ...)`: Save screenshot.
*   `sb.cdp.remove_element(selector)`: Remove element from DOM.
*   `sb.cdp.evaluate(expression)`: Execute JavaScript.

## 5. Important Considerations and Best Practices

1.  **Always Start with `uc=True`**.
2.  **Strategic `sb.sleep()`:** Mimic human behavior and allow page rendering.
3.  **Prefer Explicit Waits:** Use `sb.cdp.wait_for_*` methods for specific conditions.
4.  **Cautious Reconnection (`sb.reconnect()`):** Only if absolutely necessary and past main bot checks.
5.  **Leverage GUI Methods (`sb.cdp.gui_*`) for Tough Spots:** For CAPTCHAs or heavily guarded elements. Requires visible window.
6.  **Potential for IP Blocking:** Use good pacing, consider proxies for large tasks.
7.  **PyAutoGUI Dependency:** `gui_*` methods rely on it.
8.  **Headless Mode:** Standard CDP methods work; `gui_*` methods do not. Use `headless2=True` for UC headless.
9.  **Test Incrementally and Observe:** Especially on new sites, run with browser visible.
10. **Ad Blocking (`ad_block=True`) and Locale (`locale_code`)**: Can help.
11. **Keep SeleniumBase Updated (`pip install -U seleniumbase`)**.

## 6. Further Resources

*   **Official SeleniumBase CDP Docs:** [https://seleniumbase.io/examples/cdp_mode/ReadMe/](https://seleniumbase.io/examples/cdp_mode/ReadMe/)
*   **GitHub CDP Examples:** [https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode)
*   **SeleniumBase UC Mode Docs:** [https://seleniumbase.io/help_docs/uc_mode/](https://seleniumbase.io/help_docs/uc_mode/)
*   **SeleniumBase YouTube Channel:** Search for SeleniumBase, often linked in docs.
*   **SeleniumBase Discord Channel:** [https://discord.gg/EdhQTn3EyE](https://discord.gg/EdhQTn3EyE)
*   **Underlying Tech (Advanced):** Chrome DevTools Protocol docs, python-cdp, nodriver.

This concludes the explanation of SeleniumBase CDP Mode.

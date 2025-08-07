# SeleniumBase CDP Mode Reference

## Introduction

SeleniumBase CDP (Chrome DevTools Protocol) Mode is a powerful feature that allows for deep control over Chromium-based browsers (like Chrome and Edge). It's particularly useful for bypassing advanced bot-detection mechanisms that can often detect and block standard WebDriver-based automation.

When CDP mode is active, WebDriver is disconnected from the browser, and a CDP-Driver takes over. This allows your scripts to perform actions without being flagged as a bot. You can then reconnect WebDriver when it's safe to do so.

### Key Features:

*   **Evade Bot Detection:** By disconnecting WebDriver and using the CDP-Driver, you can fly under the radar of many anti-bot systems.
*   **Combined Power:** Use both WebDriver and CDP commands in the same script.
*   **Stealthy Actions:** Perform clicks, typing, and other interactions that appear more human-like.
*   **PyAutoGUI Integration:** For even more advanced stealth capabilities, some CDP methods leverage PyAutoGUI.

## Activating CDP Mode

To use CDP mode, you must be running in UC Mode (`uc=True` or `--uc`). You can then activate CDP mode by calling `sb.activate_cdp_mode(url)`.

Here's a simple example of how to activate CDP mode:

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.uc_gui_click_captcha()
    sb.sleep(2)
```

In this example, `activate_cdp_mode` navigates to the specified URL and enables the CDP driver. After this call, you can start using `sb.cdp` methods.

## Core CDP Methods

Once CDP mode is active, you can access a range of methods through the `sb.cdp` object. Here are some of the most common ones:

| Method                                   | Description                                                                 |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| `sb.cdp.get(url, **kwargs)`              | Navigates to the specified URL.                                             |
| `sb.cdp.open(url, **kwargs)`             | Alias for `get()`.                                                          |
| `sb.cdp.click(selector)`                 | Clicks an element using the CDP API.                                        |
| `sb.cdp.type(selector, text)`            | Types text into an element.                                                 |
| `sb.cdp.press_keys(selector, text)`      | Types text into an element at a human-like speed.                           |
| `sb.cdp.get_text(selector)`              | Returns the text content of an element.                                     |
| `sb.cdp.find_element(selector)`          | Finds a single element.                                                     |
| `sb.cdp.find_elements(selector)`         | Finds a list of elements.                                                   |
| `sb.cdp.is_element_visible(selector)`    | Checks if an element is visible on the page.                                |
| `sb.cdp.wait_for_element_visible(selector)` | Waits for an element to become visible.                                     |
| `sb.cdp.save_screenshot(name)`           | Saves a screenshot of the current page.                                     |
| `sb.cdp.gui_click_element(selector)`     | Clicks an element using PyAutoGUI for more stealth.                         |
| `sb.cdp.gui_write(text)`                 | Types text using PyAutoGUI.                                                 |

This is not an exhaustive list. For a full list of methods, please refer to the official SeleniumBase documentation.

## WebElement CDP Methods

When you find an element using `sb.cdp.find_element()` or `sb.cdp.find_elements()`, you can call a variety of methods on the element itself.

| Method                   | Description                                         |
| ------------------------ | --------------------------------------------------- |
| `element.click()`        | Clicks the element.                                 |
| `element.type(text)`     | Types text into the element.                        |
| `element.get_text()`     | Returns the text content of the element.            |
| `element.get_attribute(name)` | Returns the value of an attribute.                |
| `element.is_visible()`   | Checks if the element is visible.                   |
| `element.scroll_into_view()` | Scrolls the element into view.                    |
| `element.save_screenshot(name)` | Saves a screenshot of the element.              |

## Practical Examples

Here are a few examples of how to use CDP mode to interact with websites that have bot-detection measures.

### Example 1: Interacting with a Form

This example shows how to use CDP mode to fill out a login form on a website that uses Cloudflare protection.

```python
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://www.planetminecraft.com/account/sign_in/"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.cdp.gui_click_element("#turnstile-widget div")
    sb.sleep(2)
    sb.cdp.type('input[name="username"]', "my-username")
    sb.cdp.type('input[name="password"]', "my-password")
    sb.cdp.click('button:contains("Sign in")')
```

### Example 2: Scraping Data

This example demonstrates how to scrape data from a website that is protected by Incapsula/Imperva.

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://www.pokemon.com/us"
    sb.activate_cdp_mode(url)
    sb.sleep(3.2)
    sb.cdp.click("button#onetrust-accept-btn-handler")
    sb.sleep(1.2)
    sb.cdp.click("a span.icon_pokeball")
    sb.sleep(2.5)
    sb.cdp.click('b:contains("Show Advanced Search")')
    sb.sleep(2.5)
    sb.cdp.click('span[data-type="type"][data-value="electric"]')
    sb.sleep(0.5)
    sb.scroll_into_view("a#advSearch")
    sb.sleep(0.5)
    sb.cdp.click("a#advSearch")
    sb.sleep(1.2)
    sb.cdp.click('img[src*="img/pokedex/detail/025.png"]')
    sb.cdp.assert_text("Pikachu", 'div[class*="title"]')
```

## Connection Management

In CDP mode, you have full control over the WebDriver connection. This allows you to disconnect when you need to be stealthy and reconnect when you need to perform standard WebDriver actions.

### Methods for Connection Management:

*   `sb.disconnect()`: Disconnects the WebDriver from the browser. While disconnected, you can only use `sb.cdp` methods.
*   `sb.reconnect()`: Reconnects the WebDriver. This will allow you to use standard `sb` methods again, but it may also make your script detectable by anti-bot systems.
*   `sb.is_connected()`: Returns `True` if the WebDriver is currently connected, and `False` otherwise.

Here's an example of how you might use these methods:

```python
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://example.com"
    sb.activate_cdp_mode(url)

    # Perform some actions with the CDP driver
    print(sb.cdp.get_title())

    # Reconnect to use standard WebDriver methods
    sb.reconnect()
    sb.assert_element("h1")

    # Disconnect again for more stealthy actions
    sb.disconnect()
    sb.cdp.click("a")
```

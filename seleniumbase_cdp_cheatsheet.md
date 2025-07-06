# SeleniumBase CDP Mode - Cheat Sheet

This cheat sheet provides a quick reference to common methods and examples for using SeleniumBase in CDP (Chrome DevTools Protocol) Mode. Remember to activate CDP mode first within a UC Mode test:

```python
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.activate_cdp_mode("https://example.com")
    # Now use sb.cdp methods
    # ...
```

Or, for manual browser lifecycle:
```python
# sb = SB(uc=True)
# sb.open("https://example.com") # Optional: open initial page with WebDriver
# sb.activate_cdp_mode(sb.get_current_url()) # Or pass a new URL
# ...
# sb.driver.quit() # eventually
```

## 1. Key `sb.cdp.*` API Methods (Browser-Level)

This section covers general browser control and interaction methods available via `sb.cdp`.

**Navigation & Page Info:**

*   `sb.cdp.open(url)` or `sb.cdp.get(url)`
    *   Navigates to the given URL.
    *   Example: `sb.cdp.open("https://seleniumbase.io")`
*   `sb.cdp.reload()`
    *   Reloads the current page.
    *   Example: `sb.cdp.reload()`
*   `sb.cdp.go_back()` / `sb.cdp.go_forward()`
    *   Navigates browser history.
    *   Example: `sb.cdp.go_back()`
*   `sb.cdp.get_title() -> str`
    *   Returns the page title.
    *   Example: `title = sb.cdp.get_title()`
*   `sb.cdp.get_current_url() -> str`
    *   Returns the current URL.
    *   Example: `current_url = sb.cdp.get_current_url()`
*   `sb.cdp.get_page_source() -> str`
    *   Returns the page's HTML source.
    *   Example: `source = sb.cdp.get_page_source()`

**Finding Elements:**

*   `sb.cdp.find_element(selector, timeout=None) -> CDPWebElement`
    *   Finds the first element matching the CSS selector.
    *   Example: `el = sb.cdp.find_element("#myId")`
*   `sb.cdp.find_elements(selector, timeout=None) -> list[CDPWebElement]`
    *   Finds all elements matching the CSS selector. (Also `sb.cdp.select_all()`)
    *   Example: `elements = sb.cdp.find_elements("div.item")`
*   `sb.cdp.is_element_visible(selector) -> bool`
    *   Checks if an element is visible.
    *   Example: `is_vis = sb.cdp.is_element_visible("button.submit")`
*   `sb.cdp.is_element_present(selector) -> bool`
    *   Checks if an element is present in the DOM.
    *   Example: `is_pres = sb.cdp.is_element_present("input[name='q']")`

**Interacting with Elements:**

*   `sb.cdp.click(selector, timeout=None)`
    *   Clicks an element.
    *   Example: `sb.cdp.click("a#login-link")`
*   `sb.cdp.type(selector, text, timeout=None)`
    *   Types text into an element. (Also `sb.cdp.send_keys()`)
    *   Example: `sb.cdp.type("input#email", "user@example.com")`
*   `sb.cdp.press_keys(selector, text, timeout=None)`
    *   Types text with human-like speed.
    *   Example: `sb.cdp.press_keys("textarea#comment", "Hello world!")`
*   `sb.cdp.get_text(selector) -> str`
    *   Gets the visible text of an element.
    *   Example: `button_text = sb.cdp.get_text("button#submit")`
*   `sb.cdp.get_attribute(selector, attribute_name) -> str`
    *   Gets an element's attribute value.
    *   Example: `link_href = sb.cdp.get_attribute("a#details", "href")`
*   `sb.cdp.focus(selector)`
    *   Sets focus to an element.
    *   Example: `sb.cdp.focus("input#username")`
*   `sb.cdp.highlight(selector)` / `sb.cdp.flash(selector, duration=1, color="44CC88")`
    *   Visually highlights an element for debugging.
    *   Example: `sb.cdp.highlight("div.important-notice")`
*   `sb.cdp.scroll_into_view(selector)`
    *   Scrolls the element into the visible area.
    *   Example: `sb.cdp.scroll_into_view("footer#copyright")`
*   `sb.cdp.remove_element(selector)` / `sb.cdp.remove_elements(selector)`
    *   Removes element(s) from the DOM.
    *   Example: `sb.cdp.remove_element("div.popup-ad")`

**Waiting:**

*   `sb.cdp.wait_for_element_visible(selector, timeout=None)`
    *   Waits for an element to become visible.
    *   Example: `sb.cdp.wait_for_element_visible("div#results", timeout=10)`
*   `sb.cdp.wait_for_element_absent(selector, timeout=None)`
    *   Waits for an element to be removed from the DOM.
    *   Example: `sb.cdp.wait_for_element_absent("div#loading-spinner")`
*   `sb.cdp.wait_for_text(text, selector="body", timeout=None)`
    *   Waits for specific text to appear.
    *   Example: `sb.cdp.wait_for_text("Welcome back!", "h1.title")`

**Screenshots & PDF:**

*   `sb.cdp.save_screenshot(name, folder=None, selector=None)`
    *   Saves a screenshot of the page or an element.
    *   Example: `sb.cdp.save_screenshot("homepage.png")`
    *   Example: `sb.cdp.save_screenshot("login_form.png", selector="form#login")`
*   `sb.cdp.print_to_pdf(name, folder=None)`
    *   Prints the current page to a PDF file.
    *   Example: `sb.cdp.print_to_pdf("article.pdf")`

**JavaScript & Cookies:**

*   `sb.cdp.evaluate(expression) -> any`
    *   Executes JavaScript and returns the result.
    *   Example: `user_agent = sb.cdp.evaluate("navigator.userAgent")`
*   `sb.cdp.get_all_cookies() -> list[dict]`
    *   Gets all browser cookies.
    *   Example: `cookies = sb.cdp.get_all_cookies()`
*   `sb.cdp.clear_cookies()`
    *   Clears all browser cookies.
    *   Example: `sb.cdp.clear_cookies()`

**GUI Methods (using PyAutoGUI - requires visible browser):**

*   `sb.cdp.gui_click_element(selector)`
    *   Clicks an element using OS-level mouse events. Useful for elements like Turnstile CAPTCHAs if not auto-bypassed.
    *   Example: `sb.cdp.gui_click_element("#turnstile-widget div")` (Use parent selector above #shadow-root)
*   `sb.cdp.gui_press_keys(keys_string)`
    *   Simulates OS-level keyboard presses.
    *   Example: `sb.cdp.gui_press_keys("Hello\\n")`

## 2. Key `element.*` CDP WebElement API Methods

When you find an element using `sb.cdp.find_element()` or iterate through `sb.cdp.find_elements()`, you get CDPWebElement objects. These objects have their own set of methods.

```python
# Example of getting a CDPWebElement
el = sb.cdp.find_element("input#username")
if el:
    # Now use element methods
    el.type("testuser")
    print(el.get_attribute("value"))
```

*   `element.click()`
    *   Clicks the element.
    *   Example: `el.click()`
*   `element.type(text)` / `element.send_keys(text)`
    *   Types text into the element.
    *   Example: `el.type("some value")`
*   `element.press_keys(text)`
    *   Types text with human-like speed.
    *   Example: `el.press_keys("detailed comment.")`
*   `element.clear_input()`
    *   Clears the input value of the element.
    *   Example: `el.clear_input()`
*   `element.focus()`
    *   Sets focus to this element.
    *   Example: `el.focus()`
*   `element.get_attribute(attribute_name) -> str`
    *   Gets an attribute value from this element.
    *   Example: `href = el.get_attribute("href")`
*   `element.get_html() -> str`
    *   Gets the outer HTML of the element.
    *   Example: `html_content = el.get_html()`
*   `element.get_text() -> str` (often available via `element.text` property)
    *   Gets the visible text of the element.
    *   Example: `text = el.text` or `text = el.get_text()`
*   `element.highlight_overlay()` / `element.flash(duration=0.5, color="EE4488")`
    *   Visually highlights this element.
    *   Example: `el.highlight_overlay()`
*   `element.scroll_into_view()`
    *   Scrolls this element into view.
    *   Example: `el.scroll_into_view()`
*   `element.is_visible() -> bool`
    *   Checks if this element is currently visible. (May need to be implemented or might rely on WebDriver's concept if available through CDP object)
    *   Example: `if el.is_visible(): print("Element is visible")`
*   `element.save_screenshot(name, folder=None)`
    *   Saves a screenshot of just this element.
    *   Example: `el.save_screenshot("button_image.png")`
*   `element.query_selector(selector) -> CDPWebElement`
    *   Finds a descendant element using a CSS selector, relative to this element.
    *   Example: `child_el = el.query_selector("span.label")`
*   `element.query_selector_all(selector) -> list[CDPWebElement]`
    *   Finds all descendant elements.
    *   Example: `all_items = el.query_selector_all("li")`

## 3. Summary of Common/Popular `sb.cdp.*` Methods with Examples

This section reiterates some of the most frequently used `sb.cdp` methods with quick examples.

*   **Open URL:**
    `sb.cdp.open("https://example.com")`
*   **Click Element:**
    `sb.cdp.click("button#submit")`
*   **Type into Field:**
    `sb.cdp.type("input[name='search']", "SeleniumBase CDP")`
*   **Get Text from Element:**
    `my_text = sb.cdp.get_text("h1.main-title")`
*   **Get Attribute Value:**
    `image_src = sb.cdp.get_attribute("img#logo", "src")`
*   **Check Element Visibility:**
    `if sb.cdp.is_element_visible("div#confirmation-message"): ...`
*   **Wait for Element to Appear:**
    `sb.cdp.wait_for_element_visible("ul#results-list", timeout=15)`
*   **Wait for Text to Appear:**
    `sb.cdp.wait_for_text("Login Successful", "div.status", timeout=10)`
*   **Execute JavaScript:**
    `title = sb.cdp.evaluate("document.title")`
*   **Take Screenshot:**
    `sb.cdp.save_screenshot("current_view.png")`
*   **Find a single element:**
    `login_button = sb.cdp.find_element("button.login")`
    `if login_button: login_button.click()`
*   **Find multiple elements and iterate:**
    ```python
    items = sb.cdp.find_elements("ul.product-list li")
    for item in items:
        print(item.text) # Accessing .text property of CDPWebElement
        # Or: print(item.get_text())
    ```
*   **Sleep (Pause execution):**
    `sb.cdp.sleep(2.5) # Pauses for 2.5 seconds`

---
This cheat sheet should serve as a helpful starting point and quick lookup for SeleniumBase CDP functionalities. For the exhaustive list and more detailed explanations, always refer to the [official SeleniumBase CDP documentation](https://seleniumbase.io/examples/cdp_mode/ReadMe/).
```

# Using SeleniumBase CDP Mode Within Functions & Classes

Modularizing your web automation code into functions and classes is a best practice for creating maintainable, reusable, and readable scripts. This guide explains how to effectively use SeleniumBase CDP (Chrome DevTools Protocol) Mode when your logic is encapsulated in this way.

## a. Introduction

**Benefits of Modularization:**
*   **Reusability:** Write a CDP interaction sequence once and call it multiple times.
*   **Readability:** Break down complex tasks into smaller, understandable functions.
*   **Maintainability:** Easier to update and debug isolated pieces of logic.

When using SeleniumBase (especially in CDP mode), the key is to correctly pass and manage the `SB` instance (commonly referred to as `sb`).

## b. Core Concept: Passing the `SB` Instance

Just like you might pass a `driver` object in traditional Selenium, with SeleniumBase, you pass the `sb` object (the instance of the `SB` class) to your functions or methods. This `sb` object holds all SeleniumBase functionalities, including `sb.cdp.*` methods after CDP mode is activated.

```python
# Conceptual
def perform_cdp_login(sb_instance, username, password):
    # Assuming CDP mode is active on sb_instance
    sb_instance.cdp.type("#username", username)
    sb_instance.cdp.type("#password", password)
    sb_instance.cdp.click("#login-button")
    # ...
```

## c. Setup Examples (Obtaining and Passing `sb`)

How you obtain the `sb` instance to pass into your functions depends on whether you're using a context manager or managing the browser lifecycle manually.

### i. With Context Manager (Recommended)

The `sb` object is available within the `with` block.

```python
from seleniumbase import SB

def my_custom_cdp_task(sb_param, data_to_use):
    # Ensure CDP mode is active if this function expects it
    # (Best to activate before calling, or function needs to handle activation)
    print(f"Performing CDP task with: {data_to_use}")
    sb_param.cdp.highlight("body") # Example CDP action
    # ... more sb_param.cdp.* calls ...
    return sb_param.cdp.get_title()

# Main script execution
if __name__ == "__main__":
    with SB(uc=True, headless=False) as sb: # uc=True is essential
        sb.open("https://example.com")

        # Best practice: Activate CDP before calling functions that rely on it
        sb.activate_cdp_mode(sb.get_current_url())
        print(f"CDP mode active (WebDriver connected: {sb.is_connected()})")

        page_title = my_custom_cdp_task(sb, "some_data")
        print(f"Page title from function: {page_title}")

        # Another function call
        # another_cdp_function(sb, "other_data")
    # Browser closes automatically here
```

### ii. Without Context Manager (Manual Lifecycle)

You instantiate `SB` directly and are responsible for `sb.driver.quit()`.

```python
from seleniumbase import SB

def extract_product_names_cdp(sb_obj, product_selector):
    # Assumes sb_obj has CDP mode active
    product_elements = sb_obj.cdp.find_elements(product_selector)
    names = [el.text for el in product_elements]
    return names

# Main script execution
if __name__ == "__main__":
    sb_instance = SB(uc=True, headless=False) # uc=True is essential
    try:
        sb_instance.open("https://example.com/products")

        # Activate CDP mode
        sb_instance.activate_cdp_mode(sb_instance.get_current_url())
        print(f"CDP mode active (WebDriver connected: {sb_instance.is_connected()})")

        product_names = extract_product_names_cdp(sb_instance, "div.product-title")
        print("Product Names:", product_names)

        input("Tasks done. Browser open. Press Enter to quit.")
    finally:
        if hasattr(sb_instance, 'driver') and sb_instance.driver:
            sb_instance.driver.quit()
```

## d. Writing Functions with `sb.cdp.*` Methods

### i. Basic Function Structure

```python
def my_cdp_function(sb, param1, param2): # 'sb' is the conventional name
    # Ensure CDP mode is active (see section 'e' for discussion)
    # if not sb.is_connected() is False: # A bit verbose check
    #     print("Warning: CDP mode might not be active for my_cdp_function")

    print(f"Running my_cdp_function with {param1}, {param2}")
    # Use sb.cdp.* methods
    sb.cdp.wait_for_element_visible(param1, timeout=5)
    sb.cdp.click(param1)
    sb.cdp.type(param2, "some text")
    # ...
```

### ii. Example: CDP Click & Wait Function

```python
def click_and_wait_for_next_cdp(sb_instance, click_selector, wait_selector, timeout=10):
    """Clicks an element using CDP and waits for another element to be visible."""
    print(f"CDP Clicking '{click_selector}' and waiting for '{wait_selector}'")
    sb_instance.cdp.click(click_selector)
    sb_instance.cdp.wait_for_element_visible(wait_selector, timeout=timeout)
    print(f"'{wait_selector}' is now visible.")
```

### iii. Example: Data Extraction with `sb.cdp.evaluate()`

```python
def get_js_variable_cdp(sb_instance, js_variable_name):
    """Extracts a global JavaScript variable using CDP."""
    print(f"CDP Evaluating for JS variable: {js_variable_name}")
    script = f"return window.{js_variable_name};"
    try:
        data = sb_instance.cdp.evaluate(script)
        return data
    except Exception as e:
        print(f"Error evaluating '{script}': {e}")
        return None
```

## e. Managing CDP State (`sb.activate_cdp_mode()`) within or before Functions

When and where to call `sb.activate_cdp_mode()` is important.

*   **Best Practice: Activate CDP Mode *Before* Calling Reusable Functions.**
    *   The code that sets up the `sb` instance (e.g., your main script block) should be responsible for opening the initial URL and activating CDP mode.
    *   Reusable functions should then assume the passed `sb` instance is already in the desired state (CDP active, on the correct page).
    *   This makes functions more predictable and focused on their specific task.
    *   **Why?** A function that internally calls `activate_cdp_mode` might have side effects (like navigation if a URL is passed, or disconnecting WebDriver) that the calling code doesn't expect or want at that specific moment.

*   **Alternative (Use with Caution): Function Activates CDP Mode.**
    *   If a function *must* ensure CDP mode is active, it should do so carefully.
    *   **Idempotency:** If called multiple times, `activate_cdp_mode` on an already CDP-active session might be harmless or could potentially re-run parts of its setup.
    *   **Checking State:** A function could check `sb.is_connected()` (which returns `False` if CDP mode has disconnected WebDriver) before attempting activation.
    ```python
    def ensure_cdp_active_and_do_task(sb_instance, target_url_for_cdp):
        if sb_instance.is_connected(): # True if WebDriver is connected
            print("WebDriver is connected. Activating CDP mode now.")
            sb_instance.activate_cdp_mode(target_url_for_cdp)
            # Note: activate_cdp_mode might navigate if URL is different.
            # This could be an issue if the function is called when already on a page.
        elif sb_instance.get_current_url() != target_url_for_cdp:
            # Already in CDP, but maybe wrong page for this function's specific needs
            print(f"CDP active, but navigating to {target_url_for_cdp} for this task.")
            sb_instance.cdp.open(target_url_for_cdp) # Use cdp.open if already in CDP

        # ... perform CDP task ...
        sb_instance.cdp.highlight("h1")
    ```
    This approach adds complexity to the function and makes its behavior less straightforward.

## f. Returning Data from CDP Functions

Functions can return any data extracted using `sb.cdp.*` methods.

```python
def get_all_links_data_cdp(sb_instance):
    """Collects href and text of all 'a' tags using CDP."""
    links_data = []
    link_elements = sb_instance.cdp.find_elements("a")
    for link_el in link_elements:
        href = link_el.get_attribute("href")
        text = link_el.text # Or link_el.get_text()
        if href: # Only include links with an href
            links_data.append({"text": text, "href": href})
    return links_data

# Usage:
# all_links = get_all_links_data_cdp(sb)
# for link_info in all_links:
# print(f"Link Text: {link_info['text']}, URL: {link_info['href']}")
```

## g. Error Handling in CDP Functions

Wrap CDP calls within `try...except` blocks inside your functions to handle potential issues like timeouts, elements not found, or JavaScript errors during `evaluate`.

```python
def safe_cdp_get_text(sb_instance, selector, default_value="N/A"):
    try:
        # sb_instance.cdp.wait_for_element_present(selector, timeout=2) # Optional wait
        return sb_instance.cdp.get_text(selector)
    except Exception as e:
        print(f"Could not get text for selector '{selector}' using CDP: {e}")
        return default_value
```

## h. OOP Approach: Using CDP Mode in Classes

If you're using an Object-Oriented Programming (OOP) approach, you'd typically pass the `sb` instance to your class constructor or a setup method, and store it as an instance variable (e.g., `self.sb`). Methods of the class would then use `self.sb.cdp.*`.

```python
class PageScraper:
    def __init__(self, sb_instance):
        self.sb = sb_instance # Store the SB instance
        # It's generally best to activate CDP mode outside, before creating PageScraper instance,
        # or have an explicit setup_cdp method.

    def setup_cdp_for_page(self, url_to_activate_on):
        """Ensures CDP is active for the given URL context."""
        if self.sb.is_connected() or self.sb.get_current_url() != url_to_activate_on:
            # This logic might need refinement: what if already CDP on wrong page?
            print(f"Activating CDP mode for {url_to_activate_on} in PageScraper.")
            self.sb.activate_cdp_mode(url_to_activate_on)
        print(f"CDP mode active for PageScraper (WebDriver connected: {self.sb.is_connected()})")


    def extract_titles_cdp(self):
        # Assumes CDP is active
        if self.sb.is_connected(): # Check if not in CDP mode
             print("Error: CDP mode not active for extract_titles_cdp. Call setup_cdp_for_page first.")
             return []

        title_elements = self.sb.cdp.find_elements("h2.article-title")
        return [el.text for el in title_elements]

    def click_load_more_cdp(self, button_selector):
        # Assumes CDP is active
        try:
            self.sb.cdp.click(button_selector)
            self.sb.cdp.sleep(1.5) # Wait for content
            return True
        except Exception as e:
            print(f"Error clicking load more button '{button_selector}' with CDP: {e}")
            return False

# Usage with a class:
# with SB(uc=True) as sb_main:
#     sb_main.open("https://example.com/articles")
#     # Activate CDP before passing sb_main to the class instance
#     sb_main.activate_cdp_mode(sb_main.get_current_url())
#
#     scraper = PageScraper(sb_main)
#     # Alternatively, if scraper.setup_cdp_for_page handles it:
#     # scraper.setup_cdp_for_page(sb_main.get_current_url())

#     titles = scraper.extract_titles_cdp()
# print("Article Titles:", titles)
```

## i. Important Considerations

*   **Function Preconditions:** Be clear in your function's documentation (docstrings) about the expected state of the `sb` instance (e.g., "Assumes CDP mode is already active and on the target page").
*   **Side Effects:** Functions that modify global browser state (e.g., changing user agent via `sb.cdp.set_user_agent()`, clearing cookies with `sb.cdp.clear_cookies()`) should clearly document these side effects, or such actions should be managed at a higher level.
*   **Page Context:** Remember that CDP commands are executed in the context of the browser's current page. If your function needs to operate on a specific page, ensure the browser is navigated there *before* the function's CDP logic runs.
*   **Error Propagation:** Decide if your functions should handle errors internally (and return a default value or status) or let exceptions propagate to the caller.

By passing the `sb` instance and managing CDP activation thoughtfully, you can build robust and well-structured SeleniumBase CDP automation scripts.
```

The file `seleniumbase_cdp_in_functions.md` has been created with the initial structure and content covering the planned sections.

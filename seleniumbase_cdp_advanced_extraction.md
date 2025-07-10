# Advanced Content Extraction with SeleniumBase CDP Mode

This guide explores advanced techniques using SeleniumBase CDP (Chrome DevTools Protocol) Mode to extract content that may be hidden, dynamically generated, embedded in JavaScript, or otherwise difficult to access through standard DOM scraping methods.

## a. Introduction

Websites increasingly use complex JavaScript, Shadow DOM, and dynamic loading, making some content challenging to extract. SeleniumBase's CDP Mode, by allowing direct communication with the browser via the Chrome DevTools Protocol, offers powerful ways to access this "hidden" data. This guide focuses on these advanced CDP techniques.

## b. Core Prerequisites & Setup (CDP Mode)

1.  **UC Mode is Essential:** CDP Mode in SeleniumBase is an extension of Undetected-Chromedriver (UC) Mode.
    *   Always initialize `SB` with `uc=True`.

2.  **Debugging Visibility:**
    *   When developing and debugging these advanced scripts, it's highly recommended to run with `headless=False` (or `headless2=True` with `test=True` for headed execution in newer SeleniumBase versions with Chrome > 109) to observe browser behavior.
    *   Example: `sb = SB(uc=True, headless=False)`

3.  **Activate CDP Mode:**
    *   Call `sb.activate_cdp_mode(url)` after your initial navigation to the target page and *before* you intend to use `sb.cdp.*` methods for extraction. This disconnects WebDriver and enables the CDP driver.

**Setup Examples:**

*   **With Context Manager (Recommended for most scripts):**
    ```python
    from seleniumbase import SB

    with SB(uc=True, headless=False) as sb: # Or headless2=True for headed
        sb.open("https://target-website.com/data-page")
        # Any initial interactions like cookie banners if needed
        sb.activate_cdp_mode(sb.get_current_url())
        # ... Your advanced CDP extraction logic here ...
    ```

*   **Without Context Manager (Manual Browser Lifecycle):**
    ```python
    from seleniumbase import SB

    sb = SB(uc=True, headless=False) # Or headless2=True for headed
    try:
        sb.open("https://target-website.com/data-page")
        sb.activate_cdp_mode(sb.get_current_url())
        # ... Your advanced CDP extraction logic here ...
        input("Browser open for inspection. Press Enter to quit.")
    finally:
        if hasattr(sb, 'driver') and sb.driver:
            sb.driver.quit()
    ```

## c. Advanced Extraction Techniques (CDP Mode Examples)

Always ensure CDP mode is active (`sb.activate_cdp_mode()`) before using these.

### i. Accessing JavaScript Variables / Global Data Stores

Often, websites load data into global JavaScript variables or objects (e.g., `window.INITIAL_STATE`, `window.__DATA__`). CDP's `evaluate` method can directly access these.

```python
# Assumes 'sb' is initialized and CDP mode is active on the target page
try:
    # Example 1: Accessing a global variable
    initial_data_script = "return window.INITIAL_STATE;" # Or whatever the variable is
    data = sb.cdp.evaluate(initial_data_script)
    if data:
        print("Successfully extracted INITIAL_STATE data:", data)
        # Process the 'data' (often a dictionary or list)
    else:
        print("window.INITIAL_STATE not found or empty.")

    # Example 2: Accessing a property of a global object
    user_id_script = "return window.appData.user.id;"
    user_id = sb.cdp.evaluate(user_id_script)
    if user_id:
        print(f"Extracted User ID: {user_id}")

except Exception as e:
    print(f"Error evaluating JS for global data: {e}")
```

### ii. Extracting Content from Complex/Deep Shadow DOM

While basic CSS selectors with `sb.cdp.find_element()` can pierce the first level of Shadow DOM, deeply nested or complex Shadow DOM structures might require JavaScript execution.

```python
# Assumes 'sb' and CDP mode active
# Target: <host-element> #shadow-root -> <nested-host> #shadow-root -> <target-p>Hello</target-p>
shadow_host_selector = "host-element"
nested_host_selector_in_shadow1 = "nested-host"
target_paragraph_selector_in_shadow2 = "target-p"

# Using sb.cdp.evaluate() with a JS path
script = f"""
(() => {{
    const host = document.querySelector('{shadow_host_selector}');
    if (!host || !host.shadowRoot) return null;
    const nestedHost = host.shadowRoot.querySelector('{nested_host_selector_in_shadow1}');
    if (!nestedHost || !nestedHost.shadowRoot) return null;
    const targetElement = nestedHost.shadowRoot.querySelector('{target_paragraph_selector_in_shadow2}');
    return targetElement ? targetElement.textContent : null;
}})()
"""
try:
    hidden_text = sb.cdp.evaluate(script)
    if hidden_text:
        print(f"Text from deep Shadow DOM: {hidden_text}")
    else:
        print("Target element in deep Shadow DOM not found or no text.")
except Exception as e:
    print(f"Error evaluating JS for Shadow DOM: {e}")

# Note: SeleniumBase's standard finders with ::shadow or >>> might also work for some cases
# even in CDP mode if they internally use similar JS execution. Test them first.
# Example: self.get_text("host-element::shadow nested-host::shadow target-p")
# The sb.cdp.evaluate method gives you explicit control.
```

### iii. Handling Content Loaded by Non-Scroll JS Triggers (e.g., XHR/Fetch)

Content might load after clicking a button, which triggers an XHR/Fetch request, and then updates the DOM.

```python
# Assumes 'sb' and CDP mode active
button_selector = "button#load-data-button"
data_container_selector = "div#data-container p"

print("Clicking button to load data...")
sb.cdp.click(button_selector)

# Strategy 1: Wait for a specific element to appear/update
# This is often the simplest if a clear indicator element exists.
try:
    sb.cdp.wait_for_element_visible(data_container_selector, timeout=15)
    loaded_data_elements = sb.cdp.find_elements(data_container_selector)
    for el in loaded_data_elements:
        print(f"Loaded data item: {el.text}")
except Exception as e:
    print(f"Data did not appear after click: {e}")

# Strategy 2 (More Advanced): Listen for network responses (conceptual for cheat sheet)
# This requires setting up handlers *before* the click.
# Example:
# def log_response(params):
# if "myapi/data" in params.get("response", {}).get("url", ""):
# print("Relevant API response received:", params.get("response"))
# sb.cdp.add_handler("Network.responseReceived", log_response)
# sb.cdp.click(button_selector)
# sb.cdp.sleep(5) # Allow time for API call and DOM update
# sb.cdp.remove_handler("Network.responseReceived", log_response)
# Then extract based on DOM update or data from response if captured.
# For this cheat sheet, focus on DOM changes after action.
```

### iv. Extracting Data from `<script>` Tags (JSON-LD, Initial State)

Websites often embed structured data (JSON-LD for SEO) or initial application state within `<script>` tags.

```python
# Assumes 'sb' and CDP mode active
import json
import re

# Example 1: Extracting JSON-LD
json_ld_data = []
try:
    script_elements = sb.cdp.find_elements("script[type='application/ld+json']")
    for script_el in script_elements:
        try:
            # Get the text content of the script element
            script_content = script_el.get_text() # Or .get_html() and then parse
            if script_content:
                data = json.loads(script_content)
                json_ld_data.append(data)
        except json.JSONDecodeError as je:
            print(f"Could not parse JSON from a script tag: {je}")
        except Exception as ex:
            print(f"Error processing script tag: {ex}")
    if json_ld_data:
        print("Extracted JSON-LD data:", json_ld_data)
    else:
        print("No JSON-LD script tags found or data extracted.")

except Exception as e:
    print(f"Error finding JSON-LD script tags: {e}")


# Example 2: Extracting JavaScript variable from a script tag (e.g. initial state)
# This is more complex as it requires parsing JS, regex might be a simpler approach for known patterns.
try:
    page_source = sb.cdp.get_page_source()
    # Use regex to find something like: window.INITIAL_DATA = {...};
    match = re.search(r"window\.INITIAL_DATA\s*=\s*(\{.*?\});", page_source, re.DOTALL)
    if match:
        initial_data_str = match.group(1)
        try:
            initial_data_json = json.loads(initial_data_str)
            print("Extracted INITIAL_DATA via regex and JSON parse:", initial_data_json)
        except json.JSONDecodeError as je:
            print(f"Regex found data, but failed to parse as JSON: {je}")
    else:
        print("window.INITIAL_DATA pattern not found in page source via regex.")
except Exception as e:
    print(f"Error extracting from script tag via page source: {e}")
```

### v. Getting Non-Visible Element Properties/Attributes via JS

Sometimes, data is stored as JavaScript properties of DOM elements, not as visible text or standard HTML attributes.

```python
# Assumes 'sb' and CDP mode active
element_selector = "div#user-profile"

# Example: Get a custom JS property 'element._customData'
script = f"""
(() => {{
    const el = document.querySelector('{element_selector}');
    return el ? el._customData : null;
}})()
"""
try:
    custom_data = sb.cdp.evaluate(script)
    if custom_data:
        print(f"Custom JS property data: {custom_data}")
    else:
        print("Element or custom property not found.")
except Exception as e:
    print(f"Error evaluating JS for custom property: {e}")

# Example: Get an attribute that might be set dynamically by JS
dynamic_attr_script = f"document.querySelector('{element_selector}').getAttribute('data-dynamic-id');"
try:
    attr_value = sb.cdp.evaluate(dynamic_attr_script)
    if attr_value:
        print(f"Dynamically set attribute value: {attr_value}")
except Exception as e:
    print(f"Error evaluating JS for dynamic attribute: {e}")
```

### vi. Strategies for DOMs Manipulated by Anti-Scraping Measures

Some sites alter the DOM when they detect developer tools or script-like interactions.
CDP mode, being disconnected from WebDriver's typical tells, can sometimes bypass these.

*   **Rapid snapshot:** Get page source or specific data quickly after an action before potential manipulation.
    ```python
    sb.cdp.click("#trigger-action")
    # Immediately get source or evaluate, before any potential anti-scraping JS runs
    quick_source = sb.cdp.get_page_source()
    # Or: quick_data = sb.cdp.evaluate("document.querySelector('#data').innerText")
    sb.cdp.sleep(0.1) # Minimal pause
    # Compare with later source/data if needed
    ```
*   **Disable JavaScript (Extreme):** If data is present in initial HTML but hidden/altered by JS.
    *   `sb.cdp.set_javascript_disabled(disabled=True)`
    *   Then `sb.cdp.reload()` or `sb.cdp.open()` the page. Extract data.
    *   Then `sb.cdp.set_javascript_disabled(disabled=False)` to re-enable.
    *   **Caution:** This will break most modern websites. Use very selectively.

### vii. (Briefly) Using CDP Event Listeners for Timely Capture

For highly dynamic content, you might need to listen to specific browser events. This is advanced.
`sb.cdp.add_handler(event_name, callback_function)` allows you to react to events like:
*   `DOM.documentUpdated`: When the overall DOM structure changes.
*   `DOM.subtreeModified`: When a part of the DOM tree under a specific node changes.
*   `Runtime.consoleAPICalled`: To capture console log messages.
*   `Network.responseReceived`: To inspect network responses.

```python
# Conceptual example for listening to console logs
# def my_console_listener(params):
#     log_entry = params.get('entry', {})
#     print(f"Browser Console ({log_entry.get('level')}): {log_entry.get('text')}")

# sb.cdp.add_handler("Log.entryAdded", my_console_listener) # Requires Log domain enabled
# sb.cdp.evaluate("console.warn('Hello from CDP test!')")
# sb.cdp.sleep(0.5)
# sb.cdp.remove_handler("Log.entryAdded", my_console_listener)
```
**Note:** Managing handlers and ensuring domains are enabled can be complex. Refer to SeleniumBase/CDP documentation for specifics if you need this level of control.

## d. Important Considerations

*   **Complexity:** These techniques are inherently more complex than standard scraping.
*   **Site-Specificity:** Solutions are often tightly coupled to the target website's structure and JavaScript implementation. They can break easily if the site changes.
*   **Performance:** Extensive JavaScript evaluation or event listening can impact performance.
*   **Debugging:** Debugging scripts that use these advanced methods can be more challenging. Use `headless=False` and browser devtools extensively.
*   **Ethical and Legal:** Always respect `robots.txt`, website Terms of Service, and relevant laws. Do not overload servers. Be mindful of privacy when handling user data.

This guide provides a starting point for tackling advanced data extraction scenarios with SeleniumBase CDP Mode. Experimentation and careful inspection of the target website's behavior are key to success.
```

The file `seleniumbase_cdp_advanced_extraction.md` has been created with the initial structure and content covering the planned sections.

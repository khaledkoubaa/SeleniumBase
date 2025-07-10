# SeleniumBase CDP Mode - Cheat Sheet

This cheat sheet provides a quick reference to common methods and examples for using SeleniumBase in CDP (Chrome DevTools Protocol) Mode. Remember to activate CDP mode first within a UC Mode test:

```python
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.open("https://www.example.com") # Navigate first
    sb.activate_cdp_mode(sb.get_current_url()) # Then activate CDP for the current page
    # Now use sb.cdp methods
    # ...
```

Or, for manual browser lifecycle:
```python
# sb = SB(uc=True)
# sb.open("https://www.example.com") # Optional: open initial page with WebDriver
# sb.activate_cdp_mode(sb.get_current_url()) # Or pass a new URL
# ...
# sb.driver.quit() # eventually
```
**Important:** Always call `sb.activate_cdp_mode()` after `sb.open()` or navigating to the page where you intend to use `sb.cdp.*` methods.

## 1. Key `sb.cdp.*` API Methods (Browser-Level)

This section covers general browser control and interaction methods available via `sb.cdp`.

**Navigation & Page Info:**
(Examples from previous version are good and retained)
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
(Examples from previous version are good and retained)
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
(Examples from previous version are good and retained, with minor additions)
*   `sb.cdp.click(selector, timeout=None)`
    *   Clicks an element.
    *   Example: `sb.cdp.click("a#login-link")`
*   `sb.cdp.type(selector, text, timeout=None)`
    *   Types text into an element. (Also `sb.cdp.send_keys()`)
    *   Example: `sb.cdp.type("input#email", "user@example.com")`
*   `sb.cdp.press_keys(selector, text, timeout=None)`
    *   Types text with human-like speed.
    *   Example: `sb.cdp.press_keys("textarea#comment", "Hello world!\\n")` # \\n for enter
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
*   `sb.cdp.scroll_to_top()` / `sb.cdp.scroll_to_bottom()`
    *   Scrolls page to top or bottom.
    *   Example: `sb.cdp.scroll_to_bottom()`
*   `sb.cdp.remove_element(selector)` / `sb.cdp.remove_elements(selector)`
    *   Removes element(s) from the DOM.
    *   Example: `sb.cdp.remove_element("div.popup-ad")`

**Waiting:**
(Examples from previous version are good and retained)
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
(Examples from previous version are good and retained)
*   `sb.cdp.save_screenshot(name, folder=None, selector=None)`
    *   Saves a screenshot of the page or an element.
    *   Example: `sb.cdp.save_screenshot("homepage.png")`
*   `sb.cdp.print_to_pdf(name, folder=None)`
    *   Prints the current page to a PDF file.
    *   Example: `sb.cdp.print_to_pdf("article.pdf")`

**JavaScript & Cookies:**
(Examples from previous version are good and retained, `evaluate` will be expanded later)
*   `sb.cdp.evaluate(expression) -> any`
    *   Executes JavaScript and returns the result.
    *   Example: `user_agent = sb.cdp.evaluate("navigator.userAgent")`
*   `sb.cdp.get_all_cookies() -> list[dict]` / `sb.cdp.add_cookie(cookie_dict)` / `sb.cdp.delete_cookie(name)`
    *   Manage browser cookies.
    *   Example: `cookies = sb.cdp.get_all_cookies()`
*   `sb.cdp.clear_cookies()`
    *   Clears all browser cookies.
    *   Example: `sb.cdp.clear_cookies()`

**GUI Methods (using PyAutoGUI - requires visible browser):**
(Examples from previous version are good and retained)
*   `sb.cdp.gui_click_element(selector)`
    *   Clicks an element using OS-level mouse events.
    *   Example: `sb.cdp.gui_click_element("#turnstile-widget div")`
*   `sb.cdp.gui_press_keys(keys_string)`
    *   Simulates OS-level keyboard presses.
    *   Example: `sb.cdp.gui_press_keys("Hello\\n")`

## 2. Key `element.*` CDP WebElement API Methods
(Content from previous version largely retained, `send_file` added here as it belongs to element)

When you find an element using `sb.cdp.find_element()` or iterate through `sb.cdp.find_elements()`, you get `CDPWebElement` objects.

```python
el = sb.cdp.find_element("input#username")
if el:
    el.type("testuser")
    print(el.get_attribute("value"))
```
*   `element.click()`
*   `element.type(text)` / `element.send_keys(text)`
*   `element.press_keys(text)` (human-speed typing)
*   `element.clear_input()`
*   `element.focus()`
*   `element.get_attribute(attribute_name) -> str`
*   `element.get_html() -> str` (outer HTML)
*   `element.get_text() -> str` (or `element.text` property)
*   `element.highlight_overlay()` / `element.flash(...)`
*   `element.scroll_into_view()`
*   `element.save_screenshot(name, folder=None)`
*   `element.query_selector(selector) -> CDPWebElement` (find descendant)
*   `element.query_selector_all(selector) -> list[CDPWebElement]` (find descendants)
*   `element.send_file(*file_paths)`
    *   Uploads file(s) to an `<input type="file">` element.
    *   Example: `file_input_el = sb.cdp.find_element("input[type='file']"); file_input_el.send_file("my_document.pdf")`

## 3. Handling JavaScript Dialogs (Alerts, Confirms, Prompts)

CDP mode can handle JavaScript dialogs like alerts, confirms, and prompts. SeleniumBase provides wrappers.

*   **Accepting a dialog (alert, confirm, or prompt with default value):**
    ```python
    # sb.cdp.click("#trigger-alert-button") # Action that triggers the dialog
    # Need to handle dialogs proactively or use try-except for unexpected ones.
    # SeleniumBase's CDP implementation might auto-accept alerts/confirms by default
    # or require explicit handling setup if not.
    # If a dialog appears and is not handled, script might hang.
    # For explicit handling:
    try:
        # Trigger action that might open a dialog
        sb.cdp.click("#trigger-alert-button")
        # If you expect a dialog and want to ensure it's handled:
        # This part depends on SeleniumBase's specific CDP wrappers for dialogs.
        # The raw CDP commands are Page.handleJavaScriptDialog.
        # SeleniumBase offers:
        sb.cdp.accept_dialog()
        print("Dialog accepted.")
    except Exception as e:
        print(f"Dialog handling error or no dialog: {e}")
    ```
*   **Dismissing a dialog (confirm or prompt):**
    ```python
    # sb.cdp.click("#trigger-confirm-button")
    try:
        sb.cdp.dismiss_dialog()
        print("Dialog dismissed.")
    except Exception as e:
        print(f"Dialog handling error or no dialog: {e}")
    ```
*   **Handling a prompt (accepting with custom text):**
    ```python
    # sb.cdp.click("#trigger-prompt-button")
    try:
        # To accept a prompt with specific text:
        sb.cdp.accept_dialog(prompt_text="My custom input")
        print("Prompt accepted with text.")
    except Exception as e:
        print(f"Dialog handling error or no dialog: {e}")
    ```
*   **Getting Dialog Message:** SeleniumBase's `sb.cdp.accept_dialog()` / `sb.cdp.dismiss_dialog()` don't directly return the message. To get the message, you'd typically need to set up an event handler for `Page.javascriptDialogOpening` *before* the dialog is triggered, which is more advanced. For a cheat sheet, knowing accept/dismiss is key.
    ```python
    # Advanced: Listening for dialog message (conceptual)
    # dialog_message = None
    # def handle_dialog(params):
    #     nonlocal dialog_message
    #     dialog_message = params.get('message')
    #     print(f"Dialog opened with message: {dialog_message}, type: {params.get('type')}")
    #     # To auto-accept: sb.driver.execute_cdp_cmd('Page.handleJavaScriptDialog', {'accept': True})
    # sb.cdp.add_handler("Page.javascriptDialogOpening", handle_dialog)
    # sb.cdp.click("#trigger-alert-button") # Trigger dialog
    # sb.cdp.sleep(0.5) # Allow event to fire
    # print(f"Captured dialog message: {dialog_message}")
    # sb.cdp.remove_handler("Page.javascriptDialogOpening", handle_dialog) # Clean up
    ```
    **Note:** Simpler alert/confirm handling is often managed by UC Mode's default behaviors or direct CDP commands if SeleniumBase wrappers are used as shown.

## 4. Emulation (Geolocation, User Agent, Device Metrics, Network)

CDP allows various emulations.

*   **Set Geolocation Override:**
    ```python
    sb.cdp.set_geolocation_override(latitude=37.7749, longitude=-122.4194, accuracy=100)
    sb.cdp.open("https://maps.google.com") # Page will think you're at this location
    ```
*   **Set User Agent:**
    ```python
    new_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
    sb.cdp.set_user_agent(new_user_agent)
    sb.cdp.open("https://www.whatsmyua.info") # Verify new UA
    ```
*   **Set Device Metrics (for responsive testing):**
    ```python
    # Emulate an iPhone X
    sb.cdp.set_device_metrics(width=375, height=812, device_scale_factor=3, mobile=True)
    sb.cdp.open("https://www.example.com") # Page should render as on iPhone X
    ```
*   **Set Network Conditions (emulate slow network, offline):**
    ```python
    # Emulate slow 3G
    sb.cdp.set_network_conditions(
        offline=False,
        latency=400,  # ms
        download_throughput=750 * 1024 / 8,  # B/s (750 kbps)
        upload_throughput=250 * 1024 / 8    # B/s (250 kbps)
    )
    sb.cdp.open("https://fast.com")
    sb.cdp.set_network_conditions() # Reset to default (online, no throttling)
    ```

## 5. File Uploads in CDP Mode

For `<input type="file">` elements.

*   **Using `CDPWebElement.send_file()`:**
    ```python
    file_input_selector = "input#file-upload"
    # Ensure the file input is not hidden by CSS (opacity:0, visibility:hidden)
    # If it's hidden, you might need JS to make it interactable first, e.g.:
    # sb.cdp.evaluate(f"document.querySelector('{file_input_selector}').style.display='block';")
    # sb.cdp.evaluate(f"document.querySelector('{file_input_selector}').style.opacity=1;")

    file_input_el = sb.cdp.find_element(file_input_selector)
    if file_input_el:
        file_path = "./my_image.png" # Path relative to script or absolute
        # Create a dummy file for testing if needed: open(file_path, 'w').write("test")
        file_input_el.send_file(file_path)
        # For multiple files: file_input_el.send_file(path1, path2)
        sb.cdp.sleep(1) # Allow upload processing
        print("File likely selected for upload.")
    else:
        print("File input element not found.")
    ```
    **Note:** The element must be present in the DOM. Some sites use custom upload buttons that hide the actual file input; you'll need to target the hidden input.

## 6. Advanced Interactions with `sb.cdp.evaluate()`

`sb.cdp.evaluate(expression)` executes JavaScript in the page context.

*   **Get Computed Style:**
    ```python
    color = sb.cdp.evaluate("window.getComputedStyle(document.querySelector('h1')).color;")
    print(f"H1 color: {color}")
    ```
*   **Trigger Custom Event:**
    ```python
    sb.cdp.evaluate("document.querySelector('#myButton').dispatchEvent(new Event('myCustomEvent'));")
    ```
*   **Pass Arguments and Return Complex Data:**
    ```python
    js_code = """
    (selector, newText) => {
        const el = document.querySelector(selector);
        if (el) {
            el.innerText = newText;
            return { success: true, oldText: el.dataset.old || '' };
        }
        return { success: false };
    }
    """
    # To pass arguments to evaluate, you need to format them into the script string
    # or use a more complex execute_cdp_cmd structure for Runtime.callFunctionOn
    # SeleniumBase's sb.cdp.evaluate might simplify this, or you might need sb.execute_script
    # For sb.cdp.evaluate, you typically build the full script string:
    selector = "#myDiv"
    new_text = "Updated by CDP!"
    result = sb.cdp.evaluate(f"(() => {{ const el = document.querySelector('{selector}'); if (el) {{ el.innerText = '{new_text}'; return true; }} return false; }})()")
    print(f"JS execution result: {result}")
    ```
    **Note:** For passing complex arguments or calling functions with specific `this` context, `sb.execute_script(script, arg1, ...)` (which works even in CDP mode if WebDriver isn't fully disconnected or if it uses CDP backend) or raw `sb.driver.execute_cdp_cmd('Runtime.callFunctionOn', {...})` might be more flexible than simple `sb.cdp.evaluate()`. `sb.cdp.evaluate` is best for simple expressions.

## 7. Debugging Tips for CDP Mode

*   **Ensure CDP Mode is Active:** After `sb.activate_cdp_mode()`, `sb.is_connected()` should return `False` (indicating WebDriver is disconnected).
*   **Use `sb.cdp.sleep(seconds)`:** Introduce pauses to observe behavior, especially if things happen too fast or if waiting for asynchronous operations.
*   **`sb.cdp.highlight(selector)`:** Visually confirm you're targeting the correct elements.
*   **Check Browser Console:** Manually inspect the browser's developer console for errors if `headless=False`. For programmatic access (advanced):
    ```python
    # def log_console_message(params):
    #     print(f"CONSOLE: {params['message']['level']} - {params['message']['text']}")
    # sb.cdp.add_handler("Log.entryAdded", log_console_message)
    # # ... then later sb.cdp.remove_handler(...)
    ```
*   **Verbose CDP Logging (via SeleniumBase options):**
    If you run tests with `pytest --pdb --verbose_cdp`, SeleniumBase logs CDP events.
*   **Incremental Development:** Build and test CDP interactions step-by-step.
*   **Selector Issues:** If `sb.cdp.find_element` returns `None` or times out, your selector is likely incorrect or the element isn't present/visible when searched. Test selectors in the browser's devtools console (`document.querySelector(...)`).

## 8. Summary of Common/Popular `sb.cdp.*` Methods with Examples
(This section was good, largely retained)
*   **Open URL:** `sb.cdp.open("https://example.com")`
*   **Click Element:** `sb.cdp.click("button#submit")`
*   **Type into Field:** `sb.cdp.type("input[name='search']", "SeleniumBase CDP")`
*   **Get Text from Element:** `my_text = sb.cdp.get_text("h1.main-title")`
*   **Check Element Visibility:** `if sb.cdp.is_element_visible("div#confirmation"): ...`
*   **Wait for Element:** `sb.cdp.wait_for_element_visible("ul#results", timeout=10)`
*   **Execute JavaScript:** `title = sb.cdp.evaluate("document.title")`
*   **Take Screenshot:** `sb.cdp.save_screenshot("view.png")`
*   **Find element & interact (CDPWebElement):**
    ```python
    el = sb.cdp.find_element("button.login")
    if el: el.click()
    ```
*   **Sleep:** `sb.cdp.sleep(1.5)`

---
This cheat sheet covers many common CDP functionalities. For exhaustive details, refer to the [official SeleniumBase CDP documentation](https://seleniumbase.io/examples/cdp_mode/ReadMe/).
```

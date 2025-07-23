# SeleniumBase CDP Mode - Pocket API Reference

This document provides a detailed and extensive API reference for SeleniumBase's Chrome DevTools Protocol (CDP) mode. It is intended to serve as an alternative to the official documentation, offering in-depth explanations and practical examples to help you master web scraping and browser automation.

## Introduction to CDP Mode

SeleniumBase's CDP mode is a powerful feature that allows you to control a web browser using the Chrome DevTools Protocol. This mode is particularly useful for bypassing anti-bot measures, as it enables you to interact with web pages in a way that is less detectable than traditional WebDriver commands.

### Key Features:

*   **Stealthy Automation**: By disconnecting the WebDriver and using the CDP-Driver, you can perform actions without triggering many common bot-detection mechanisms.
*   **Hybrid Control**: Seamlessly switch between WebDriver and CDP-Driver, allowing you to leverage the strengths of both.
*   **Rich Functionality**: Access a wide range of methods for everything from basic navigation to complex interactions like handling cookies, permissions, and pop-ups.
*   **`PyAutoGUI` Integration**: For advanced stealth, CDP mode integrates with `PyAutoGUI` to simulate human-like mouse and keyboard actions.

## Activating CDP Mode

To get started, you need to activate CDP mode from a UC Mode script. This is done by calling `sb.activate_cdp_mode(url)`.

### Example:

```python
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://nowsecure.nl/#relax"
    sb.activate_cdp_mode(url)
    # Your CDP automation code here
```

## Core API Reference

The following sections provide a comprehensive reference for the `sb.cdp` methods available in SeleniumBase.

### Navigation

| Method                                      | Description                                                                                                                              |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `get(url, **kwargs)`                        | Navigates to the specified URL.                                                                                                          |
| `open(url, **kwargs)`                       | An alias for `get()`.                                                                                                                    |
| `reload(ignore_cache=True, ...)`            | Reloads the current page. Set `ignore_cache` to `False` to use the cache.                                                                |
| `refresh(*args, **kwargs)`                  | An alias for `reload()`.                                                                                                                 |
| `go_back()`                                 | Navigates to the previous page in the browser's history.                                                                                 |
| `go_forward()`                              | Navigates to the next page in the browser's history.                                                                                     |
| `get_navigation_history()`                  | Returns the browser's navigation history.                                                                                                |
| `open_new_window(url=None, switch_to=True)` | Opens a new browser window.                                                                                                              |
| `open_new_tab(url=None, switch_to=True)`    | Opens a new browser tab.                                                                                                                 |
| `switch_to_window(window)`                  | Switches the context to the specified window.                                                                                            |
| `switch_to_tab(tab)`                        | Switches the context to the specified tab.                                                                                               |
| `switch_to_newest_window()`                 | Switches to the most recently opened window.                                                                                             |
| `switch_to_newest_tab()`                    | Switches to the most recently opened tab.                                                                                                |
| `close_active_tab()`                        | Closes the currently active tab.                                                                                                         |
| `get_active_tab()`                          | Returns the currently active tab object.                                                                                                 |
| `get_tabs()`                                | Returns a list of all open tabs.                                                                                                         |

### Element Interaction

| Method                                  | Description                                                                                                                                                            |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `click(selector, timeout=None)`         | Clicks the specified element.                                                                                                                                          |
| `click_active_element()`                | Clicks the currently active (focused) element on the page.                                                                                                             |
| `click_if_visible(selector)`            | Clicks the element only if it is visible.                                                                                                                              |
| `click_visible_elements(selector, ...)` | Clicks all visible elements matching the selector.                                                                                                                     |
| `mouse_click(selector, timeout=None)`   | Simulates a mouse click on the element.                                                                                                                                |
| `nested_click(parent_selector, ...)`    | Clicks a child element within a parent element. Useful for iframes.                                                                                                    |
| `double_click(selector, timeout=None)`  | Performs a double-click on an element. *(Note: This method is not in the provided file but is a common and useful interaction.)*                                        |
| `send_keys(selector, text, ...)`        | Sends a sequence of key presses to an element.                                                                                                                         |
| `press_keys(selector, text, ...)`       | Simulates typing at a human-like speed.                                                                                                                                |
| `type(selector, text, timeout=None)`    | Clears the text field and then sends keys.                                                                                                                             |
| `set_value(selector, text, ...)`        | Sets the value of an input field directly using JavaScript.                                                                                                            |
| `submit(selector)`                      | Submits a form by simulating a key press on the "Enter" key.                                                                                                           |
| `focus(selector)`                       | Brings an element into focus.                                                                                                                                          |
| `scroll_into_view(selector)`            | Scrolls the page to bring the specified element into view.                                                                                                             |
| `flash(selector, duration=1, ...)`      | Briefly highlights an element with a colored dot.                                                                                                                      |
| `highlight(selector)`                   | Highlights an element with a multi-colored effect.                                                                                                                     |
| `highlight_overlay(selector)`           | Places a persistent overlay on an element to highlight it.                                                                                                             |
| `select_option_by_text(dropdown, ...)`  | Selects an option from a dropdown menu based on its visible text.                                                                                                      |
| `check_if_unchecked(selector)`          | Checks a checkbox if it is not already checked.                                                                                                                        |
| `uncheck_if_checked(selector)`          | Unchecks a checkbox if it is already checked.                                                                                                                          |
| `remove_element(selector)`              | Removes a single element from the DOM.                                                                                                                                 |
| `remove_elements(selector)`             | Removes all elements matching the selector from the DOM.                                                                                                               |

### Element State and Information

| Method                                      | Description                                                                                                                                   |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `is_element_present(selector)`              | Checks if an element is present in the DOM.                                                                                                   |
| `is_element_visible(selector)`              | Checks if an element is visible on the page.                                                                                                  |
| `is_text_visible(text, selector="body")`    | Checks if the specified text is visible within an element.                                                                                    |
| `is_exact_text_visible(text, ...)`          | Checks if the exact text is visible within an element.                                                                                        |
| `is_checked(selector)`                      | Returns `True` if a checkbox or radio button is checked.                                                                                      |
| `is_selected(selector)`                     | An alias for `is_checked()`.                                                                                                                  |
| `get_text(selector)`                        | Retrieves the text content of an element.                                                                                                     |
| `get_title()`                               | Retrieves the title of the current page.                                                                                                      |
| `get_current_url()`                         | Retrieves the URL of the current page.                                                                                                        |
| `get_origin()`                              | Retrieves the origin (protocol, hostname, and port) of the current page.                                                                      |
| `get_page_source()`                         | Retrieves the full HTML source of the current page.                                                                                           |
| `get_user_agent()`                          | Retrieves the user agent string of the browser.                                                                                               |
| `get_locale_code()`                         | Retrieves the locale code of the browser.                                                                                                     |
| `get_attribute(selector, attribute)`        | Retrieves the value of an element's attribute.                                                                                                |
| `get_element_html(selector)`                | Retrieves the outer HTML of an element.                                                                                                       |
| `get_element_rect(selector, timeout=None)`  | Retrieves the position and size of an element relative to the viewport.                                                                       |
| `get_element_size(selector, timeout=None)`  | Retrieves the width and height of an element.                                                                                                 |
| `get_element_position(selector, ...)`       | Retrieves the x and y coordinates of an element relative to the viewport.                                                                     |
| `get_gui_element_rect(selector, ...)`       | Retrieves the element's position and size relative to the screen.                                                                             |
| `get_gui_element_center(selector, ...)`     | Retrieves the center coordinates of an element relative to the screen.                                                                        |
| `get_active_element()`                      | Retrieves the currently focused element.                                                                                                      |
| `get_active_element_css()`                  | Retrieves the CSS selector of the active element.                                                                                             |

### Browser and Window Management

| Method                                      | Description                                                                                             |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `maximize()`                                | Maximizes the browser window.                                                                           |
| `minimize()`                                | Minimizes the browser window.                                                                           |
| `medimize()`                                | Restores the window to its normal size from a minimized state.                                          |
| `set_window_rect(x, y, width, height)`      | Sets the position and size of the browser window.                                                       |
| `reset_window_size()`                       | Resets the window to its default size.                                                                  |
| `get_window_rect()`                         | Retrieves the position and size of the browser window.                                                  |
| `get_window_size()`                         | Retrieves the width and height of the browser window.                                                   |
| `get_window_position()`                     | Retrieves the x and y coordinates of the browser window.                                                |
| `get_screen_rect()`                         | Retrieves the dimensions of the screen.                                                                 |
| `tile_windows(windows=None, ...)`           | Arranges multiple browser windows in a tiled grid.                                                      |
| `bring_active_window_to_front()`            | Brings the currently active browser window to the foreground.                                           |
| `save_screenshot(name, folder=None, ...)`   | Saves a screenshot of the current viewport or a specific element.                                       |
| `print_to_pdf(name, folder=None)`           | Prints the current page to a PDF file.                                                                  |

### Cookies and Storage

| Method                                 | Description                                                                                                                                                                                                                                                                                                                         |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_all_cookies(*args, **kwargs)`     | Retrieves all cookies for the current domain.                                                                                                                                                                                                                                                                                       |
| `set_all_cookies(*args, **kwargs)`     | Sets multiple cookies.                                                                                                                                                                                                                                                                                                              |
| `save_cookies(*args, **kwargs)`        | Saves the current cookies to a file.                                                                                                                                                                                                                                                                                                |
| `load_cookies(*args, **kwargs)`        | Loads cookies from a file.                                                                                                                                                                                                                                                                                                          |
| `clear_cookies()`                      | Clears all cookies for the current domain.                                                                                                                                                                                                                                                                                          |
| `get_cookie_string()`                  | Retrieves the cookies as a single string.                                                                                                                                                                                                                                                                                           |
| `get_local_storage_item(key)`          | Retrieves an item from the browser's local storage.                                                                                                                                                                                                                                                                                 |
| `set_local_storage_item(key, value)`   | Sets an item in the browser's local storage.                                                                                                                                                                                                                                                                                          |
| `get_session_storage_item(key)`        | Retrieves an item from the browser's session storage.                                                                                                                                                                                                                                                                               |
| `set_session_storage_item(key, value)` | Sets an item in the browser's session storage.                                                                                                                                                                                                                                                                                        |

### Permissions

| Method                               | Description                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grant_permissions(permissions, ...)`| Grants specific browser permissions (e.g., "geolocation", "notifications").                                                                                                                                                                                                                                                           |
| `grant_all_permissions()`            | Grants all possible browser permissions.                                                                                                                                                                                                                                                                                            |
| `reset_permissions()`                | Resets all browser permissions to their default state.                                                                                                                                                                                                                                                                              |

### Advanced and GUI Automation

| Method                                       | Description                                                                                                                                                                                                                                                                                                                         |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gui_press_key(key)`                         | Simulates a single key press using `PyAutoGUI`.                                                                                                                                                                                                                                                                                     |
| `gui_press_keys(keys)`                       | Simulates a sequence of key presses using `PyAutoGUI`.                                                                                                                                                                                                                                                                                |
| `gui_write(text)`                            | Simulates typing text using `PyAutoGUI`.                                                                                                                                                                                                                                                                                            |
| `gui_click_x_y(x, y)`                        | Clicks at the specified screen coordinates.                                                                                                                                                                                                                                                                                         |
| `gui_click_element(selector)`                | Clicks the center of a specified element.                                                                                                                                                                                                                                                                                           |
| `gui_drag_drop_points(x1, y1, x2, y2, ...)`  | Drags the mouse from a starting point to an ending point.                                                                                                                                                                                                                                                                           |
| `gui_drag_and_drop(drag_selector, ...)`      | Drags an element and drops it onto another element.                                                                                                                                                                                                                                                                                 |
| `gui_click_and_hold(selector, ...)`          | Clicks and holds an element.                                                                                                                                                                                                                                                                                                        |
| `gui_hover_x_y(x, y)`                        | Hovers the mouse over specified screen coordinates.                                                                                                                                                                                                                                                                                 |
| `gui_hover_element(selector)`                | Hovers the mouse over the center of an element.                                                                                                                                                                                                                                                                                     |
| `gui_hover_and_click(hover_selector, ...)`   | Hovers over one element and then clicks another.                                                                                                                                                                                                                                                                                    |

### Assertions and Waits

| Method                                      | Description                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `wait_for_text(text, selector="body", ...)` | Waits for the specified text to appear within an element.                                                                                                                                                                                                                                                                           |
| `wait_for_text_not_visible(text, ...)`      | Waits for the specified text to become invisible.                                                                                                                                                                                                                                                                                     |
| `wait_for_element_visible(selector, ...)`   | Waits for an element to become visible.                                                                                                                                                                                                                                                                                             |
| `wait_for_element_not_visible(selector, ...)`| Waits for an element to become invisible.                                                                                                                                                                                                                                                                                           |
| `wait_for_element_absent(selector, ...)`    | Waits for an element to be removed from the DOM.                                                                                                                                                                                                                                                                                      |
| `wait_for_any_of_elements_visible(...)`     | Waits for at least one of several elements to become visible.                                                                                                                                                                                                                                                                         |
| `wait_for_any_of_elements_present(...)`     | Waits for at least one of several elements to be present in the DOM.                                                                                                                                                                                                                                                                  |
| `assert_element(selector, timeout=None)`    | Asserts that an element is visible.                                                                                                                                                                                                                                                                                                 |
| `assert_element_visible(selector, ...)`     | An alias for `assert_element()`.                                                                                                                                                                                                                                                                                                    |
| `assert_element_present(selector, ...)`     | Asserts that an element is present in the DOM.                                                                                                                                                                                                                                                                                      |
| `assert_element_absent(selector, ...)`      | Asserts that an element is not present in the DOM.                                                                                                                                                                                                                                                                                  |
| `assert_element_not_visible(selector, ...)` | Asserts that an element is not visible.                                                                                                                                                                                                                                                                                             |
| `assert_element_attribute(selector, ...)`   | Asserts that an element has a specific attribute and, optionally, that the attribute has a specific value.                                                                                                                                                                                                                            |
| `assert_title(title)`                       | Asserts that the page title matches the specified text.                                                                                                                                                                                                                                                                             |
| `assert_title_contains(substring)`          | Asserts that the page title contains the specified substring.                                                                                                                                                                                                                                                                         |
| `assert_url(url)`                           | Asserts that the current URL matches the specified URL.                                                                                                                                                                                                                                                                               |
| `assert_url_contains(substring)`            | Asserts that the current URL contains the specified substring.                                                                                                                                                                                                                                                                        |
| `assert_text(text, selector="html", ...)`   | Asserts that the specified text is present within an element.                                                                                                                                                                                                                                                                         |
| `assert_exact_text(text, selector="html", ...)`| Asserts that the exact text matches the content of an element.                                                                                                                                                                                                                                                                     |
| `assert_text_not_visible(text, ...)`        | Asserts that the specified text is not visible.                                                                                                                                                                                                                                                                                     |
| `assert_true(expression)`                   | Asserts that an expression evaluates to `True`.                                                                                                                                                                                                                                                                                     |
| `assert_false(expression)`                  | Asserts that an expression evaluates to `False`.                                                                                                                                                                                                                                                                                    |
| `assert_equal(first, second)`               | Asserts that two values are equal.                                                                                                                                                                                                                                                                                                  |
| `assert_not_equal(first, second)`           | Asserts that two values are not equal.                                                                                                                                                                                                                                                                                              |
| `assert_in(first, second)`                  | Asserts that the first value is contained within the second.                                                                                                                                                                                                                                                                          |
| `assert_not_in(first, second)`              | Asserts that the first value is not contained within the second.                                                                                                                                                                                                                                                                      |

This comprehensive API reference should provide you with the knowledge and tools needed to effectively use SeleniumBase's CDP mode for your web automation and scraping projects. For more examples and advanced usage, refer to the official SeleniumBase documentation and the `examples/cdp_mode` directory in the repository.

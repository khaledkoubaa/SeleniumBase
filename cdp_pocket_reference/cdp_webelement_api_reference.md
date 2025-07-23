# CDP Mode: WebElement API - Pocket Reference

This document provides an extensive pocket reference for the WebElement API methods available in SeleniumBase's Chrome DevTools Protocol (CDP) mode. When you find an element using methods like `sb.cdp.find_element()`, it returns a WebElement object with its own set of methods. This guide details each of these methods with explanations, examples, and clarifications.

## Introduction to WebElement Methods

After locating a web element, you can perform various actions on it, such as clicking it, typing into it, or retrieving its attributes. The methods listed below are called on the element object itself.

**Example of finding an element and calling a method on it:**

```python
# Find the search input element
search_input = sb.cdp.find_element("input#search")

# Type into the search input
search_input.type("SeleniumBase")
```

## WebElement Methods

### `clear_input()`

Clears the text from an input field or textarea.

**Example:**

```python
email_field = sb.cdp.find_element("input#email")
email_field.clear_input()
```

### `click()`

Clicks the element. This is the standard way to interact with buttons, links, etc.

**Example:**

```python
login_button = sb.cdp.find_element("button#login")
login_button.click()
```

### `flash(duration=0.5, color="EE4488")`

Briefly highlights the element with a colored dot. Useful for visual debugging.

*   **`duration`**: The duration of the flash in seconds.
*   **`color`**: The color of the flash in RGB hex format.

**Example:**

```python
submit_button = sb.cdp.find_element("button#submit")
submit_button.flash(duration=1, color="FF0000")
```

### `focus()`

Brings the element into focus. This can trigger focus-dependent JavaScript events.

**Example:**

```python
comment_box = sb.cdp.find_element("textarea#comment")
comment_box.focus()
```

### `gui_click(timeframe=0.25)`

Simulates a click using `PyAutoGUI`. This is a stealthier way to click, as it moves the mouse cursor over the element before clicking.

*   **`timeframe`**: The duration of the mouse movement.

**Example:**

```python
download_link = sb.cdp.find_element("a#download")
download_link.gui_click()
```

### `highlight_overlay()`

Places a persistent overlay on the element to highlight it. The overlay remains until the page is reloaded or you navigate away.

**Example:**

```python
important_row = sb.cdp.find_element("tr#important-data")
important_row.highlight_overlay()
```

### `mouse_click()`

Simulates a mouse click on the element. This can be more human-like than a simple `click()`.

**Example:**

```python
dropdown_trigger = sb.cdp.find_element("div.dropdown-trigger")
dropdown_trigger.mouse_click()
```

### `mouse_drag(destination)`

Drags the element to a specified destination. The destination can be another element or a set of coordinates.

*   **`destination`**: The target element or coordinates to drag to.

**Example:**

```python
# Drag a slider handle
slider_handle = sb.cdp.find_element("div.slider-handle")
slider_track = sb.cdp.find_element("div.slider-track")
slider_handle.mouse_drag(slider_track)
```

### `mouse_move()`

Moves the mouse cursor over the element, triggering any hover effects.

**Example:**

```python
menu_item = sb.cdp.find_element("li#menu-item-3")
menu_item.mouse_move()  # To reveal a submenu
```

### `press_keys(text)`

Simulates typing text into an element at a human-like speed.

*   **`text`**: The text to type.

**Example:**

```python
search_bar = sb.cdp.find_element("input#search")
search_bar.press_keys("SeleniumBase automation")
```

### `query_selector(selector)`

Finds the first child element that matches the given CSS selector.

*   **`selector`**: The CSS selector of the child element.

**Example:**

```python
# Find a form and then find the submit button within it
form = sb.cdp.find_element("form#login-form")
submit_button = form.query_selector("button[type='submit']")
submit_button.click()
```

### `querySelector(selector)`

An alias for `query_selector()`.

### `query_selector_all(selector)`

Finds all child elements that match the given CSS selector.

*   **`selector`**: The CSS selector of the child elements.

**Example:**

```python
# Find a list and get all of its items
item_list = sb.cdp.find_element("ul#item-list")
items = item_list.query_selector_all("li")
for item in items:
    print(item.text)
```

### `querySelectorAll(selector)`

An alias for `query_selector_all()`.

### `remove_from_dom()`

Removes the element from the DOM.

**Example:**

```python
ad_banner = sb.cdp.find_element("div.ad")
ad_banner.remove_from_dom()
```

### `save_screenshot(*args, **kwargs)`

Saves a screenshot of the element.

*   **`*args`**: Arguments to pass to the screenshot function, such as the filename.
*   **`**kwargs`**: Keyword arguments, such as the folder.

**Example:**

```python
chart = sb.cdp.find_element("div#chart-container")
chart.save_screenshot("my_chart.png", folder="screenshots")
```

### `save_to_dom()`

Saves the element's current state to the DOM. This is not a standard Selenium method and its use case is very specific.

**Example:**

```python
# This method is not commonly used.
# Refer to SeleniumBase documentation for specific use cases.
```

### `scroll_into_view()`

Scrolls the page to bring the element into view.

**Example:**

```python
footer_link = sb.cdp.find_element("a#contact-us")
footer_link.scroll_into_view()
footer_link.click()
```

### `select_option()`

Selects an `<option>` element within a `<select>` dropdown.

**Example:**

```python
# Find the option for "Canada" and select it
country_dropdown = sb.cdp.find_element("select#country")
canada_option = country_dropdown.query_selector('option[value="CA"]')
canada_option.select_option()
```

### `send_file(*file_paths)`

Uploads one or more files to an `<input type="file">` element.

*   **`*file_paths`**: The path(s) to the file(s) to upload.

**Example:**

```python
file_input = sb.cdp.find_element('input[type="file"]')
file_input.send_file("/path/to/my/file.txt")
```

### `send_keys(text)`

Sends a sequence of key presses to the element.

*   **`text`**: The text to send.

**Example:**

```python
username_field = sb.cdp.find_element("input#username")
username_field.send_keys("testuser")
```

### `set_text(value)`

Sets the text of an element directly. This is not for input fields, but for elements where you want to change the visible text.

*   **`value`**: The text to set.

**Example:**

```python
# Change the text of a heading
heading = sb.cdp.find_element("h1")
heading.set_text("Welcome to the New Page")
```

### `type(text)`

Clears the text field and then sends keys. A combination of `clear_input()` and `send_keys()`.

*   **`text`**: The text to type.

**Example:**

```python
email_field = sb.cdp.find_element("input#email")
email_field.type("new.email@example.com")
```

### `get_position()`

Retrieves the position and size of the element. Returns a dictionary with `x`, `y`, `width`, and `height`.

**Example:**

```python
button = sb.cdp.find_element("button#my-button")
position = button.get_position()
print(f"Button is at ({position['x']}, {position['y']})")
```

### `get_html()`

Retrieves the outer HTML of the element.

**Example:**

```python
element = sb.cdp.find_element("div#my-div")
html_content = element.get_html()
print(html_content)
```

### `get_js_attributes()`

Retrieves all the JavaScript attributes of the element.

**Example:**

```python
element = sb.cdp.find_element("div#my-div")
attributes = element.get_js_attributes()
print(attributes)
```

### `get_attribute(attribute)`

Retrieves the value of a specific attribute of the element.

*   **`attribute`**: The name of the attribute to retrieve.

**Example:**

```python
link = sb.cdp.find_element("a#my-link")
href = link.get_attribute("href")
print(f"The link goes to: {href}")
```

### `get_parent()`

Retrieves the parent element of the current element.

**Example:**

```python
child_element = sb.cdp.find_element("span.child")
parent_element = child_element.get_parent()
print(f"Parent tag: {parent_element.tag_name}")
```

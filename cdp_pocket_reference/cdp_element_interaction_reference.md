# CDP Mode: Element Interaction - Pocket Reference

This document provides an extensive pocket reference for the element interaction methods available in SeleniumBase's Chrome DevTools Protocol (CDP) mode. Each method is detailed with explanations, examples, and additional clarifications to help you write robust and reliable automation scripts.

## Introduction to Element Interaction in CDP Mode

Interacting with elements is at the core of web automation. CDP mode provides a rich set of methods to click, type, and otherwise manipulate elements on a web page. These methods are designed to be stealthy, reducing the likelihood of bot detection.

### `click(selector, timeout=None)`

Clicks the specified element. This is the most common way to interact with buttons, links, and other clickable elements.

*   **`selector`**: The CSS selector of the element to click.
*   **`timeout`**: The maximum time to wait for the element to be ready for a click.

**Example:**

```python
# Click the "Login" button
sb.cdp.click("button#login")
```

### `click_active_element()`

Clicks the currently active (focused) element on the page. This is useful when you need to interact with an element that has just received focus.

**Example:**

```python
# Focus on an input field, then click it
sb.cdp.focus("input#username")
sb.cdp.click_active_element()
```

### `click_if_visible(selector)`

Clicks the element only if it is visible. This prevents errors that might occur if you try to click an element that is not on the screen.

*   **`selector`**: The CSS selector of the element.

**Example:**

```python
# Click the "Close" button on a popup, if it exists
sb.cdp.click_if_visible("button.close-popup")
```

### `click_visible_elements(selector, limit=0)`

Clicks all visible elements matching the selector. You can optionally limit the number of clicks.

*   **`selector`**: The CSS selector of the elements.
*   **`limit`**: The maximum number of elements to click. If `0`, all visible elements will be clicked.

**Example:**

```python
# Click all checkboxes on the page
sb.cdp.click_visible_elements('input[type="checkbox"]')
```

### `mouse_click(selector, timeout=None)`

Simulates a mouse click on the element. This can be more human-like than a simple `click()`.

*   **`selector`**: The CSS selector of the element.
*   **`timeout`**: The maximum time to wait for the element.

**Example:**

```python
# Use a mouse click to open a dropdown menu
sb.cdp.mouse_click("div.dropdown-trigger")
```

### `nested_click(parent_selector, selector)`

Clicks a child element within a parent element. This is particularly useful for clicking elements inside an iframe or a complex component.

*   **`parent_selector`**: The CSS selector of the parent element.
*   **`selector`**: The CSS selector of the child element to click.

**Example:**

```python
# Click a button inside an iframe
sb.cdp.nested_click("iframe#my-iframe", "button#submit")
```

### `send_keys(selector, text, timeout=None)`

Sends a sequence of key presses to an element. This is the primary method for typing into input fields.

*   **`selector`**: The CSS selector of the input element.
*   **`text`**: The text to type.
*   **`timeout`**: The maximum time to wait for the element.

**Example:**

```python
# Enter a username and password
sb.cdp.send_keys("input#username", "my_user")
sb.cdp.send_keys("input#password", "my_password")
```

### `press_keys(selector, text, timeout=None)`

Simulates typing at a human-like speed. This can help avoid bot detection on some sites.

*   **`selector`**: The CSS selector of the input element.
*   **`text`**: The text to type.
*   **`timeout`**: The maximum time to wait.

**Example:**

```python
# Slowly type a search query
sb.cdp.press_keys("input#search", "SeleniumBase rocks!")
```

### `type(selector, text, timeout=None)`

Clears the text field and then sends keys. This is a convenience method that combines clearing an input with typing into it.

*   **`selector`**: The CSS selector of the input element.
*   **`text`**: The text to type.
*   **`timeout`**: The maximum time to wait.

**Example:**

```python
# Update the value of a text field
sb.cdp.type("input#email", "new.email@example.com")
```

### `set_value(selector, text, timeout=None)`

Sets the value of an input field directly using JavaScript. This is faster than `send_keys` but may be more detectable.

*   **`selector`**: The CSS selector of the input element.
*   **`text`**: The value to set.
*   **`timeout`**: The maximum time to wait.

**Example:**

```python
# Set the value of a hidden input field
sb.cdp.set_value('input[type="hidden"][name="token"]', "abc-123")
```

### `submit(selector)`

Submits a form by simulating a key press on the "Enter" key. This is often used after filling out a form.

*   **`selector`**: The CSS selector of an element within the form.

**Example:**

```python
# Fill out a form and submit it
sb.cdp.type("input#name", "John Doe")
sb.cdp.submit("form#contact-form")
```

### `focus(selector)`

Brings an element into focus. This can be useful for triggering focus-dependent events.

*   **`selector`**: The CSS selector of the element to focus.

**Example:**

```python
# Focus on a text area to enable a "submit" button
sb.cdp.focus("textarea#comment")
```

### `scroll_into_view(selector)`

Scrolls the page to bring the specified element into view. This is essential for interacting with elements that are off-screen.

*   **`selector`**: The CSS selector of the element.

**Example:**

```python
# Scroll to the "Terms and Conditions" section before clicking it
sb.cdp.scroll_into_view("a#terms-and-conditions")
sb.cdp.click("a#terms-and-conditions")
```

### `flash(selector, duration=1, color="44CC88", pause=0)`

Briefly highlights an element with a colored dot. This is useful for debugging and visualizing which element is being interacted with.

*   **`selector`**: The CSS selector of the element.
*   **`duration`**: The duration of the flash in seconds.
*   **`color`**: The color of the flash in RGB hex format.
*   **`pause`**: An optional pause after the flash.

**Example:**

```python
# Flash the "Add to Cart" button before clicking it
sb.cdp.flash("button.add-to-cart", duration=2, color="FF0000")
sb.cdp.click("button.add-to-cart")
```

### `highlight(selector)`

Highlights an element with a multi-colored effect. This is another visual debugging tool.

*   **`selector`**: The CSS selector of the element.

**Example:**

```python
# Highlight the main heading of the page
sb.cdp.highlight("h1")
```

### `highlight_overlay(selector)`

Places a persistent overlay on an element to highlight it. The overlay remains until the page is reloaded.

*   **`selector`**: The CSS selector of the element.

**Example:**

```python
# Highlight a specific table row for inspection
sb.cdp.highlight_overlay("tr#row-5")
```

### `select_option_by_text(dropdown_selector, option)`

Selects an option from a dropdown menu based on its visible text.

*   **`dropdown_selector`**: The CSS selector of the `<select>` element.
*   **`option`**: The text of the option to select.

**Example:**

```python
# Select "United States" from a country dropdown
sb.cdp.select_option_by_text("select#country", "United States")
```

### `check_if_unchecked(selector)`

Checks a checkbox if it is not already checked.

*   **`selector`**: The CSS selector of the checkbox.

**Example:**

```python
# Ensure the "I agree to the terms" checkbox is checked
sb.cdp.check_if_unchecked("input#terms-checkbox")
```

### `uncheck_if_checked(selector)`

Unchecks a checkbox if it is already checked.

*   **`selector`**: The CSS selector of the checkbox.

**Example:**

```python
# Ensure the "Subscribe to newsletter" checkbox is not checked
sb.cdp.uncheck_if_checked("input#subscribe-checkbox")
```

### `remove_element(selector)`

Removes a single element from the DOM. This can be useful for simplifying the page or removing distracting elements.

*   **`selector`**: The CSS selector of the element to remove.

**Example:**

```python
# Remove a banner ad
sb.cdp.remove_element("div.ad-banner")
```

### `remove_elements(selector)`

Removes all elements matching the selector from the DOM.

*   **`selector`**: The CSS selector of the elements to remove.

**Example:**

```python
# Remove all social media sharing buttons
sb.cdp.remove_elements("button.social-share")
```

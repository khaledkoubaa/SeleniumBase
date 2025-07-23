# CDP Mode: Assertions and Waits - Pocket Reference

This document provides an extensive pocket reference for the assertion and wait methods available in SeleniumBase's Chrome DevTools Protocol (CDP) mode. Each method is detailed with explanations, examples, and additional clarifications to help you write robust and reliable automation scripts.

## Introduction to Assertions and Waits in CDP Mode

Assertions and waits are crucial for creating stable and predictable automation scripts. In CDP mode, these methods are designed to handle the asynchronous nature of web pages, ensuring that your script only proceeds when the application is in the expected state.

*   **Waits**: These methods pause the execution of your script until a specific condition is met, such as an element becoming visible or text appearing on the page. They are essential for dealing with dynamic content and slow-loading pages.
*   **Assertions**: These methods verify that the state of the application is as expected. If an assertion fails, it will raise an exception, typically causing the test to fail. This is how you validate the behavior of your application.

## Wait Methods

### `wait_for_text(text, selector="body", timeout=None)`

Waits for the specified text to appear within an element. This is useful for synchronizing your script with dynamically loaded content.

*   **`text`**: The text to wait for.
*   **`selector`**: The CSS selector of the element to search within. Defaults to the entire `<body>`.
*   **`timeout`**: The maximum time to wait in seconds. If `None`, the default timeout is used.

**Example:**

```python
# Wait for the text "Welcome, User!" to appear in the header
sb.cdp.wait_for_text("Welcome, User!", "header#main-header")
```

### `wait_for_text_not_visible(text, selector="body", timeout=None)`

Waits for the specified text to become invisible. This is useful for confirming that an action has removed content from the page.

*   **`text`**: The text to wait for to disappear.
*   **`selector`**: The CSS selector of the element to search within.
*   **`timeout`**: The maximum time to wait in seconds.

**Example:**

```python
# Wait for the "Loading..." message to disappear
sb.cdp.wait_for_text_not_visible("Loading...", "div#loading-spinner")
```

### `wait_for_element_visible(selector, timeout=None)`

Waits for an element to become visible on the page. This is one of the most common and useful wait methods.

*   **`selector`**: The CSS selector of the element to wait for.
*   **`timeout`**: The maximum time to wait in seconds.

**Example:**

```python
# Wait for the search results container to be visible
sb.cdp.wait_for_element_visible("div#search-results")
```

### `wait_for_element_not_visible(selector, timeout=None)`

Waits for an element to become invisible. The element may still be present in the DOM but not visible to the user.

*   **`selector`**: The CSS selector of the element.
*   **`timeout`**: The maximum time to wait in seconds.

**Example:**

```python
# Wait for a modal dialog to close
sb.cdp.wait_for_element_not_visible("div#modal-overlay")
```

### `wait_for_element_absent(selector, timeout=None)`

Waits for an element to be completely removed from the DOM. This is a stronger condition than `wait_for_element_not_visible`.

*   **`selector`**: The CSS selector of the element.
*   **`timeout`**: The maximum time to wait in seconds.

**Example:**

```python
# Wait for a temporary notification to be removed from the DOM
sb.cdp.wait_for_element_absent("div.temp-notification")
```

### `wait_for_any_of_elements_visible(*args, **kwargs)`

Waits for at least one of a list of elements to become visible. This is useful when a page can have different content depending on the situation.

*   **`*args`**: A list of CSS selectors.
*   **`timeout`**: (Optional) The maximum time to wait.

**Example:**

```python
# Wait for either the success message or the error message to appear
sb.cdp.wait_for_any_of_elements_visible("div.success", "div.error")
```

### `wait_for_any_of_elements_present(*args, **kwargs)`

Waits for at least one of a list of elements to be present in the DOM. Visibility is not required.

*   **`*args`**: A list of CSS selectors.
*   **`timeout`**: (Optional) The maximum time to wait.

**Example:**

```python
# Wait for either a <video> or <audio> tag to be present
sb.cdp.wait_for_any_of_elements_present("video", "audio")
```

## Assertion Methods

### `assert_element(selector, timeout=None)`

Asserts that an element is visible on the page. This is an alias for `assert_element_visible()`.

*   **`selector`**: The CSS selector of the element.
*   **`timeout`**: The maximum time to wait for the element to become visible.

**Example:**

```python
# Assert that the logo is visible
sb.cdp.assert_element("img#logo")
```

### `assert_element_visible(selector, timeout=None)`

Asserts that an element is visible. This is the same as `assert_element()`.

**Example:**

```python
# Assert that the "Add to Cart" button is visible
sb.cdp.assert_element_visible("button.add-to-cart")
```

### `assert_element_present(selector, timeout=None)`

Asserts that an element is present in the DOM, even if it's not visible.

*   **`selector`**: The CSS selector of the element.
*   **`timeout`**: The maximum time to wait for the element to be present.

**Example:**

```python
# Assert that a hidden input field exists in the form
sb.cdp.assert_element_present('input[type="hidden"][name="user_id"]')
```

### `assert_element_absent(selector, timeout=None)`

Asserts that an element is not present in the DOM.

*   **`selector`**: The CSS selector of the element.
*   **`timeout`**: The maximum time to wait for the element to be absent.

**Example:**

```python
# Assert that the "deleted_item" is no longer in the DOM
sb.cdp.assert_element_absent("div#item-123")
```

### `assert_element_not_visible(selector, timeout=None)`

Asserts that an element is not visible on the page.

*   **`selector`**: The CSS selector of the element.
*   **`timeout`**: The maximum time to wait for the element to become invisible.

**Example:**

```python
# Assert that the loading spinner is no longer visible
sb.cdp.assert_element_not_visible("div#loading-spinner")
```

### `assert_element_attribute(selector, attribute, value=None)`

Asserts that an element has a specific attribute. You can also optionally assert that the attribute has a specific value.

*   **`selector`**: The CSS selector of the element.
*   **`attribute`**: The name of the attribute.
*   **`value`**: (Optional) The expected value of the attribute.

**Example:**

```python
# Assert that the link has the correct href
sb.cdp.assert_element_attribute("a#home-link", "href", "https://example.com/")

# Assert that the button is disabled
sb.cdp.assert_element_attribute("button#submit", "disabled")
```

### `assert_title(title)`

Asserts that the page title exactly matches the specified text.

*   **`title`**: The expected page title.

**Example:**

```python
# Assert that the page title is "My Awesome App"
sb.cdp.assert_title("My Awesome App")
```

### `assert_title_contains(substring)`

Asserts that the page title contains the specified substring.

*   **`substring`**: The substring to look for in the title.

**Example:**

```python
# Assert that the page title contains "Dashboard"
sb.cdp.assert_title_contains("Dashboard")
```

### `assert_url(url)`

Asserts that the current URL exactly matches the specified URL.

*   **`url`**: The expected URL.

**Example:**

```python
# Assert that the URL is correct
sb.cdp.assert_url("https://example.com/login")
```

### `assert_url_contains(substring)`

Asserts that the current URL contains the specified substring.

*   **`substring`**: The substring to look for in the URL.

**Example:**

```python
# Assert that the URL contains the user's ID
sb.cdp.assert_url_contains("user_id=123")
```

### `assert_text(text, selector="html", timeout=None)`

Asserts that the specified text is present within an element.

*   **`text`**: The text to search for.
*   **`selector`**: The CSS selector of the element to search within. Defaults to the entire `<html>` tag.
*   **`timeout`**: The maximum time to wait.

**Example:**

```python
# Assert that the success message is displayed
sb.cdp.assert_text("Your changes have been saved.", "div.flash-message")
```

### `assert_exact_text(text, selector="html", timeout=None)`

Asserts that the exact text matches the content of an element.

*   **`text`**: The exact text to match.
*   **`selector`**: The CSS selector of the element.
*   **`timeout`**: The maximum time to wait.

**Example:**

```python
# Assert that the heading is exactly "Welcome"
sb.cdp.assert_exact_text("Welcome", "h1")
```

### `assert_text_not_visible(text, selector="body", timeout=None)`

Asserts that the specified text is not visible on the page.

*   **`text`**: The text to assert is not visible.
*   **`selector`**: The CSS selector to search within.
*   **`timeout`**: The maximum time to wait.

**Example:**

```python
# Assert that the error message is not displayed
sb.cdp.assert_text_not_visible("Invalid input", "div.error-message")
```

### Generic Assertions

These methods provide basic assertion capabilities that are not specific to web elements.

*   **`assert_true(expression)`**: Asserts that an expression is `True`.
*   **`assert_false(expression)`**: Asserts that an expression is `False`.
*   **`assert_equal(first, second)`**: Asserts that two values are equal.
*   **`assert_not_equal(first, second)`**: Asserts that two values are not equal.
*   **`assert_in(first, second)`**: Asserts that the first value is contained in the second.
*   **`assert_not_in(first, second)`**: Asserts that the first value is not contained in the second.

**Example:**

```python
# Get the number of items in the cart
cart_item_count = len(sb.cdp.find_elements("ul#cart > li"))

# Assert that the cart is not empty
sb.cdp.assert_true(cart_item_count > 0)

# Assert that there are 3 items in the cart
sb.cdp.assert_equal(cart_item_count, 3)
```

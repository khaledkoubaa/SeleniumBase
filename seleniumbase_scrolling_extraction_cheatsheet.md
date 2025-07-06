# SeleniumBase: Scrolling & Element Extraction Cheat Sheet

This cheat sheet provides common methods and examples for scrolling web pages or specific elements, and then extracting data using SeleniumBase.

**Initial Setup (Standard Mode Example):**
```python
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__) # If running as pytest

class MyScrollingTests(BaseCase):
    def test_scrolling_and_extraction(self):
        self.open("https://some-website-with-scrolling.com")
        # ... scrolling and extraction logic below ...
```

**Initial Setup (CDP Mode Example):**
```python
from seleniumbase import SB

with SB(uc=True) as sb: # Or sb = SB(uc=True) for manual quit
    sb.open("https://some-website-with-scrolling.com")
    # sb.activate_cdp_mode(sb.get_current_url()) # Optional, for CDP specific scrolling
    # ... scrolling and extraction logic below ...
```

## 1. Scrolling the Main Page Window

**a. Scroll to Bottom of the Page:**

*   **Standard Method:**
    ```python
    self.scroll_to_bottom()
    # Or to ensure it really gets there on dynamic pages:
    self.slow_scroll_to_bottom()
    ```
*   **JavaScript (often reliable):**
    ```python
    self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    ```
*   **CDP Mode:**
    ```python
    # sb.activate_cdp_mode(sb.get_current_url()) # If not already active
    sb.cdp.scroll_to_bottom()
    ```

**b. Scroll to a Specific Element:**

*   **Standard Method (ensures element is in view):**
    ```python
    self.scroll_to("footer#site-footer") # Scrolls to the element
    self.wait_for_element_visible("footer#site-footer") # Good practice
    ```
*   **CDP Mode:**
    ```python
    # sb.activate_cdp_mode(sb.get_current_url())
    sb.cdp.scroll_into_view("footer#site-footer")
    ```

**c. Scroll by a Specific Amount (Pixels):**

*   **Standard Method (JavaScript):**
    ```python
    self.execute_script("window.scrollBy(0, 500);") # Scrolls down 500 pixels
    self.execute_script("window.scrollBy(0, -200);") # Scrolls up 200 pixels
    ```
*   **CDP Mode:**
    ```python
    # sb.activate_cdp_mode(sb.get_current_url())
    sb.cdp.scroll_down(500) # Scrolls down 500px
    sb.cdp.scroll_up(200)   # Scrolls up 200px
    ```

**d. Scroll an Element into the Middle of the Viewport:**
*   **Standard Method:**
    ```python
    self.scroll_into_view_center("div#target-div")
    ```

## 2. Scrolling Within a Specific Scrollable Element

This applies to elements like popups, `<div>` tags with `overflow: scroll;` or `overflow: auto;`.

**a. Identify the Scrollable Element:**
First, you need the CSS selector for the scrollable container element itself.
Example: `scrollable_div_selector = "div.popup-content-area"`

**b. Scroll Scrollable Element to its Bottom:**

*   **Standard Method (JavaScript):**
    ```python
    scrollable_selector = "div.my-scrollable-list"
    # Ensure element is loaded
    self.wait_for_element_present(scrollable_selector)
    script = "arguments[0].scrollTop = arguments[0].scrollHeight;"
    self.execute_script(script, scrollable_selector)
    ```

**c. Scroll Scrollable Element to a Specific Inner Element:**

*   **Standard Method (JavaScript - more complex):**
    This often involves calculating offsets or using `scrollIntoView` on the inner element *if the browser correctly contexts it to the scrollable parent*.
    ```python
    scrollable_container = "div#scroll-box"
    inner_element = "div#scroll-box li:nth-child(20)"
    self.wait_for_element_present(inner_element)
    # Option 1: Try direct scrollIntoView (might scroll page too)
    # self.scroll_to(inner_element) # This might scroll the whole page

    # Option 2: More precise JS (can be tricky)
    # Get the inner element with JS, then call scrollIntoView on it within its parent.
    # This is highly dependent on page structure.
    # A simpler SeleniumBase approach is often to repeatedly scroll the container down
    # by a fixed amount until the inner element is visible.
    script = "arguments[0].scrollIntoView();"
    self.execute_script(script, inner_element) # May need adjustments
    ```
    A more robust SeleniumBase-centric way if direct JS is tricky:
    ```python
    scrollable_container = "div#scroll-box"
    inner_element_selector = "div#scroll-box li#item-50"
    while not self.is_element_visible(inner_element_selector):
        self.execute_script("arguments[0].scrollTop += 100;", scrollable_container)
        self.sleep(0.1) # Small pause to allow rendering
        # Add a counter or timeout to prevent infinite loops
        if self.is_element_visible(inner_element_selector): # Check again
            break
    self.assert_element_visible(inner_element_selector)
    ```

**d. Scroll Scrollable Element by a Specific Amount:**

*   **Standard Method (JavaScript):**
    ```python
    scrollable_selector = "div.terms-and-conditions"
    self.wait_for_element_present(scrollable_selector)
    script = "arguments[0].scrollTop += 200;" # Scroll down by 200px
    self.execute_script(script, scrollable_selector)
    ```

## 3. Handling Infinite Scroll / Lazy Loading

Pages that load more content as you scroll down require a loop.

**Strategy:**
1. Scroll down a bit.
2. Wait for new content to load (e.g., check if the number of items increased or a loading spinner disappeared).
3. If no new content loads after a few scrolls (or a specific "end" marker appears), assume you've reached the bottom.
4. Extract all loaded elements.

*   **Standard Method Example:**
    ```python
    self.open("https://example.com/infinite-scroll-items")

    product_selector = "div.product-item"
    initial_item_count = 0
    no_new_content_strikes = 0
    max_strikes = 3 # How many scrolls with no new items before stopping

    while no_new_content_strikes < max_strikes:
        self.scroll_to_bottom() # Or scroll by a fixed large amount
        self.sleep(1.5) # Wait for content to potentially load

        current_items = self.find_elements(product_selector)
        current_item_count = len(current_items)

        if current_item_count > initial_item_count:
            print(f"Loaded {current_item_count} items...")
            initial_item_count = current_item_count
            no_new_content_strikes = 0 # Reset strikes
        else:
            no_new_content_strikes += 1
            print(f"No new content loaded, strike {no_new_content_strikes}/{max_strikes}")

        # Optional: Check for an "end of results" message
        if self.is_element_visible("p#no-more-results"):
            print("Reached end of results marker.")
            break

    print(f"Finished scrolling. Total items found: {initial_item_count}")
    # Now extract from all 'current_items' or re-fetch all elements
    all_loaded_products = self.find_elements(product_selector)
    for product in all_loaded_products:
        print(product.text) # Or extract specific attributes
    ```

## 4. Extracting Elements After Scrolling

Once you've scrolled appropriately, element extraction is standard.

**a. Extracting a Single Element:**

*   **Standard Method:**
    ```python
    self.scroll_to("div#contact-info") # Ensure it's in view
    email = self.get_text("div#contact-info p.email")
    phone = self.get_attribute("div#contact-info a.phone-link", "href")
    print(f"Email: {email}, Phone Link: {phone}")
    ```
*   **CDP Mode:**
    ```python
    # sb.activate_cdp_mode(sb.get_current_url())
    sb.cdp.scroll_into_view("div#contact-info")
    email = sb.cdp.get_text("div#contact-info p.email")
    # For attributes with CDP, you might need to find element then get attribute
    contact_element = sb.cdp.find_element("div#contact-info a.phone-link")
    phone_link = contact_element.get_attribute("href") if contact_element else None
    print(f"CDP Email: {email}, Phone Link: {phone_link}")
    ```

**b. Extracting Multiple Elements:**

*   **Standard Method:**
    ```python
    self.scroll_to_bottom() # Ensure all are loaded/visible if not lazy-loaded
    item_selector = "ul#item-list li.list-item"
    self.wait_for_element_present(item_selector) # Wait for at least one

    items = self.find_elements(item_selector)
    all_item_texts = []
    for item_element in items:
        # Check visibility if items can be hidden but present in DOM
        if item_element.is_displayed(): # Selenium WebElement property
            all_item_texts.append(item_element.text)
    print(f"Found items: {all_item_texts}")
    ```
*   **CDP Mode:**
    ```python
    # sb.activate_cdp_mode(sb.get_current_url())
    sb.cdp.scroll_to_bottom()
    item_selector = "ul#item-list li.list-item"
    # Wait for at least one element to be present/visible using CDP waits
    sb.cdp.wait_for_element_visible(item_selector, timeout=5)

    cdp_elements = sb.cdp.find_elements(item_selector)
    all_cdp_item_texts = []
    for cdp_el in cdp_elements:
        # CDP elements don't have is_displayed directly, visibility is often
        # assumed if found by non-hidden selectors or checked with sb.cdp.is_element_visible(unique_selector_for_this_cdp_el)
        all_cdp_item_texts.append(cdp_el.text) # Access .text property
    print(f"CDP Found items: {all_cdp_item_texts}")
    ```

**c. Extracting from Stale Elements (After Scrolling/DOM Changes):**
If the DOM changes significantly after scrolling (common with React/Vue/Angular apps), previously found `WebElement` objects can become stale.
*   **Solution:** Re-fetch the elements after scrolling and any actions that might cause DOM re-renders.
    ```python
    self.scroll_to_bottom()
    self.sleep(1) # Allow for any dynamic updates
    # Re-fetch elements INSTEAD of using previously found ones
    updated_items = self.find_elements("div.product-tile")
    for item in updated_items:
        print(item.get_attribute("data-product-id"))
    ```

## Tips for Robust Scrolling & Extraction:

*   **Wait:** Always use appropriate waits (`self.wait_for_element_visible()`, `self.sleep()`, `sb.cdp.wait_for_element_visible()`) after scrolling, especially if content loads dynamically.
*   **Visibility:** Ensure elements are not just present in the DOM but also visible before trying to interact or extract text that depends on rendering. `self.is_element_visible()` or `element.is_displayed()` can help.
*   **StaleElementReferenceException:** If you encounter this, it means the element you're trying to use is no longer attached to the DOM. Re-find the element after the action that caused it to go stale (like a scroll that re-renders content).
*   **CDP vs Standard:**
    *   CDP scrolling (`sb.cdp.scroll_to_bottom()`, `sb.cdp.scroll_into_view()`) can sometimes be faster or behave differently.
    *   Standard methods using JavaScript execution (`self.execute_script()`) are very flexible and widely applicable.
*   **Small Incremental Scrolls:** For tricky scrollable elements or lazy loading, scrolling by smaller amounts in a loop and checking for visibility/new content can be more reliable than one large scroll.

---
This cheat sheet provides a foundation. Specific implementations may vary based on website structure and behavior.
```

The file `seleniumbase_scrolling_extraction_cheatsheet.md` has been created with the initial structure and content. I will proceed to populate and refine it according to the plan.

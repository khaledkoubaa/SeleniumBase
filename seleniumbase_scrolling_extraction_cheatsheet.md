# SeleniumBase: CDP Mode Scrolling & Element Extraction Cheat Sheet

This cheat sheet focuses on methods and examples for scrolling web pages or specific elements using **SeleniumBase CDP Mode**, and then extracting data.

**Initial Setup (CDP Mode):**

*   **With Context Manager (Recommended for most cases):**
    ```python
    from seleniumbase import SB

    with SB(uc=True) as sb: # uc=True is essential for CDP
        sb.open("https://some-website-with-scrolling.com")
        sb.activate_cdp_mode(sb.get_current_url()) # Activate CDP
        # ... CDP scrolling and extraction logic below ...
    # Browser closes automatically
    ```

*   **Without Context Manager (Manual Browser Lifecycle):**
    ```python
    from seleniumbase import SB

    sb = SB(uc=True) # uc=True is essential for CDP
    try:
        sb.open("https://some-website-with-scrolling.com")
        sb.activate_cdp_mode(sb.get_current_url()) # Activate CDP
        # ... CDP scrolling and extraction logic below ...
        print("Script finished. Browser will remain open if sb.driver.quit() is not called.")
    finally:
        # pass  # To keep browser open
        # Or, to close:
        # if hasattr(sb, 'driver') and sb.driver:
        #     sb.driver.quit()
        pass # For this example, keep it open or manage manually
    ```
**Important:** Always call `sb.activate_cdp_mode()` after `sb.open()` or navigating to the page where you intend to use `sb.cdp.*` methods.

## 1. Scrolling the Main Page Window (CDP Mode)

**a. Scroll to Bottom of the Page:**
    ```python
    # Assumes sb is initialized and CDP mode is active
    sb.cdp.scroll_to_bottom()
    sb.sleep(0.5) # Optional: short pause for content to settle
    ```

**b. Scroll to a Specific Element:**
    ```python
    # Assumes sb is initialized and CDP mode is active
    target_selector = "footer#site-footer"
    sb.cdp.scroll_into_view(target_selector)
    sb.cdp.wait_for_element_visible(target_selector, timeout=5) # Good practice
    ```

**c. Scroll by a Specific Amount (Pixels):**
    ```python
    # Assumes sb is initialized and CDP mode is active
    sb.cdp.scroll_down(500)  # Scrolls down 500px
    sb.sleep(0.3)
    sb.cdp.scroll_up(200)    # Scrolls up 200px
    ```

## 2. Scrolling Within a Specific Scrollable Element (CDP Mode)

Scrolling within a specific element (like a popup or a div with `overflow: scroll;`) using direct `sb.cdp.*` methods for sub-element scrolling is **less straightforward** than page scrolling. The `sb.cdp.scroll_into_view()` and `sb.cdp.scroll_down()` typically operate on the main viewport.

**Strategies for CDP Mode:**

*   **Focus and Keyboard Scroll (If Applicable):** If the scrollable element can receive focus and responds to keyboard arrow keys.
    ```python
    scrollable_container_selector = "div.popup-content-area"
    sb.cdp.focus(scrollable_container_selector)
    sb.sleep(0.1)
    # Simulate pressing ArrowDown key (requires PyAutoGUI integration, often via sb.cdp.gui_press_keys)
    # This is an advanced case; for simplicity, direct sb.cdp methods for this are limited.
    # Example using a GUI-based approach if direct CDP scroll isn't working for the inner element:
    # sb.cdp.gui_press_keys("\\ue015") # Example: ArrowDown key code
    # This might be needed multiple times in a loop.
    print(f"Note: Scrolling specific inner elements with only sb.cdp.* might require sb.cdp.evaluate() or GUI workarounds.")
    ```

*   **Using `sb.cdp.evaluate()` to execute JavaScript:** This is often the most reliable way to scroll specific sub-elements in CDP mode if direct CDP commands don't target them.
    ```python
    # Assumes sb is initialized and CDP mode is active
    scrollable_selector = "div.my-scrollable-list"
    sb.cdp.wait_for_element_present(scrollable_selector) # Ensure container exists

    # Scroll scrollable element to its bottom using JS
    js_script_bottom = "document.querySelector(arguments[0]).scrollTop = document.querySelector(arguments[0]).scrollHeight;"
    sb.cdp.evaluate(js_script_bottom % repr(scrollable_selector)) # repr() handles quotes
    sb.sleep(0.5)

    # Scroll scrollable element by a specific amount using JS
    js_script_by_amount = "document.querySelector(arguments[0]).scrollTop += 200;"
    sb.cdp.evaluate(js_script_by_amount % repr(scrollable_selector))
    sb.sleep(0.5)

    # Scroll to a specific inner element within the scrollable container using JS
    inner_element_selector_js = "li#item-20-within-scrollable" # JS compatible selector
    scrollable_container_js_selector = "div.my-scrollable-list" # JS compatible selector

    # Ensure the inner element is queryable by JS before trying to scroll to it
    # This JS tries to scroll the inner element into view within its scrollable parent
    js_scroll_inner_into_view = f"""
        var container = document.querySelector('{scrollable_container_js_selector}');
        var element = container ? container.querySelector('{inner_element_selector_js}') : null;
        if (element) {{
            element.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'nearest' }});
            return true;
        }}
        return false;
    """
    scrolled_ok = sb.cdp.evaluate(js_scroll_inner_into_view)
    if scrolled_ok:
        sb.cdp.wait_for_element_visible(f"{scrollable_container_js_selector} {inner_element_selector_js}")
    else:
        print(f"Could not scroll inner element {inner_element_selector_js} into view using JS.")
    ```
**Note:** For complex inner-element scrolling, direct JavaScript execution via `sb.cdp.evaluate()` is generally more robust in CDP mode than trying to adapt viewport-based CDP scroll commands.

## 3. Handling Infinite Scroll / Lazy Loading (CDP Mode)

Pages that load more content as you scroll down require a loop.

**Strategy (using CDP Mode):**
1. Scroll down the main page (e.g., `sb.cdp.scroll_to_bottom()` or `sb.cdp.scroll_down(amount)`).
2. Wait for new content (e.g., `sb.sleep()`, or `sb.cdp.wait_for_element_visible()` for a new item, or check item count).
3. If no new content loads after a few scrolls, or an "end" marker appears, assume bottom.
4. Extract all loaded elements using `sb.cdp.find_elements()`.

```python
# Assumes sb is initialized and CDP mode is active
sb.open("https://example.com/infinite-scroll-items")
sb.activate_cdp_mode(sb.get_current_url()) # Ensure CDP is active

product_selector = "div.product-item" # CSS selector for the items
initial_item_count = 0
no_new_content_strikes = 0
max_strikes = 3 # How many scrolls with no new items before stopping

print("Starting infinite scroll handling...")
while no_new_content_strikes < max_strikes:
    sb.cdp.scroll_to_bottom()
    sb.sleep(1.5) # Wait for content to potentially load, adjust as needed

    # Check for new items using CDP methods
    current_items = sb.cdp.find_elements(product_selector)
    current_item_count = len(current_items)

    if current_item_count > initial_item_count:
        print(f"Loaded {current_item_count} items...")
        initial_item_count = current_item_count
        no_new_content_strikes = 0 # Reset strikes
    else:
        no_new_content_strikes += 1
        print(f"No new content detected, strike {no_new_content_strikes}/{max_strikes}")

    # Optional: Check for an "end of results" message using CDP
    if sb.cdp.is_element_visible("p#no-more-results"):
        print("Reached end of results marker.")
        break

print(f"Finished scrolling. Total items found: {initial_item_count}")
# Now extract from all 'current_items' or re-fetch all elements
all_loaded_products = sb.cdp.find_elements(product_selector) # Re-fetch with CDP
for product_element in all_loaded_products:
    # product_element is a CDPWebElement
    print(product_element.text) # Or extract specific attributes like product_element.get_attribute('data-id')
```

## 4. Extracting Elements After Scrolling (CDP Mode)

Once you've scrolled, element extraction uses `sb.cdp.find_element()` or `sb.cdp.find_elements()`.

**a. Extracting a Single Element:**
    ```python
    # Assumes sb is initialized and CDP mode is active
    target_div_selector = "div#contact-info"
    email_selector_within_div = "p.email" # Relative selector
    phone_link_selector_within_div = "a.phone-link"

    sb.cdp.scroll_into_view(target_div_selector) # Ensure parent is in view
    sb.cdp.wait_for_element_visible(target_div_selector)

    # Get text from a child element
    email = sb.cdp.get_text(f"{target_div_selector} {email_selector_within_div}")

    # Get attribute from a child element
    phone_link_element = sb.cdp.find_element(f"{target_div_selector} {phone_link_selector_within_div}")
    phone_href = phone_link_element.get_attribute("href") if phone_link_element else "N/A"

    print(f"CDP Extracted Email: {email}, Phone Link: {phone_href}")
    ```

**b. Extracting Multiple Elements:**
    ```python
    # Assumes sb is initialized and CDP mode is active
    sb.cdp.scroll_to_bottom() # Ensure all are loaded/visible if not lazy-loaded

    item_selector = "ul#item-list li.list-item"
    sb.cdp.wait_for_element_present(item_selector, timeout=5) # Wait for at least one

    cdp_elements = sb.cdp.find_elements(item_selector)
    all_item_texts = []
    for cdp_el in cdp_elements:
        # cdp_el is a CDPWebElement
        # Visibility check might be needed if items can be hidden but present in DOM
        # For robust check: if sb.cdp.is_element_visible(unique_selector_for_cdp_el):
        all_item_texts.append(cdp_el.text) # Access .text property
    print(f"CDP Found items: {all_item_texts}")
    ```

**c. Extracting from Stale Elements (After Scrolling/DOM Changes):**
If the DOM changes significantly after scrolling, previously found `CDPWebElement` objects can become stale or point to the wrong underlying browser element.
*   **Solution:** Re-fetch the elements using `sb.cdp.find_elements()` *after* scrolling and any actions that might cause DOM re-renders.
    ```python
    # Assumes sb is initialized and CDP mode is active
    sb.cdp.scroll_to_bottom()
    sb.sleep(1) # Allow for any dynamic updates

    # Re-fetch elements INSTEAD of using previously found ones
    updated_item_selector = "div.product-tile"
    updated_items = sb.cdp.find_elements(updated_item_selector)
    for item_cdp_el in updated_items:
        print(item_cdp_el.get_attribute("data-product-id"))
    ```

## Tips for Robust CDP Scrolling & Extraction:

*   **Activate CDP Mode:** Always call `sb.activate_cdp_mode()` before using `sb.cdp.*` methods.
*   **Wait After Scroll:** Use `sb.sleep()` or specific `sb.cdp.wait_for_*` methods after scrolling, especially if content loads dynamically. CDP actions can be very fast.
*   **Visibility with CDP:** `sb.cdp.is_element_visible(selector)` is the primary way to check visibility. `CDPWebElement` objects themselves don't have an `is_displayed()` method like Selenium WebElements.
*   **Stale Elements:** Re-fetch elements with `sb.cdp.find_element(s)()` if the DOM might have changed after a scroll or other interaction.
*   **JavaScript via `sb.cdp.evaluate()`:** For complex scrolling within specific elements or custom scroll logic, `sb.cdp.evaluate()` is a powerful tool in CDP mode.
*   **Small Incremental Scrolls for Lazy Loading:** In the infinite scroll loop, instead of `sb.cdp.scroll_to_bottom()`, you could use `sb.cdp.scroll_down(fixed_amount)` multiple times, checking for new content more frequently.

---
This cheat sheet provides a foundation for CDP-focused scrolling. Specific implementations may vary.
```

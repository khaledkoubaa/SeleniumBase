# Scraping Infinite Scroll Pages with SeleniumBase CDP Mode

Infinite scroll is a common web design pattern where content is loaded continuously as the user scrolls down the page. This presents challenges for web scraping, as not all content is available on the initial page load. SeleniumBase CDP (Chrome DevTools Protocol) Mode offers effective ways to handle these scenarios.

## a. Introduction

**Challenges of Infinite Scroll:**
*   Content is loaded dynamically, often via JavaScript (XHR/Fetch requests) triggered by scroll events.
*   The full extent of the content is unknown beforehand.
*   Determining when all content has been loaded can be tricky.

**Benefits of CDP Mode:**
*   **Stealth:** CDP interactions can be less detectable than standard WebDriver actions, which is useful on sites with anti-bot measures.
*   **Speed:** Direct CDP commands can sometimes be faster.
*   **Control:** Provides fine-grained control over browser actions, including JavaScript execution and (more advanced) network event monitoring.

This guide outlines strategies for scraping infinite scroll pages using SeleniumBase CDP Mode.

## b. Core Setup (CDP Mode)

1.  **UC Mode is Essential:** CDP Mode in SeleniumBase builds on UC Mode.
    *   Initialize `SB` with `uc=True`.

2.  **Debugging Visibility:**
    *   Use `headless=False` (or `headless2=True` for headed mode with newer Chrome versions) during development to see what the browser is doing.
    *   Example: `sb = SB(uc=True, headless=False)`

3.  **Activate CDP Mode:**
    *   After initial page load with `sb.open()`, call `sb.activate_cdp_mode(sb.get_current_url())` before starting scroll interactions.

**Setup Examples:**

*   **With Context Manager (Recommended):**
    ```python
    from seleniumbase import SB
    import time

    with SB(uc=True, headless=False) as sb:
        sb.open("https://example.com/infinite-scroll-page")
        sb.activate_cdp_mode(sb.get_current_url())
        # ... Your infinite scroll logic using sb.cdp.* ...
    ```

*   **Without Context Manager (Manual Browser Lifecycle):**
    ```python
    from seleniumbase import SB
    import time

    sb = SB(uc=True, headless=False)
    try:
        sb.open("https://example.com/infinite-scroll-page")
        sb.activate_cdp_mode(sb.get_current_url())
        # ... Your infinite scroll logic using sb.cdp.* ...
        input("Browser open. Press Enter to quit.")
    finally:
        if hasattr(sb, 'driver') and sb.driver:
            sb.driver.quit()
    ```

## c. Strategy 1: Iterative Scrolling & Item Count Check

This is the most common and often simplest approach.

**Logic:**
1.  Scroll down (either to the page bottom or by a fixed amount).
2.  Pause briefly to allow new content to load.
3.  Count the number of relevant items currently in the DOM.
4.  If the item count has increased since the last scroll, repeat.
5.  If the item count hasn't changed after a few consecutive scrolls, assume the end is reached.
6.  Optionally, look for an explicit "end of results" marker.

**Example:**
```python
# Assumes 'sb' is initialized, page opened, and CDP mode active.
item_selector = "div.product-item"  # CSS selector for individual items
all_item_data = {} # Store unique items, using item ID or hash as key

last_item_count = 0
consecutive_no_new_items_strikes = 0
max_strikes = 3 # Stop after 3 scrolls with no new items

print("Starting iterative scroll...")
while consecutive_no_new_items_strikes < max_strikes:
    sb.cdp.scroll_to_bottom()  # Or sb.cdp.scroll_down(1000) for fixed amount
    sb.cdp.sleep(2)  # Adjust sleep time based on site's loading speed

    current_elements = sb.cdp.find_elements(item_selector)

    new_items_found_this_scroll = 0
    for el in current_elements:
        # Create a unique ID for the item (e.g., from data-id or by hashing content)
        item_id = el.get_attribute("data-id") # Assuming items have a data-id
        if not item_id: # Fallback if no data-id, hash some text content
            item_id = hash(el.text[:50]) # Example hash

        if item_id not in all_item_data:
            all_item_data[item_id] = {"text": el.text, "attribute": el.get_attribute("some-other-attribute")}
            new_items_found_this_scroll += 1

    current_total_items = len(all_item_data)
    print(f"Current total unique items: {current_total_items}. New this scroll: {new_items_found_this_scroll}")

    if new_items_found_this_scroll > 0:
        consecutive_no_new_items_strikes = 0 # Reset strikes
    else:
        consecutive_no_new_items_strikes += 1
        print(f"No new unique items found. Strike {consecutive_no_new_items_strikes}/{max_strikes}.")

    # Optional: Check for an "end of results" element
    end_marker_selector = "p.end-of-results"
    if sb.cdp.is_element_visible(end_marker_selector):
        print("Reached 'end of results' marker.")
        break

print(f"Finished scrolling. Total unique items extracted: {len(all_item_data)}")
# Now 'all_item_data' dictionary contains your scraped data
# for item_id, data in all_item_data.items():
# print(f"ID: {item_id}, Data: {data}")
```

## d. Strategy 2: Scroll & Wait for Specific Network Activity (Advanced Conceptual)

This can be more robust if item counts are unreliable or if there's a clear API call that loads new items.

**Logic:**
1.  Set up a CDP network event listener (e.g., for `Network.responseReceived` or `Network.loadingFinished`).
2.  Scroll down.
3.  In the event listener, check if the response URL matches the expected API endpoint for new items.
4.  Once the relevant network request that loads data completes, allow a brief moment for DOM update, then extract.
5.  This requires careful identification of the data-loading XHR/Fetch requests.

**Conceptual Example Snippet (Handler part):**
```python
# This is advanced and requires careful setup.
# relevant_api_url_part = "/api/items?page="
# new_data_loaded_flag = False

# def handle_network_response(params):
#     nonlocal new_data_loaded_flag
#     response_url = params.get("response", {}).get("url", "")
#     if relevant_api_url_part in response_url:
#         print(f"Relevant API call detected: {response_url}")
#         # Potentially check status code params.get("response", {}).get("status")
#         new_data_loaded_flag = True # Signal that new data might be available

# sb.cdp.add_handler("Network.responseReceived", handle_network_response)
# # ... perform scroll ...
# sb.cdp.sleep(0.1) # Tiny sleep to allow event to fire if request was fast
# # ... loop while new_data_loaded_flag is true or timeout ...
# # Reset new_data_loaded_flag = False before next scroll
# # sb.cdp.remove_handler("Network.responseReceived", handle_network_response) # Cleanup
```
**Note:** Full implementation is complex. For a cheat sheet, Strategy 1 is usually more practical to implement quickly.

## e. Strategy 3: Scroll & Check for DOM Mutation Markers

Instead of item count, look for visual cues or DOM elements that indicate loading or completion.

**Logic:**
1.  Scroll down.
2.  Look for a loading spinner to appear and then disappear.
3.  Or, wait for a placeholder element (e.g., "Load More" button) to be removed or changed.
4.  Or, wait for a *new batch* of items to become visible, perhaps by checking a known attribute on the last item of a batch.

**Example (Waiting for spinner to disappear):**
```python
# Assumes 'sb' is initialized, page opened, and CDP mode active.
spinner_selector = "div.loading-spinner"
item_selector = "div.product-item"

print("Scrolling and waiting for spinner...")
while True:
    sb.cdp.scroll_to_bottom()

    # Wait for spinner to appear (if it does on scroll) then disappear
    # This logic assumes spinner shows then hides when content is loaded
    try:
        # Briefly wait for spinner to potentially show if it's quick
        # If spinner is always there until content loads, this wait_for_visible might not be needed
        # sb.cdp.wait_for_element_visible(spinner_selector, timeout=1)
        sb.cdp.wait_for_element_absent(spinner_selector, timeout=5) # Wait for spinner to go away
        print("Spinner disappeared, content likely loaded.")
        # Potentially add a small fixed sleep here if content takes time to render AFTER spinner is gone
        sb.cdp.sleep(0.5)
    except Exception as e: # TimeoutException if spinner didn't disappear
        print(f"Spinner did not disappear or was not found as expected. Assuming end or error: {e}")
        break

    # Add logic here to check if new items were actually loaded to prevent infinite loops
    # (e.g., compare current item count to previous, similar to Strategy 1)
    # For simplicity, this example just breaks on spinner timeout.
    # A robust solution would combine this with item counting.

    # Optional: Check for "end of results" marker
    if sb.cdp.is_element_visible("p.end-of-results"):
        print("Reached 'end of results' marker.")
        break

print("Finished scrolling based on spinner.")
# Extract data...
```

## f. Strategy 4: Custom Scroll & Check Logic with `sb.cdp.evaluate()`

Execute JavaScript to perform scroll actions and check conditions directly in the browser's context.

**Logic:**
1.  Write a JavaScript function that:
    *   Scrolls the page (e.g., `window.scrollTo()`).
    *   Checks if new content was loaded (e.g., by comparing item counts before/after scroll, or looking for specific markers).
    *   Returns a status (e.g., `true` if new content loaded, `false` otherwise).
2.  Call this JS function repeatedly using `sb.cdp.evaluate()`.

**Example:**
```python
# Assumes 'sb' is initialized, page opened, and CDP mode active.
item_selector_js = "div.product-item" # JS-compatible selector

# JavaScript function to scroll and check for new items
# This is a simplified example; real-world JS might be more complex
scroll_and_check_js = f"""
(() => {{
    const initialItemCount = document.querySelectorAll('{item_selector_js}').length;
    window.scrollTo(0, document.body.scrollHeight);
    // Need a delay here for content to load, which is hard to do synchronously in a single evaluate call.
    // This strategy is better if the check for new content can be done immediately
    // or if the JS itself can wait (e.g. using Promises and async/await within the evaluate).
    // For simplicity, this example assumes immediate check or that a subsequent sleep in Python is used.
    // A better JS for this would involve MutationObserver or polling within the JS.
    // For this cheat sheet, we'll rely on a Python-side sleep.
    return {{ initialCount: initialItemCount }}; // Return initial count to compare later
}})()
"""

print("Scrolling using sb.cdp.evaluate() (conceptual)...")
previous_item_count = 0
strikes = 0
max_strikes_js = 3

while strikes < max_strikes_js:
    # Get current item count before scroll (can also be done in JS)
    current_elements_before_scroll = sb.cdp.find_elements(item_selector_js)
    count_before = len(current_elements_before_scroll)

    sb.cdp.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    sb.cdp.sleep(2) # CRITICAL: Allow time for new content to load after JS scroll

    current_elements_after_scroll = sb.cdp.find_elements(item_selector_js)
    count_after = len(current_elements_after_scroll)

    print(f"Items before: {count_before}, Items after: {count_after}")
    if count_after > count_before:
        strikes = 0
    else:
        strikes += 1
        print(f"No new items from JS scroll. Strike {strikes}/{max_strikes_js}")

    if sb.cdp.is_element_visible("p.end-of-results"):
        print("Reached 'end of results' marker via JS scroll strategy.")
        break

print("Finished scrolling with JS evaluate strategy.")
# Extract data...
```

## g. Data Extraction Best Practices Post-Scroll

*   **Uniqueness:** If items might appear duplicated during lazy loading or if your selectors are not precise enough, store extracted data in a way that ensures uniqueness (e.g., use a dictionary with item IDs as keys, or a set of tuples of key data points). The example in Strategy 1 demonstrates this.
*   **Re-Query Elements:** After all scrolling is complete, re-query the DOM for *all* items using `sb.cdp.find_elements(item_selector)`. This avoids potential `StaleElementReferenceException` if you try to use element objects found during earlier scroll iterations, as the DOM might have changed.
*   **Extract All Necessary Data:** Once you have the final list of `CDPWebElement` objects, iterate through them and extract all required text, attributes, etc.

## h. Key CDP Methods Recap for Infinite Scroll

*   `sb.cdp.scroll_to_bottom()`: Scrolls the main viewport to the bottom.
*   `sb.cdp.scroll_down(pixels)`: Scrolls down by a specified amount.
*   `sb.cdp.find_elements(selector)`: Gets a list of `CDPWebElement` objects.
*   `CDPWebElement.text` / `CDPWebElement.get_attribute(name)`: For data extraction from elements.
*   `sb.cdp.is_element_visible(selector)`: Checks if an element (like an end-marker or spinner) is visible.
*   `sb.cdp.wait_for_element_visible(selector, timeout)` / `sb.cdp.wait_for_element_absent(selector, timeout)`: Useful for waiting for loaders or new content sections.
*   `sb.cdp.sleep(seconds)`: Essential for pausing to allow asynchronous content loading.
*   `sb.cdp.evaluate(javascript_string)`: For custom in-browser scroll and check logic.

## i. Important Considerations

*   **Sleep/Wait Times:** Crucial. Too short, and you miss content. Too long, and the scrape is slow. These often need tuning per site.
*   **Detecting the End:** This is the hardest part. Relying on "no new items" for N tries is common. If an "end of results" message or element appears, use it.
*   **Rate Limits/Blocking:** Excessive scrolling or too many requests can trigger anti-bot measures. Implement polite delays.
*   **Memory Usage:** For extremely long infinite scroll pages, continuously adding elements to a Python list can consume significant memory. Consider processing/saving data in chunks if this becomes an issue.
*   **Error Handling:** Wrap scroll loops and extraction in `try...except` blocks to handle unexpected changes in page structure or timeouts.
*   **Site Changes:** Infinite scroll implementations vary. What works for one site may need adjustment for another. Scripts can be fragile to UI updates.

This guide provides several strategies. The best one (or combination) depends on how the specific target website implements its infinite scroll.
```

The file `seleniumbase_cdp_infinite_scroll_scraping.md` has been created with the initial structure and content outlining the planned sections and strategies.

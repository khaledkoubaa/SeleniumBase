# Guidelines for Scraping Google Search Results (SERP) with SeleniumBase

Scraping Google Search Engine Results Pages (SERP) can be challenging due to Google's anti-bot measures. However, with a powerful tool like SeleniumBase, it's possible to automate this process effectively. This guide provides best practices and a sample script to help you get started.

## Is it Possible with SeleniumBase?

Yes, it is possible to scrape Google SERP with SeleniumBase. The library includes features like Undetected-Chromedriver (UC) mode, which helps bypass many common anti-bot mechanisms. By using UC mode and other stealth techniques, you can reliably scrape search results.

## Sample Script: `scrape_google.py`

Here is a sample Python script that demonstrates how to scrape Google search results for a given query. This script is located in the `examples/` directory of the SeleniumBase repository.

### Code

```python
from seleniumbase import SB

def scrape_google(query):
    with SB(uc=True, test=True, headless=True) as sb:
        sb.open("https://google.com/ncr")
        sb.type('textarea[title="Search"]', f"{query}\n")
        sb.wait_for_element("div#search")
        results = sb.find_elements("div.g")
        scraped_data = []
        for result in results:
            try:
                title_element = result.find_element("h3")
                title = title_element.text
                link_element = result.find_element("a")
                link = link_element.get_attribute("href")
                if title and link:
                    scraped_data.append({"title": title, "link": link})
            except Exception as e:
                print(f"Skipping a result due to an error: {e}")
    return scraped_data

if __name__ == "__main__":
    search_query = "SeleniumBase GitHub"
    scraped_results = scrape_google(search_query)
    for item in scraped_results:
        print(item)
```

### How to Run the Script

1.  **Navigate to the `examples` directory:**

    ```bash
    cd examples
    ```

2.  **Run the script from your terminal:**

    ```bash
    python scrape_google.py
    ```

### Explanation

*   **`from seleniumbase import SB`**: Imports the necessary `SB` class from SeleniumBase.
*   **`with SB(uc=True, test=True, headless=True) as sb:`**: Initializes the SeleniumBase browser instance with specific configurations:
    *   `uc=True`: Enables Undetected-Chromedriver mode to avoid bot detection.
    *   `test=True`: Provides additional test-related features and exception handling.
    *   `headless=True`: Runs the browser in the background without a visible UI.
*   **`sb.open("https://google.com/ncr")`**: Opens Google's homepage. The `ncr` (no country redirect) ensures you get global search results.
*   **`sb.type('textarea[title="Search"]', f"{query}\n")`**: Types the search query into the search bar and presses Enter.
*   **`sb.wait_for_element("div#search")`**: Waits for the search results container to appear, ensuring the page has loaded.
*   **`results = sb.find_elements("div.g")`**: Selects all search result elements, which are typically contained within `div` tags with the class `g`.
*   **Looping through results**: The script iterates through each result, extracts the title (`h3` tag) and the link (`a` tag), and stores them in a list.
*   **Error Handling**: A `try-except` block is included to handle cases where a search result might not have a title or link, preventing the script from crashing.

## Best Practices and Guidelines

1.  **Use UC Mode**: Always enable `uc=True` to minimize the risk of being detected as a bot.
2.  **Headless Mode**: For scraping tasks, `headless=True` is recommended to improve performance and avoid unnecessary GUI rendering.
3.  **Rate Limiting**: Avoid sending too many requests in a short period. Implement delays between requests to mimic human behavior.
    *   You can use `sb.sleep(seconds)` to add delays.
4.  **User-Agent Rotation**: While SeleniumBase's UC mode handles many stealth aspects, you can further enhance this by rotating user-agents for different requests.
5.  **Handle CAPTCHAs**: Google may still present CAPTCHAs. Be prepared to handle them, either manually or by integrating a CAPTCHA-solving service.
6.  **Be Respectful**: Do not overload Google's servers. Adhere to their `robots.txt` file and terms of service. Scraping should be done responsibly.
7.  **Robust Element Selectors**: Google's page structure can change. Use reliable selectors (like `div.g` for results) and be prepared to update them if the scraping fails.

By following these guidelines and using the provided script as a starting point, you can effectively scrape Google search results with SeleniumBase.

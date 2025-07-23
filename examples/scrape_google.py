from seleniumbase import SB

def scrape_google(query):
    with SB(uc=True, test=True, headless=True) as sb:
        sb.open("https://google.com/ncr")
        sb.type('textarea[title="Search"]', f"{query}\n")
        sb.wait_for_element("div#search")
        results = sb.find_elements("div.g")
        scraped_data = []
        for result in results:
            title = result.find_element("h3").text
            link = result.find_element("a").get_attribute("href")
            scraped_data.append({"title": title, "link": link})
    return scraped_data

if __name__ == "__main__":
    search_query = "SeleniumBase GitHub"
    scraped_results = scrape_google(search_query)
    for item in scraped_results:
        print(item)

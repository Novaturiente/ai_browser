from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from google import genai


def scrape_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"
            }
        )
        page.goto(url, wait_until="load")

        # Get visible elements using JavaScript evaluation
        visible_html = page.evaluate("""() => {
            function isVisible(element) {
                const style = window.getComputedStyle(element);
                if (style.display === 'none') return false;
                if (style.visibility === 'hidden') return false;
                if (style.opacity === '0' || style.opacity === '0') return false;
                if (element.offsetWidth === 0 && element.offsetHeight === 0) return false;
                return true;
            }

            const allElements = document.querySelectorAll('body *');
            const visibleElements = [];
            
            for (const element of allElements) {
                if (isVisible(element)) {
                    // Clone to avoid modifying original DOM
                    visibleElements.push(element.cloneNode(true));
                }
            }

            // Create container and append visible elements
            const container = document.createElement('div');
            for (const el of visibleElements) {
                container.appendChild(el);
            }
            return container.innerHTML;
        }""")

        browser.close()
        source_data = BeautifulSoup(visible_html, "html.parser")
        data = summarize(url, source_data)

        return data


def summarize(url, content):
    client = genai.Client()
    message = f"""Extract data from this page source only keep relevent information. Format extracted data as markdown.
    url : {url}

    content : {content}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=message
    )
    return response.text


url = "https://nixos.wiki/wiki/Virt-manager"

data = scrape_data(url)
print(data)

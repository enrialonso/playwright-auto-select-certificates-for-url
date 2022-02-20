from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as playwright:
        context = playwright.chromium.launch(headless=False)
        page = context.new_page()
        page.goto("https://client.badssl.com/")
        print(page.inner_html("body"))
        context.close()


if __name__ == '__main__':
    main()

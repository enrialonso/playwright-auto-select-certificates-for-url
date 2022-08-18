import os

from playwright.sync_api import sync_playwright

CUSTOM_PREF = 'user_pref("security.default_personal_cert", "Select Automatically");'
DEFAULT_PROFILE_DIR = "./default"
CERT_PASSWORD = "badssl.com"


def set_default_profile_settings():
    with sync_playwright() as playwright:
        context = playwright.firefox.launch_persistent_context(
            headless=True,
            user_data_dir=DEFAULT_PROFILE_DIR,
        )
        page = context.new_page()
        page.goto("https://google.com/")
        context.close()

    # Update about:config for auto select the certificates on the cert9.db
    with open(f"{DEFAULT_PROFILE_DIR}/prefs.js", "r+", encoding="utf-8") as file:
        if CUSTOM_PREF not in file.read():
            file.write(CUSTOM_PREF)
            file.write("\n")

    # Storage the cert on cert9.db for use in the profile in the next launch of the browser
    os.system(f'pk12util -i "./badssl.com-client.p12" -d "{DEFAULT_PROFILE_DIR}" -W "{CERT_PASSWORD}"')


def main():

    set_default_profile_settings()

    with sync_playwright() as playwright:
        context = playwright.firefox.launch_persistent_context(
            headless=True,
            user_data_dir="./default",
        )
        page = context.new_page()

        page.goto("https://client.badssl.com/")
        print(page.inner_html("body"))
        context.close()


if __name__ == "__main__":
    main()

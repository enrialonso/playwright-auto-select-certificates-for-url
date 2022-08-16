import os

from playwright.sync_api import sync_playwright

custom_pref = 'user_pref("security.default_personal_cert", "Select Automatically");'
default_profile_dir = "./default"


def set_default_profile_settings():
    with sync_playwright() as playwright:
        context = playwright.firefox.launch_persistent_context(
            headless=True,
            user_data_dir=default_profile_dir,
        )
        page = context.new_page()
        page.goto("https://google.com/")
        context.close()

    # Update about:config for auto select the certificates on the cert9.db
    with open(f"{default_profile_dir}/prefs.js", "r+", encoding="utf-8") as file:
        if custom_pref not in file.read():
            file.write(custom_pref)
            file.write("\n")

    # Storage the cert on cert9.db for use in the profile in the next launch of the browser
    os.system(f'pk12util -i "./badssl.com-client.p12" -d "{default_profile_dir}" -W "badssl.com"')


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

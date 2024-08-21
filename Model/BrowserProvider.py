import json
import os.path
from Config import CONFIG
from playwright.sync_api import sync_playwright, Playwright, Page
from Config.Configuration import User
from pathlib import Path
import platform


class BrowserProvider:
    def __init__(self, user: User):
        args = ["--disable-blink-features=AutomationControlled"]
        pl = sync_playwright().start()
        self.playwright: Playwright = pl
        headless = platform.system() != "Windows"
        self.browser = pl.chromium.launch(headless=headless, args=args)
        self.context = self.browser.new_context(
            # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            #            "Chrome/58.0.3029.110 Safari/537.3")
            user_agent='5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36')

        self.load_cookies(user)
        self.page: Page = self.context.new_page()
        self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => false,
                });
                """)

    def dispose(self):
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def load_cookies(self, user: User):
        cookie_path = os.path.join(os.path.join(Path(__file__).parent.parent, 'Cookies'), f"cookies_{user.name}.json")
        if not os.path.exists(cookie_path):
            raise Exception(f"Cookie file does not exist at {cookie_path}")

        with open(cookie_path, "r") as f:
            cookies = json.loads(f.read())
            self.context.add_cookies(cookies)

    def change_url(self, new_url: str, html_id: str = None) -> None:
        i = 0
        is_page_changed = False
        while i < CONFIG.max_login_attempts and not is_page_changed:
            try:
                self.page.goto(url=new_url, timeout=5000)
                is_page_changed = True

                if html_id is not None:
                    self.page.wait_for_selector(html_id, state='visible', timeout=10000)

            except Exception:
                is_page_changed = False
            finally:
                i += 1

        if i >= CONFIG.max_login_attempts:
            raise Exception(f"page cannot be set to url {new_url}, and waited until {html_id} is visible")

from playwright.async_api import async_playwright
from playwright.async_api._generated import Browser, BrowserContext, Page, Playwright

from app.serializers import CustomNote


class AnkiWebPyConnector:
    login_url: str = "https://ankiweb.net/account/login"

    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password

    async def start(self) -> None:
        """Start the browser and login to Anki"""
        self.playwright: Playwright = await async_playwright().start()
        self.browser: Browser = await self.playwright.chromium.launch()
        self.context: BrowserContext = await self.browser.new_context()
        self.page: Page = await self.context.new_page()
        await self._login_into_anki()

    async def close(self) -> None:
        """Close browser resources"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def send_card(
        self,
        custom_note: CustomNote,
        tags: list[str],
        card_type: str = "Basic_",
    ) -> bool:
        """Add a new note to AnkiWeb"""
        await self.page.get_by_role("link", name="Add").click()

        type_selector = (
            self.page.get_by_role("main")
            .locator("div")
            .filter(has_text="Type Basic_")
            .get_by_role("textbox")
            .first
        )
        await type_selector.click()

        await self.page.get_by_text(card_type, exact=True).first.click()

        if tags:
            tag_field = self.page.locator("form").get_by_role("textbox")
            await tag_field.click()
            await tag_field.fill(",".join(tags) + ",")

        await self._fill_fields(custom_note)
        await self.page.get_by_role("button", name="Add").click()
        return True

    async def _login_into_anki(self) -> None:
        await self.page.goto(self.login_url)
        email_field = self.page.get_by_role("textbox", name="Email")
        await email_field.click()
        await email_field.fill(self.username)

        password_field = self.page.get_by_role("textbox", name="Password")
        await password_field.click()
        await password_field.fill(self.password)

        await self.page.get_by_role("button", name="Log In").click()

    async def _fill_fields(self, custom_note: CustomNote) -> None:
        if not custom_note.fields:
            return

        for field, value in custom_note.fields:
            if field == "audio":
                continue  # Skip audio handling

            if not value:
                continue

            field_locator = (
                self.page.get_by_role("main")
                .locator("div")
                .filter(has_text=field)
                .locator("div")
                .nth(1)
            )

            await field_locator.fill(value)

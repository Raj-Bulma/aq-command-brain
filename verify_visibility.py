import asyncio
from playwright.async_api import async_playwright

async def verify_visibility():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Load the index.html
        import os
        path = "file://" + os.path.abspath("index.html")
        await page.goto(path)

        # Bypass login if needed or wait for app
        # The app requires login. I should mock the login or bypass it.
        # I'll try to inject a session.
        await page.evaluate("localStorage.setItem('cb_ses', 'test@aqglobal.net')")
        await page.reload()

        # Wait for app to be visible
        await page.wait_for_selector("#app.on", timeout=5000)

        # Wait a bit for animations
        await asyncio.sleep(2)

        # Check visibility of mod-cards
        cards = await page.query_selector_all(".mod-card")
        print(f"Found {len(cards)} cards")

        for i, card in enumerate(cards):
            opacity = await card.evaluate("el => getComputedStyle(el).opacity")
            is_visible = await card.is_visible()
            print(f"Card {i} opacity: {opacity}, is_visible: {is_visible}")

        await page.screenshot(path="verification/visibility_check.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_visibility())

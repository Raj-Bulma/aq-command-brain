import asyncio
from playwright.async_api import async_playwright
import os

async def verify_visibility():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        path = "file://" + os.path.abspath("index.html")
        await page.goto(path)

        # Manually trigger bootApp logic
        await page.evaluate("""() => {
            CU = 'test@aqglobal.net';
            localStorage.setItem('cb_ses', CU);
            bootApp();
        }""")

        # Wait for app to be visible
        try:
            await page.wait_for_selector("#app.on", timeout=5000)
        except:
            print("App didn't turn on, checking state...")
            content = await page.content()
            # print(content)

        # Wait a bit for animations
        await asyncio.sleep(2)

        # Check visibility of mod-cards
        cards = await page.query_selector_all(".mod-card")
        print(f"Found {len(cards)} cards")

        os.makedirs("verification", exist_ok=True)
        for i, card in enumerate(cards):
            opacity = await card.evaluate("el => getComputedStyle(el).opacity")
            is_visible = await card.is_visible()
            text = await card.inner_text()
            print(f"Card {i} opacity: {opacity}, is_visible: {is_visible}, text sample: {text[:20]}")

        await page.screenshot(path="verification/visibility_check_v2.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_visibility())

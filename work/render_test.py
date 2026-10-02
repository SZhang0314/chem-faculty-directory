# -*- coding: utf-8 -*-
import asyncio, os
from playwright.async_api import async_playwright

HTML = r"D:\USTC-AI\chem-faculty\index.html"

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": 1400, "height": 1000})
        errors = []
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        await pg.goto("file:///" + HTML.replace("\\", "/"))
        await pg.wait_for_timeout(2500)
        shown = await pg.inner_text("#shown")
        schcount = await pg.inner_text("#schcount")
        cards = await pg.eval_on_selector_all(".card", "els => els.length")
        tabs = await pg.eval_on_selector_all("#schooltabs button", "els => els.map(e=>e.textContent.trim())")
        # test search
        await pg.fill("#q", "超分子")
        await pg.wait_for_timeout(800)
        shown2 = await pg.inner_text("#shown")
        await pg.fill("#q", "")
        await pg.wait_for_timeout(500)
        # test school tab (Nankai)
        await pg.click("#schooltabs button[data-school='nankai']")
        await pg.wait_for_timeout(800)
        shown3 = await pg.inner_text("#shown")
        await pg.screenshot(path=r"D:\USTC-AI\chem-faculty\work\screenshot.png", full_page=False)
        print("shown:", shown, "| schcount:", schcount, "| cards:", cards)
        print("tabs:", tabs[:6])
        print("search 超分子 ->", shown2)
        print("nankai tab ->", shown3)
        print("JS errors:", errors[:5] if errors else "none")
        await b.close()

asyncio.run(main())

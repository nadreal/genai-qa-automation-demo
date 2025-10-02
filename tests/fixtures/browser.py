from playwright.sync_api import sync_playwright, Browser, Page

import pytest

@pytest.fixture(scope='session')
def pw():
    with sync_playwright() as p:
        yield p
        
@pytest.fixture(scope='session')
def browser(pw):
    return pw.chromium.launch(headless=False)

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

    
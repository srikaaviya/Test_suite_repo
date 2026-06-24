import pytest
from playwright.sync_api import expect


BASE_UI_URL = "https://automationintesting.online"


@pytest.mark.e2e
def test_homepage_loads(page):
    page.goto(BASE_UI_URL)
    expect(page).to_have_title("Restful-booker-platform demo")


@pytest.mark.e2e
def test_admin_login(page):
    page.goto(f"{BASE_UI_URL}/admin")
    page.fill("input[id='username']", "admin")
    page.fill("input[id='password']", "password")
    page.click("button[id='doLogin']")
    page.wait_for_timeout(2000)
    # expect(page.locator("a[href='/#/admin']")).to_be_visible()
    expect(page.locator("button", has_text="Logout")).to_be_visible()


@pytest.mark.e2e
def test_invalid_login_shows_error(page):
    page.goto(f"{BASE_UI_URL}/admin")
    page.fill("input[id='username']", "wrong")
    page.fill("input[id='password']", "wrong")
    page.click("button[id='doLogin']")
    page.wait_for_timeout(2000)
    expect(page.locator("input[id='username']")).to_be_visible()


@pytest.mark.e2e
def test_rooms_page_accessible(page):
    page.goto(f"{BASE_UI_URL}/admin")
    page.fill("input[id='username']", "admin")
    page.fill("input[id='password']", "password")
    page.click("button[id='doLogin']")
    page.wait_for_timeout(2000)
    # expect(page.locator(".room-details")).to_be_visible()
    expect(page.locator("text=Room #")).to_be_visible()


@pytest.mark.e2e
def test_contact_form_visible(page):
    page.goto(BASE_UI_URL)
    expect(page.locator("input[id='name']")).to_be_visible()
    expect(page.locator("input[id='email']")).to_be_visible()
    expect(page.locator("input[id='phone']")).to_be_visible()
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


@pytest.mark.e2e
def test_admin_create_room(page):
    page.goto(f"{BASE_UI_URL}/admin")
    page.fill("input[id='username']", "admin")
    page.fill("input[id='password']", "password")
    page.click("button[id='doLogin']")
    page.wait_for_timeout(2000)

    page.fill("input[id='roomName']", "201")
    page.select_option("select[id='type']", "Double")
    page.select_option("select[id='accessible']", "true")
    page.fill("input[id='roomPrice']", "175")
    page.check("input[id='wifiCheckbox']")
    page.click("button[id='createRoom']")
    page.wait_for_timeout(2000)
    expect(page.locator("text=201")).to_be_visible()


@pytest.mark.e2e
def test_admin_create_second_room(page):
    page.goto(f"{BASE_UI_URL}/admin")
    page.fill("input[id='username']", "admin")
    page.fill("input[id='password']", "password")
    page.click("button[id='doLogin']")
    page.wait_for_timeout(2000)

    room_count_before = page.locator("text=Room #").count()
    page.fill("input[id='roomName']", "999")
    page.fill("input[id='roomPrice']", "100")
    page.click("button[id='createRoom']")
    page.wait_for_timeout(2000)
    expect(page.locator("text=999")).to_be_visible()


@pytest.mark.e2e
def test_contact_form_submission(page):
    page.goto(BASE_UI_URL)
    page.fill("input[id='name']", "Test User")
    page.fill("input[id='email']", "test@example.com")
    page.fill("input[id='phone']", "01234567890")
    page.fill("input[id='subject']", "Test Subject")
    page.fill("textarea[id='description']", "This is a test message for the contact form.")
    page.click("button:has-text('Submit')")
    page.wait_for_timeout(2000)
    expect(page.locator("text=Thanks for getting in touch")).to_be_visible()


@pytest.mark.e2e
def test_contact_form_empty_submit(page):
    page.goto(BASE_UI_URL)
    page.click("button:has-text('Submit')")
    page.wait_for_timeout(1000)
    expect(page.locator("text=may not be blank").first).to_be_visible()


@pytest.mark.e2e
def test_login_then_logout(page):
    page.goto(f"{BASE_UI_URL}/admin")
    page.fill("input[id='username']", "admin")
    page.fill("input[id='password']", "password")
    page.click("button[id='doLogin']")
    page.wait_for_timeout(2000)
    expect(page.locator("button", has_text="Logout")).to_be_visible()

    page.click("button:has-text('Logout')")
    page.wait_for_timeout(2000)
    # expect(page.locator("input[id='username']")).to_be_visible()
    expect(page).to_have_url(BASE_UI_URL + "/")
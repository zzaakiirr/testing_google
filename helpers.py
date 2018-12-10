import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def is_results_page_loads(driver, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "resultStats"))
        )
    except TimeoutException:
        return False
    return True


def scroll_to_the_page_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)


def get_screen_keyboard(driver):
    try:
        screen_keyboard = driver.find_element_by_id("kbd")
    except NoSuchElementException:
        return None
    return screen_keyboard


def is_symbol_button_click_puts_symbol_to_search_input(
        search_input_field, symbol_button, extra_symbols):
    try:
        symbol = symbol_button.find_element_by_css_selector("*")
    except NoSuchElementException:
        pass
    else:
        if symbol_button in extra_symbols:
            return True, None
        symbol_button.click()
        expected_symbol = symbol.get_attribute("innerHTML")
        entered_symbol = search_input_field.get_attribute("value")
        if not entered_symbol == expected_symbol:
            return False, "Expected '{}', but entered '{}'".format(
                expected_symbol, entered_symbol
            )
        search_input_field.clear()
        search_input_field.click()
    return True, None

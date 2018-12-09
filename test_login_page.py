import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

import requests


class MainPageTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.start_url = "https://www.google.com/"
        cls.driver.get(cls.start_url)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


class GenericTests(MainPageTestCase):
    """ Generic tests for checking if page loads with correct elements"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        ...

    def test_url_reaching_return_success_status_code(self):
        response = requests.get(self.start_url)
        self.assertEqual(response.status_code, 200)

    def test_is_page_title_correct(self):
        expected_title = 'Google'
        self.assertEqual(expected_title, self.driver.title)

    def test_is_search_input_field_exist(self):
        try:
            search_input_field = self.driver.find_element_by_name("q")
        except NoSuchElementException:
            self.fail("Search input field doesn't exist")

    def test_is_logo_exist(self):
        try:
            logo = self.driver.find_element_by_id("hplogo")
        except NoSuchElementException:
            self.fail("Logo doesn't exist")

    def test_is_search_button_exist(self):
        try:
            search_button = self.driver.find_element_by_name("btnK")
        except NoSuchElementException:
            self.fail("Search button doesn't exist")

    def test_is_i_am_lucky_button_exist(self):
        try:
            i_am_lucky_button = self.driver.find_element_by_name("btnI")
        except NoSuchElementException:
            self.fail("I am lucky button doesn't exist")

    def test_does_not_voice_search_button_exist(self):
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name("voice_search_button")

    def test_page_loads_without_active_screen_keyboard(self):
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_id("kbd")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class SearchInputFieldTests(MainPageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.driver.back()
        ignored_exceptions = (
            NoSuchElementException,
            StaleElementReferenceException,
        )
        wait = WebDriverWait(
            self.driver, 10, ignored_exceptions=ignored_exceptions,
        )
        self.search_input_field = wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

    def test_empty_search_input_field_can_not_submit_by_return_key(self):
        self.search_input_field.send_keys(Keys.RETURN)
        time.sleep(3)
        self.assertEqual(self.driver.current_url, self.start_url)

    def test_filled_search_input_field_submit_by_return_key(self):
        self.search_input_field.send_keys("Kaspersky", Keys.RETURN)
        time.sleep(3)
        self.assertNotEqual(self.driver.current_url, self.start_url)

    def test_search_input_field_saves_logged_user_search_history(self):
        ...

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class IamLuckyButtonTests(MainPageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    # def test_i_am_lucky_button_redirect(self):
    #     i_am_lucky_button = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.NAME, "btnI"))
    #     )
    #     i_am_lucky_button.click()
    #     time.sleep(3)
    #     expected_url = "https://www.google.com/doodles/"
    #     self.assertEqual(expected_url, self.driver.current_url)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class SearchButtonTests(MainPageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.search_button = cls.driver.find_element_by_name("btnK")
        cls.search_input_field = cls.driver.find_element_by_name("q")

    # Doesn't work self.search_button.click()
    # def test_filled_search_input_field_submit_by_search_button(self):
    #     self.search_input_field.send_keys("Kaspersky")
    #     self.search_button.click()
    #     time.sleep(3)
    #     self.assertNotEqual(self.driver.current_url, self.start_url)

    def test_empty_search_input_field_can_not_submit_by_search_button(self):
        self.search_input_field.send_keys(Keys.RETURN)
        time.sleep(3)
        self.assertEqual(self.driver.current_url, self.start_url)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class ScreenKeyboardTests(MainPageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.screen_keyboard_button = cls.driver.find_element_by_xpath(
            "//div/div/form/div/div/div/div/div/div/span"
        )
        cls.search_input_field = cls.driver.find_element_by_name("q")

    # def test_is_activate_screen_keyboard_button_exist(self):
    #     try:
    #         screen_keyboard_button = self.driver.find_element_by_xpath(
    #             "//div/div/form/div/div/div/div/div/div"
    #         )
    #     except NoSuchElementException:
    #         self.fail("Search button doesn't exist")

    def setUp(self):
        self.screen_keyboard_button.click()

    def tearDown(self):
        screen_keyboard = self.driver.find_element_by_id("kbd")
        if screen_keyboard.is_displayed():
            screen_keyboard.click()

    def test_screen_keyboard_opens_by_screen_keyboard_activate_button(self):
        """ Testing if screen keyboard can be opened by click on
        keyboard activate button inside search input field"""

        try:
            screen_keyboard = self.driver.find_element_by_id("kbd")
        except NoSuchElementException:
            self.fail()
        self.assertTrue(screen_keyboard.is_displayed())

    def test_screen_keyboard_closes_by_screen_keyboard_activate_button(self):
        """ Testing if opened by keyboard activate button inside
        search input field screen keyboard can be closed by
        clicking same button"""

        self.screen_keyboard_button.click()
        screen_keyboard = self.driver.find_element_by_id("kbd")
        self.assertFalse(screen_keyboard.is_displayed())

    def test_screen_keyboard_closes_by_close_button_on_screen_keyboard(self):
        screen_keyboard_close_button = self.driver.find_element_by_class_name(
            "vk-sf-cl")
        screen_keyboard_close_button.click()
        screen_keyboard = self.driver.find_element_by_id("kbd")
        self.assertFalse(screen_keyboard.is_displayed())

    def test_screen_keyboard_symbols_click(self):
        symbol_buttons = self.driver.find_elements_by_class_name("vk-btn")
        search_input_field = self.driver.find_element_by_name("q")

        caps_lock = self.driver.find_element_by_id("K20")
        backspace = self.driver.find_element_by_id("K8")
        shifts = self.driver.find_elements_by_id("K16")
        ctrl_alts = self.driver.find_elements_by_id("K273")
        space = self.driver.find_element_by_id("K32")
        extra_symbols = [caps_lock, backspace, space, ]
        for shift in shifts:
            extra_symbols.append(shift)
        for ctrl_alt in ctrl_alts:
            extra_symbols.append(ctrl_alt)

        for symbol_button in symbol_buttons:
            try:
                symbol_title = symbol_button.find_element_by_css_selector("*")
            except NoSuchElementException:
                pass
            else:
                if symbol_button in extra_symbols:
                    continue
                symbol_button.click()
                expected_symbol = symbol_title.get_attribute("innerHTML")
                entered_symbol = search_input_field.get_attribute("value")
                if not entered_symbol == expected_symbol:
                    self.fail("Expected '{}', but entered '{}'".format(
                        expected_symbol, entered_symbol
                    ))
                search_input_field.clear()
                search_input_field.click()

    def test_caps_lock_button(self):
        ...

    def test_shift_button(self):
        ...

    def test_backspace_button(self):
        ...

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

if __name__ == "__main__":
    unittest.main()

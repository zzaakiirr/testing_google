import unittest
import time

import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains

from screen_keyboard_tests_helpers import (
    is_symbol_button_click_put_symbol_to_search_input,
    scroll_to_the_page_bottom,
    is_results_page_loads,
)


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
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.expected_title = 'Google'

    def test_is_page_title_correct(self):
        self.assertEqual(self.expected_title, self.driver.title)


class SearchInputFieldTests(MainPageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.search_input_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

    def test_empty_search_input_field_can_not_be_submited_by_return_key(self):
        self.search_input_field.send_keys(Keys.RETURN)
        self.assertFalse(is_results_page_loads(self.driver))

    def test_filled_search_input_field_submit_by_return_key(self):
        self.search_input_field.send_keys("Kaspersky", Keys.RETURN)
        self.assertTrue(is_results_page_loads(self.driver))

    # TO DO:
    def test_search_input_field_saves_logged_user_search_history(self):
        ...

    def tearDown(self):
        self.driver.back()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class IamLuckyButtonTests(MainPageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    # TO DO:
    def test_i_am_lucky_button_redirect(self):
        ...

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class SearchButtonTests(MainPageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.search_button = cls.driver.find_element_by_name("btnK")
        cls.search_input_field = cls.driver.find_element_by_name("q")

    def test_filled_search_input_field_submit_by_search_button(self):
        self.search_input_field.send_keys("Kaspersky")
        scroll_to_the_page_bottom(self.driver)
        self.search_button.click()
        self.assertTrue(is_results_page_loads(self.driver))

    # TO DO:
    def test_empty_search_input_field_cant_be_submited_by_search_button(self):
        ...

    def tearDown(self):
        self.driver.back()

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

        # Need to FIX:
        # cls.caps_lock = cls.driver.find_element_by_id("K20")
        # cls.backspace = cls.driver.find_element_by_id("K8")
        # cls.shifts = cls.driver.find_elements_by_id("K16")
        # cls.ctrl_alts = cls.driver.find_elements_by_id("K273")
        # cls.space = cls.driver.find_element_by_id("K32")

    def test_page_loads_without_active_screen_keyboard(self):
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_id("kbd")

    # def setUp(self):
    #     self.russian_e_button = self.driver.find_element_by_id("K192")

    def test_screen_keyboard_opens_by_screen_keyboard_activate_button(self):
        """ Testing if screen keyboard can be opened by click on
        keyboard activate button inside search input field"""

        self.screen_keyboard_button.click()
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
        self.screen_keyboard_button.click()
        screen_keyboard = self.driver.find_element_by_id("kbd")
        self.assertFalse(screen_keyboard.is_displayed())

    def test_screen_keyboard_closes_by_close_button_on_screen_keyboard(self):
        screen_keyboard_close_button = self.driver.find_element_by_class_name(
            "vk-sf-cl")
        screen_keyboard_close_button.click()
        screen_keyboard = self.driver.find_element_by_id("kbd")
        self.assertFalse(screen_keyboard.is_displayed())

    def get_extra_symbols(self):
        extra_symbols = [self.caps_lock, self.backspace, self.space, ]
        for shift in self.shifts:
            extra_symbols.append(shift)
        for ctrl_alt in self.ctrl_alts:
            extra_symbols.append(ctrl_alt)

        return extra_symbols

    def test_screen_keyboard_symbols_click(self):
        symbol_buttons = self.driver.find_elements_by_class_name("vk-btn")
        extra_symbols = self.get_extra_symbols()

        for symbol_button in symbol_buttons:
            no_error, error_message = (
                is_symbol_button_click_put_symbol_to_search_input(
                    self.search_input_field, symbol_button, extra_symbols,
                ))
            if not no_error:
                self.fail(error_message)

    def test_screen_keyboard_caps_lock_button(self):
        self.caps_lock.click()
        self.russian_e_button.click()
        entered_symbol = self.search_input_field.get_attribute("value")
        self.assertEqual(entered_symbol, "Ё")

    def test_screen_keyboard_shifts_upper_only_first_entered_symbol(self):
        for shift in self.shifts:
            shift.click()
            self.russian_e_button.click()
            self.russian_e_button.click()
            entered_symbol = self.search_input_field.get_attribute("value")
            if not entered_symbol == "Ёё":
                self.fail()
            self.search_input_field.clear()
            self.search_input_field.click()

    def test_screen_keyboard_backspace_button(self):
        test_value = "Касперский"
        self.search_input_field.send_keys(test_value)
        self.backspace.click()
        returned_result = self.search_input_field.get_attribute("value")
        expected_result = test_value[:-1]
        self.assertEqual(returned_result, expected_result)

    def test_screen_keyboard_space_button(self):
        self.space.click()
        entered_symbol = self.search_input_field.get_attribute("value")
        self.assertEqual(entered_symbol, " ")

    def tearDown(self):
        try:
            screen_keyboard = self.driver.find_element_by_id("kbd")
        except NoSuchElementException:
            pass
        else:
            if screen_keyboard.is_displayed():
                self.screen_keyboard_button.click()
        self.search_input_field.clear()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

if __name__ == "__main__":
    unittest.main()

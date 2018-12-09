import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# def is_element_exist_in_page(driver, element_xpath):
#     try:
#         driver.find_element_by_xpath(element_xpath)
#     except NoSuchElementException:
#         return False
#     return True


class MainPageTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.start_url = "http://www.google.com"
        cls.driver.get(cls.start_url)
        # cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


class GenericTests(MainPageTestCase):
    """  """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        ...

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

    def test_is_not_voice_search_button_exist(self):
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name("voice_search_button")

    def test_page_loads_without_active_screen_loupe(self):
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_id("kbd")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class SearchInputFieldTests():
    ...


class IamFeelingLuckyButtonTests():
    ...


class SearchButtonTests(unittest.TestCase):
    """  """

    def test_filled_search_input_field_submitting_by_button(self):
        ...

    def test_filled_search_input_field_submitting_by_enter_key(self):
        ...


class ScreenKeyboardTests(unittest.TestCase):
    """  """

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.start_url = "http://www.google.com"
        cls.driver.get(cls.start_url)
        # cls.driver.implicitly_wait(10)

    # def test_screen_loupe_button(self):

    # def test_close_screen_loupe_close_button(self):
        # wait = WebDriverWait(driver, 10)
        # self.driver.implicitly_wait(10)
        # self.assertEqual(self.start_url, self.driver.current_url)
    # def test_search_field_exist(self):

    # def test_search_in_python_org(self):
    #     #Load the main page. In this case the home page of Python.org.
    #     main_page = page.MainPage(self.driver)
    #     #Checks if the word "Python" is in title
    #     assert main_page.is_title_matches(), "python.org title doesn't match."
    #     #Sets the text of search textbox to "pycon"
    #     main_page.search_text_element = "pycon"
    #     main_page.click_go_button()
    #     search_results_page = page.SearchResultsPage(self.driver)
    #     #Verifies that the results page is not empty
    #     assert search_results_page.is_results_found(), "No results found."

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    # def tearDown(self):
    #     self.driver.close()

if __name__ == "__main__":
    unittest.main()

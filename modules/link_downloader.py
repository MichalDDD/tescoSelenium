from selenium import webdriver


class LinkDownloader:
    def __init__(self, pages: list):
        self.pages: dict = {el:0 for el in pages}
        self.driver = webdriver.Firefox()

    def check_dict(self, el, branch: str):
        """
        method used to verify if current element in loop is one of the requested
        :param el: html element of a certain product category
        :param branch: level of branch in product categories tree department/aisle/shelf
        :return:
        """
        for page in self.pages.keys():
            if page.lower() == el.text.replace('All ', '').replace('Shop\n','').replace(f'\n{branch}','').lower():
                self.pages[page] = el.get_attribute('href')

    def get_links(self) -> dict:
        """
        method used to navigate to tesco groceries tree and navigate through all the branches and leaves finding url links for requested product categories
        :return dict:
        """
        self.driver.get('https://www.tesco.com/groceries/en-GB/')
        menu_elements = self.driver.find_elements_by_css_selector('a.menu__link')
        for el in menu_elements:
            self.check_dict(el, 'department')
            el.click()
            first_element_flag = False
            dep_items = self.driver.find_element_by_class_name('menu').find_elements_by_css_selector('a.menu__link--department')
            for dep_el in dep_items:
                self.check_dict(dep_el, 'aisle')
                if not first_element_flag:
                    first_element_flag = True
                else:
                    dep_el.click()
                    aisle_items = self.driver.find_element_by_class_name('menu-aisle').find_elements_by_css_selector('a.menu__link--aisle')
                    for aisle_el in aisle_items:
                        self.check_dict(aisle_el, 'shelf')
        self.driver.close()
        return self.pages
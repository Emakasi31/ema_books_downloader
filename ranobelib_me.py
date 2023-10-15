"""
This file provides functions for download and format books from ranobelib.me
"""
from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException


def initiate_display(body) -> None:
    """
    Initiate driver and display,
    close after execution
    """

    def selenium_and_display_settings(*args, **kwargs) -> None:
        display = Display(visible=0, size=(800, 600))
        options = webdriver.FirefoxOptions()
        service = Service(executable_path="/usr/local/bin/geckodriver")
        service_log_path = "/dev/null"
        options.add_argument("--headless")  # turn off display for docker
        driver = webdriver.Firefox(
            options=options, service=service, service_log_path=service_log_path
        )
        url = str(input("input url: "))  # parser's target
        display.start()
        driver.get(url)
        body(driver, *args, **kwargs)
        driver.quit()
        display.stop()

    return selenium_and_display_settings


def close_age_warning(driver) -> None:
    """
    Alert may not appear, but if it does
    runs a delay for loading page after click confirm
    """
    try:
        driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[2]/div/button[2]"
        ).click()
    except (NoSuchElementException, ElementNotInteractableException):
        sleep(0.25)


def write_page_to_file(driver, book_name) -> None:
    """Append page's text to the file"""
    container = driver.find_element_by_class_name("reader-container")
    with open(f"{book_name}.txt", "a+", encoding="utf-8") as file:
        file.write(container.text + "\n\n\n")


def return_status(driver, page_counter) -> None:
    """Print in stdout page's number"""
    cur_url = driver.current_url
    print(f"{cur_url} {page_counter} download")


def remove_trash(book_name):
    """Remove the target string"""
    print("removing trash")
    with open("ranobelib_ignore.txt", "r", encoding="utf-8") as ignore_file:
        ignore_lines = ignore_file.readlines()  # creates a list from ignore file

    with open(f"{book_name}.txt", "r", encoding="utf-8") as file:
        filedata = file.read()  # reads data from the book

    for line in ignore_lines:
        filedata = filedata.replace(line, "")  # deletes lines from the list above

    with open(f"{book_name}.txt", "w", encoding="utf-8") as file:
        file.write(filedata)  #  rewrites the book with updated data


def bypass_cloudflare(driver) -> None:
    """Delay allows to deal < 5 requests per sec"""
    sleep(0.25)
    driver.delete_all_cookies()


def swith_page(driver) -> bool:
    """
    Swich to the next page button and returns a bool
    to detect the end of the book
    """
    try:
        fa_angle = driver.find_element_by_class_name("fa-angle-right")
    except NoSuchElementException:
        return False
    try:
        fa_angle.click()
    except ElementClickInterceptedException:
        return False
    return True


@initiate_display
def parse(driver) -> None:
    """
    Main function defines variables, does
    some things and exit when can't switch page
    """
    book_name = str(input("input book's name: "))
    with open(f"{book_name}.txt", "a+", encoding="utf-8") as file:
        file.write(f"{book_name}\n\n")  # create books file
    page_counter = 1
    while True:
        close_age_warning(driver)
        write_page_to_file(driver, book_name)
        return_status(driver, page_counter)
        bypass_cloudflare(driver)
        if swith_page(driver) is False:
            break
        page_counter += 1
    remove_trash(book_name)


if __name__ == "__main__":
    parse()  # pylint: disable=no-value-for-parameter

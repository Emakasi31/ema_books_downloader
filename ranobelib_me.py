from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException
import fileinput
from time import sleep


def initiate_display(body):
    def selenium_and_display_settings(*args, **kwargs):
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
        driver.close()
        display.stop()

    return selenium_and_display_settings


def remove_trash(trash, book_name):
    # Remove the target string
    with open("{0}.txt".format(book_name), "r") as file:
        filedata = file.read()
    filedata = filedata.replace(str(trash), "")
    with open("{0}.txt".format(book_name), "w") as file:
        file.write(filedata)
    file.close()


def trash_list(book_name):
    remove_trash(
        "Внимание! Эта манга может содержать ненормативную лексику, сексуальные сцены откровенного характера, а также художественное изображение жестокости и насилия и ux cлoвecныe oпucaнuя.\n",
        book_name,
    )
    remove_trash("Больше не показывать\n", book_name)


def swith_page(driver) -> bool:
    try:
        fa_angle = driver.find_element_by_class_name("fa-angle-right")
    except NoSuchElementException:
        return False
    fa_angle.click()
    return True


def close_age_warning(driver) -> None:
    try:
        driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[2]/div/button[2]"
        ).click()
    except Exception:
        pass
        sleep(0.25)  # delay for load page after alert


def return_status(driver, page_counter) -> None:
    cur_url = driver.current_url
    print(cur_url + " %d download" % (page_counter))


def bypass_cloudflare(driver) -> None:
    sleep(0.25)  # this delay allows to deal < 5 requests per sec
    driver.delete_all_cookies()


def write_page_to_file(driver, file) -> None:
    container = driver.find_element_by_class_name("reader-container")
    file.write(container.text + "\n\n\n")


@initiate_display
def parse(driver):
    book_name = str(input("input book's name: "))
    file = open("{0}.txt".format(book_name), "a+")
    file.write("{0}\n".format(book_name) + "\n\n")
    page_counter = 1
    while True:
        close_age_warning(driver)
        write_page_to_file(driver, file)
        return_status(driver, page_counter)  # print in stdout
        trash_list(book_name)
        bypass_cloudflare(driver)
        if swith_page(driver) == False:
            break
        page_counter += 1
    file.close()
    trash_list(book_name)


if __name__ == "__main__":
    parse()

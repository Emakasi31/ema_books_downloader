from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from pyvirtualdisplay import Display
from time import sleep


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
        # parser's target
        url = "https://yandex.ru/pogoda/ru-RU/moscow/details?lat=55.80794357615003&lon=37.822795413136696"
        display.start()
        driver.get(url)
        body(driver, *args, **kwargs)
        driver.quit()
        display.stop()

    return selenium_and_display_settings


@initiate_display
def parse(driver) -> None:
    """print weather"""
    try:
        morning = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[1]/main/div[2]/article[1]/div[1]"
        ).text
        afternoon = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[1]/main/div[2]/article[1]/div[7]"
        ).text
        evening = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[1]/main/div[2]/article[1]/div[13]"
        ).text
        night = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[1]/main/div[2]/article[1]/div[19]"
        ).text
    except Exception as e:
        print(e)
    res = f"{morning}\n{afternoon}\n{evening}\n{night}"
    print(res)
    with open("weather.txt", "w", encoding="utf-8") as file:
        file.write(res)
    return None


if __name__ == "__main__":
    parse()
    sleep(600)


# /html/body/div[1]/div/div/div[1]/main/div[2]/article[1]/div[1]/div

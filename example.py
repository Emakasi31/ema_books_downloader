from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from pyvirtualdisplay import Display
#from time import sleep

display = Display(visible=0, size=(800, 600))
options = Options()
service = Service(executable_path = "/usr/local/bin/geckodriver")
options.add_argument('--headless') #disable display for docker
driver = webdriver.Firefox(options=options, service=service)

if __name__ == '__main__':
    display.start()

    driver.get('https://www.google.com/') #Space for your
    print(driver.title)                   #selenium code

    driver.quit()
    display.stop()

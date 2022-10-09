from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from pyvirtualdisplay import Display
import fileinput
from time import sleep


our_url = str(input("input url: "))
#https://lightnovels.me/i-alone-level-up/chapter-1.html
book_name = str(input("input book's name: "))
#I Alone Level-Up
display = Display(visible=0, size=(800, 600))
options = Options()
service = Service(executable_path = "/usr/local/bin/geckodriver")
options.add_argument('--headless') #disable display for docker
driver = webdriver.Firefox(options=options, service=service)

if __name__ == '__main__':
    display.start()
    driver.get(our_url)
    sleep(1)
    driver.find_element_by_xpath("/html/body/div/div/main/div[3]/div[1]/div/div/button").click()
    our_file = open('{0}.txt'.format(book_name), 'a+')
    our_file.write('{0}\n'.format(book_name)+'\n\n')
    for charapter in range(1, 10000):
        cur_url = driver.current_url
        container = driver.find_element_by_class_name("chapter-content")
        our_file.write(container.text+'\n\n\n')
        print(cur_url +  ' %d download' % (charapter))
        driver.delete_all_cookies()
        sleep(1)
        try:
            fa_angle = driver.find_element_by_xpath("/html/body/div/div/main/div[2]/div[2]/div[1]/div[1]/div[3]/div").click() #click next page
        except Exception as e:
            break
        sleep(1) #delay for close registration alert, you can change value if your internet connetion is faster or even slower
        try:
            driver.find_element_by_xpath("/html/body/div/div/main/div[3]/div[1]/div/div/button").click() #close registration alert
        except Exception  as J:
            print(J)
    our_file.close()
    driver.quit()
    display.stop()

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import fileinput
from time import sleep

display = Display(visible=0, size=(800, 600))
options = webdriver.FirefoxOptions()
service = Service(executable_path = "/usr/local/bin/geckodriver")
options.add_argument('--headless') #turn off display for docker
driver = webdriver.Firefox(options=options, service=service)
our_url = str(input("input url: "))
#https://ranobelib.me/arifureta-shokugyou-de-sekai-saikyou-novel/v1/c0
book_name = str(input("input book's name: "))
#arifureta

def remove_trash(trash):
    ### Remove the target string
    with open('{0}.txt'.format(book_name), 'r') as file :
        filedata = file.read()
    filedata = filedata.replace(str(trash), '')
    with open('{0}.txt'.format(book_name), 'w') as file:
        file.write(filedata)
    file.close()

def trash_list():
    remove_trash('Внимание! Эта манга может содержать ненормативную лексику, сексуальные сцены откровенного характера, а также художественное изображение жестокости и насилия и ux cлoвecныe oпucaнuя.\n')
    remove_trash('Больше не показывать\n')

if __name__ == '__main__':
    display.start()
    driver.get(our_url)
    our_file = open('{0}.txt'.format(book_name), 'a+')
    our_file.write('{0}\n'.format(book_name)+'\n\n')
    for charapter in range(1, 10000):
        cur_url = driver.current_url
        try:
            driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/button[2]").click() #close age warning
        except Exception  as J:
            print(J)
        sleep(0.25) #delay for close warning
        container = driver.find_element_by_class_name("reader-container")
        our_file.write(container.text + '\n\n\n')
        print(cur_url +  ' %d download' % (charapter))
        trash_list()
        sleep(0.25)
        driver.delete_all_cookies()
        try:
            fa_angle = driver.find_element_by_class_name("fa-angle-right")
        except Exception:
            break
        fa_angle.click()
    our_file.close()
    trash_list()
    driver.quit()
    display.stop()

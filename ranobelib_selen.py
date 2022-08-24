from selenium import webdriver
import fileinput
from time import sleep
#from selenium.webdriver.firefox.options import Options



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


our_url = str(input("input url: "))
#https://ranobelib.ru/silnejshij-mudrets-nizshej-emblemy/glava-1-silnejshij-v-mire-mudrets/
book_name = str(input("input book's name: "))
#The Strongest Sage of Disqualified Crest
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0")
driver = webdriver.Firefox(profile, executable_path = './geckodriver')
driver.set_window_size(1920, 1080, driver.window_handles[0])


driver.get(our_url)
our_file = open('{0}.txt'.format(book_name), 'a+')
our_file.write('{0}\n'.format(book_name)+'\n\n')
for charapter in range(1, 10000):
    cur_url = driver.current_url
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

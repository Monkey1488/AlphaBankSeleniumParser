import login_password
 
import time 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from fake_useragent import UserAgent 
 
user = UserAgent() 
 
options = webdriver.ChromeOptions() 
options.add_argument("--disable-blink-features=AutomationControlled") #отключаем режим webdriver 
options.add_argument(f"user-agent={user.google}") 
 
url = "https://private.auth.alfabank.ru/passport/cerberus-mini-blue/dashboard-blue/username?response_type=code&client_id=click-web-adf&scope=openid" 
driver = webdriver.Chrome( 
    executable_path="chromedriver.exe", 
    options=options 
    ) 
 
#список подходящих номеров 
phone_list = [] 
 

try: 
    #аутентификация 
    driver.get(url=url) 
    email_input = driver.find_element_by_xpath("//input[@class='input__input_auq2t input__input_kjfbv input__hasLabel_auq2t input__hasLabel_kjfbv']") 
    email_input.clear() 
    email_input.send_keys(login_password.login) 
    email_input.send_keys(Keys.ENTER) 
    password_input = driver.find_element_by_xpath("//input[@class='input__input_auq2t input__input_kjfbv input__hasLabel_auq2t input__hasLabel_kjfbv']") 
    password_input.send_keys(login_password.password) 
    password_input.send_keys(Keys.ENTER) 
    time.sleep(20) #время на введение пароля из sms 
    driver.get(url=url) #обновляем страницу для перехода на старую версию сайта 
    #переход по вкладкам до страницы с вводом номеров 
    driver.implicitly_wait(5)
    first_button = driver.find_element_by_id("pt1:menu:ATP2_r1:0:i1:5:cl2").find_element_by_tag_name("span").click() 
    driver.implicitly_wait(5) 
    second_button = driver.find_element_by_id("pt1:i2:1:i1:1:ot101").click() 
    time.sleep(2) 
 
     
# перебор номеров 
    for i in range(79969467119, 79969469999): 
        phone_input = driver.find_elements_by_class_name("xpq")[0].find_element_by_class_name("x27m")#ищем поле с вводом номеров 
        phone_input.clear() 
        phone_input.send_keys(i) 
        a = driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND) #нажимаем курсором на любую точку страницы, для отображения на сайте окна с ошибкой 
        driver.implicitly_wait(2) #неявное ожидание появления окна 
        try: 
            #если номер не подходит, то всплывает надпись: "Получатель не найден, проверьте введенные данные" 
            b = driver.find_element_by_class_name("x15g").text 
            if b.split(" ")[0] == "Получатель": 
                pass 
        except: 
            pass 
        try: 
            # НО, если всплывает надпись "Внимание! Этому клиенту невозможно сделать перевод по контактным данным. Пожалуйста, укажите номер счета и ФИО клиента.", то номер подходит 
            c = driver.find_element_by_class_name("x15g").text.split(" ")[0] 
            if c.split(" ")[0] == "Внимание!": 
                phone_list.append(i) 
                print("YES", str(i)) 
        except: 
            #если всплывающее окно не найдено, значит номер подходит 
            print("YES", i) 
            phone_list.append(i) 
   
except Exception as ex: 
    print(ex) 
finally: 
    driver.close() 
    driver.quit() 
    print(phone_list) 
    with open("79969460000-79969469999.txt", "a") as final_file:
        for i in phone_list:
            final_file.write(str(i) + "\n")
 
#нужно добавить в список phone_list все номера, кроме тех, из-за который всплывает надпись: "Получатель не найден, проверьте введенные данные"
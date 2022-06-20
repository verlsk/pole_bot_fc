from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

import sys
import time

driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())

# Pagina de login
driver.get('https://www.forocoches.com/foro/misc.php?do=page&template=ident')
# time.sleep(1)
# Aceptar cookies
# driver.find_element_by_link_text("Accept all").click()
# time.sleep(2)
# Usuario y pass
element = driver.find_element(By.ID, "navbar_username")
element.send_keys(sys.argv[1])
element = driver.find_element(By.ID, "navbar_password")
element.send_keys(sys.argv[2])
element.send_keys(Keys.RETURN)
timeout = 1000
element_present = EC.presence_of_element_located((By.LINK_TEXT, sys.argv[1]))
WebDriverWait(driver, timeout).until(element_present)

start_num = int(sys.argv[3])

while 1:
    # Acceder al post
    driver.get('https://www.forocoches.com/foro/showthread.php?t=' + str(start_num))
    try:
        # Extraer el titulo del post
        title = driver.find_element_by_class_name("cmega").text
        # Comprobar si el tema es serio o no
        if "serio" in title or "Serio" in title or "+serio" in title or "+Serio" in title:
            # Tema serio. No se polea
            print("Tema serio. No se polea")
            start_num += 1
        else:
            n_posts = len(driver.find_element_by_id("posts").find_elements_by_xpath("./*")) - 1
            print(n_posts)
            if n_posts == 1:
                # Polear
                driver.find_element_by_id("vB_Editor_QR_textarea").send_keys(sys.argv[4])
                driver.find_element_by_id("qr_submit").click()
                time.sleep(30)
                start_num += 1
                print("Hilo poleado")
            elif n_posts > 1:
                # Pasar al siguiente hilo
                print("El hilo ya está poleado. Pasamos al siguiente")
                start_num += 1
    except:
        try:
            text_shown = driver.find_element_by_class_name("panelsurround").find_element_by_tag_name("center").text
            if text_shown.split(" ")[0] == "Tema":
                # Tema borrado
                start_num += 1
                print("Tema borrado. Pasar al siguiente.")
            else:
                # Tema no abierto
                print("Tema por abrir. Esperando para polear...")
        except:
            print("Tema por abrir. Esperando para polear...")
    time.sleep(1.5)

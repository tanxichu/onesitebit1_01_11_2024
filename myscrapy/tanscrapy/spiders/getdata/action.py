from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys  # Import Keys here

def perform_action(driver, locator_type, element_identifier, action, input_text="", time=0, index=0,secondcss="",second_identifier=""):
    
    if locator_type == "selector":
        by_locator = By.CSS_SELECTOR
    elif locator_type == "id":
        by_locator = By.ID
    elif locator_type == "class":
        by_locator =By.CLASS_NAME

    by_locator_second=""
    if secondcss == "selector":
        by_locator_second = By.CSS_SELECTOR
    elif secondcss == "id":
        by_locator_second = By.ID
    elif secondcss == "class":
        by_locator_second =By.CLASS_NAME
    
    
    clickaction = """
        function jsClick(element) {
            var clickEvent = new MouseEvent('click', {
                'view': window,
                'bubbles': true,
                'cancelable': true
            });
            element.dispatchEvent(clickEvent);
        }
        """

    try:
        elements = WebDriverWait(driver, time).until(
            # 注传入的是一个元组，所以要二个括号
            EC.presence_of_all_elements_located((by_locator, element_identifier))
        )

        if index < len(elements):
            element = elements[index]  # Use the element at the specified index
            if action == "click":
                element = WebDriverWait(driver, time).until(
                    # 注传入的是一个元组，所以要二个括号
                    EC.element_to_be_clickable((by_locator, element_identifier))
                )
                driver.execute_script(clickaction + "jsClick(arguments["+ str(index) + "]);", element)

              

            elif action == "input":
                #perform_action(self.driver, "id", "token-search-input","input",input_text="AMP",time=10)

                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((by_locator, element_identifier))
                )

                # 逐个字符输入，模拟慢速输入
                for char in input_text:
                    element.send_keys(char)
                    sleep(0.0001)  # 每个字符之间增加一小段延迟

            elif action == "enter":
                element = WebDriverWait(driver, time).until(
                    EC.element_to_be_clickable((by_locator, element_identifier))
                )

                while True:
                    try:
                        # 检查元素是否仍然存在，并等待 0.1 秒
                        WebDriverWait(driver, 0.1).until(
                            EC.presence_of_element_located((by_locator_second, second_identifier))
                        )
                        element.send_keys(Keys.ENTER)  # 再次尝试发送 Enter 键
                    except TimeoutException :
                        # 如果元素不再可见，则退出循环
                        break

            #price = perform_action(self.driver, "class", "token-amount-input","getdata",time=10)        
            elif action == "getprice":
                elements = WebDriverWait(driver, time).until(
                    EC.presence_of_all_elements_located((by_locator, element_identifier))
                )
                element = elements[index]
                WebDriverWait(driver, time).until(
                        lambda driver: element.get_attribute('value') not in [None, '', '0']
                )
                price = element.get_attribute('value')
                return price
            
      
            elif action == "gettext":
                elements = WebDriverWait(driver, time).until(
                    EC.presence_of_all_elements_located((by_locator, element_identifier))
                )
                while True:
                    if elements[index].text:
                        return elements[index].text
                    else:
                        sleep(0.01)
               
            
                
        else:
            raise ValueError(f"Index {index} is out of bounds for matching elements.")

    except Exception as e:
        print(f"An error occurred: {e}")


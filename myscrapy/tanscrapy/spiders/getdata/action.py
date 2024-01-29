from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys  # Import Keys here

def perform_action(driver, locator_type, element_identifier="", action="", input_text="", time=10, index=0, search_text=""):
    try:
        '''
        WebDriverWait(driver, 20).until 这是第一个循环条件，它接着一个函数。
        它会不断的检测下面的函数是否返回ture或false。
        本例中，EC是上面定义的。import expected_conditions as EC
        EC有多个内置函数，包括下面的。
        WebDriverWait 与 Expected Conditions（EC）结合使用时，EC 提供了多种预定义的条件来处理常见的等待场景。例如：
        EC.presence_of_element_located: 等待直到指定的元素加载到DOM中，但不一定可见。
        EC.visibility_of_element_located: 等待直到指定的元素不仅出现在DOM中，而且可见。
        EC.element_to_be_clickable: 等待直到元素可见且可点击。
        EC.invisibility_of_element_located: 等待直到元素不再可见。
        EC.text_to_be_present_in_element: 等待直到指定元素的文本出现特定的内容。
        在实际应用用可以自定义一个函数，返boolean即可。 
        '''
        '''
        首先定位这个元素。定位方法如下：
        1）是否存在element_identifier，即是不是通过id或class等定位的，因有一些直接通过文字内容定位的
        2）是不是存在有多个index的，
        3）有些元素是要clickable才可以的，有些是located即可以的。
        4）还有一种元素是特殊的，它不用点
        '''
        if index >0 :
            if element_identifier != "" :
                elements = WebDriverWait(driver, time).until(
                    # 注传入的是一个元组，所以要二个括号，一个是函数的，一个是元组的
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, element_identifier))
                )
                if action ==  "click":     #若要点击的，还要这个元素可点击
                    elements = WebDriverWait(driver, time).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, element_identifier))
                    )
                    element = elements[index]
                else:
                    element = elements[index]
        else:
            if element_identifier != "" :
                if action ==  "click":     #若要点击的，还要这个元素可点击
                    element = WebDriverWait(driver, time).until(
                        # 注传入的是一个元组，所以要二个括号
                        EC.element_to_be_clickable((By.CSS_SELECTOR, element_identifier))
                    )
                else:
                    # 注传入的是一个元组，所以要二个括号
                    element = WebDriverWait(driver, time).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, element_identifier))
                    )
            elif element_identifier == "" and locator_type == "find_element_by_xpath" :
                if action == "click":
                    element = WebDriverWait(driver, time).until(
                        EC.element_to_be_clickable((By.XPATH, search_text))
                    )
                else:
                     element = WebDriverWait(driver, time).until(
                        EC.visibility_of_element_located((By.XPATH, search_text))
                    )
                    
        
        #根据传入的action类型，执行不同的动作   
        if action == "click":
            # 以下clickaction其实就是一个js的函数。它是用代码模拟了一个点击的动作。注意'view'，'bubbles'，'cancelable'不能修改
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
                
            # 这个点击是针对不依CSS来点击的，它有文字的唯一性
            if locator_type == "find_element_by_xpath":
                driver.execute_script(clickaction + "jsClick(arguments[0]);", element)
                
            else:
                #此处的：arguments[0]，下标指的是element 这个传入的元素。当然，若有二个，如element1，element2，若想传入的是第二个，下标是1.
                element = WebDriverWait(driver, time).until(
                    # 注传入的是一个元组，所以要二个括号
                    EC.element_to_be_clickable((By.CSS_SELECTOR, element_identifier))
                )
                driver.execute_script(clickaction + "jsClick(arguments[0]);", element)
  
        elif action == "input":
            # 逐个字符输入，模拟慢速输入
            for char in input_text:
                element.send_keys(char)
                sleep(0.0001)  # 每个字符之间增加一小段延迟


        elif action == "enter":
            #因发现它点得太快不行，sleep太慢本项目又不想，所以来一个for
            while True:
                try:
                    # 检查元素是否仍然存在，并等待 0.1 秒，它和上面不同，它是第二个点击可用时再执行点击
                    element = WebDriverWait(driver, 0.1).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, element_identifier))
                    )  
                    element.send_keys(Keys.ENTER)  # 再次尝试发送 Enter 键
                except TimeoutException :
                    # 如果元素不再可见，则报错，此时退出循环
                    break

        elif action == "getprice": 
            '''
             WebDriverWait(driver, time).until是循环等待，它带一个函数，此函数可以是自定义的，返回boolean即可
             lambda是python自定义匿名函数，driver是由上一级传入的（内部指定）。time没有传。此外要显式写一个接收这个
             参数，就算是不用也要写。此处检测是否有value之意。
            '''
            WebDriverWait(driver, time).until(
                lambda driver: element.get_attribute('value') not in [None, '', '0']
            )
            price = element.get_attribute('value')
            return price
            
        #用于通过一个父级的唯一id，获取下属的有一个特定的txt的内容， 他下面并级的txt
        elif action == "find_element_with_text":
            # 首先等待并定位到包含“Max. slippage”的元素
            max_slippage_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, search_text))
            )

            # 然后等待并找到这个元素的下一个兄弟元素，确保它也是可见的
            next_sibling = WebDriverWait(max_slippage_element, 10).until(
                EC.visibility_of_element_located((By.XPATH, "following-sibling::*[1]"))
            )
            text = next_sibling.text
            # 检查是否存在换行符，并提取第一个值，这个是针对类似  1inch类的返回时，会有二个数值，取第一个
            if '\n' in text:
                text = text.split('\n')[0]

            return text
            
    except Exception as e:
        print(f"An error occurred: {e}")     #可以返回一个手机信息


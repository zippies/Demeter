
标志一个input元素
class AnyThing(object):
    @property
    @INPUT(element_name)
    def name_input(self):
        pass


name_input.text
name_input.clear()
name_input.input("输入内容")


标志一个button元素
class AnyThing(object):
    @property
    @BUTTON(element_name)
    def new_button(self):
        pass

new_button.click()
new_button.text
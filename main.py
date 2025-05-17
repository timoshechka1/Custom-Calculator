import math

from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

Config.set("graphics", "resizable", 1)
Config.set("graphics", "width", 400)
Config.set("graphics", "height", 500)

class CustomCalculatorApp(App):
    def update_label(self):
        self.lebalboxlay.text = self.formula

    def add_number(self, instance):
        num_eval_map = {"π": "math.pi"}
        symbol = instance.text

        if symbol == ".":
            last_number = ""
            for element in reversed(self.formula):
                if element.isdigit() or element == ".":
                    last_number += element
                else:
                    break

            if "." in last_number:
                    return

        if self.formula[-1] == "π" and symbol not in "÷×-+":
            return

        if symbol == "π":
            if self.formula[-1] not in "÷×-+(√" and self.formula != "0":
                return
            if self.formula == "0":
                self.formula = ""
                self.eval_formula = ""
            self.formula += "π"
            self.eval_formula += num_eval_map["π"]
        else:
            if self.formula in ("0", "Ошибка") and symbol != ".":
                self.formula = ""
                self.eval_formula = ""
            self.formula += symbol
            self.eval_formula += symbol

        if self.just_opened_sqrt and symbol == "(":
            self.formula += symbol
            self.eval_formula += symbol
            self.auto_close_stack += 1

        self.update_label()

    def add_operation(self, instance):
        op_display = instance.text
        op_eval_map = {"÷": "/", "×": "*", "+": "+", "-": "-", "√": "math.sqrt(", "(": "(", ")": ")",
                       "log": "math.log10(", "ln": "math.log(", "¹/x": "**-1", "%": "/100", "xʸ": "**"}
        op_eval = op_eval_map.get(op_display)

        if op_display == "√":
            if self.formula in ("0", "", "Ошибка"):
                self.formula = "√"
                self.eval_formula = op_eval
            else:
                self.formula += "√"
                self.eval_formula += op_eval
            self.just_opened_sqrt = True
            self.auto_close_stack += 1
            self.update_label()
            return

        if op_display == "log":
            if self.formula in ("0", "", "Ошибка"):
                self.formula = "log("
                self.eval_formula = op_eval
            else:
                self.formula += "log("
                self.eval_formula += op_eval
            self.just_opened_log = True
            self.auto_close_stack += 1
            self.update_label()
            return

        if self.just_opened_sqrt and op_display in "÷×-+":
            self.eval_formula += ")"
            self.just_opened_sqrt = False
            self.auto_close_stack -= 1

        if op_display == "xʸ":
            self.formula += "^"
            self.eval_formula += op_eval
            self.update_label()
            return

        if op_display == "¹/x":
            self.formula += "^(-1)"
            self.eval_formula += op_eval
            self.update_label()
            return

        if op_display == "(":
            if self.formula in ("0", "", "Ошибка"):
                self.formula = "("
                self.eval_formula = "("
            else:
                self.formula += "("
                self.eval_formula += "("
            self.auto_close_stack += 1
            self.update_label()
            return

        if op_display == ")":
            if self.auto_close_stack > 0:
                self.auto_close_stack -= 1
            if self.formula in ("0", "", "Ошибка"):
                self.formula = ")"
                self.eval_formula = ")"
            else:
                self.formula += ")"
                self.eval_formula += ")"
            self.update_label()
            return

        if self.formula[-1] in ".0123456789π()%":
            self.formula += op_display
            self.eval_formula += op_eval
        elif self.formula[-1] in "÷×-+" and op_display in "÷×-+":
           self.formula = self.formula[:-1] + op_display
           self.eval_formula = self.eval_formula[:-1] + op_eval

        self.update_label()

    def calc_result(self, instance):
        try:
            while self.auto_close_stack > 0:
                self.eval_formula += ")"
                self.auto_close_stack -= 1
            self.just_opened_sqrt = False
            self.auto_close_stack = 0
            print(self.eval_formula)
            result = eval(self.eval_formula)
            if result % 1 == 0:
                self.formula = str(int(result))
                self.eval_formula = str(int(result))
            else:
                self.formula = str(round(result, 8))
                self.eval_formula = str(round(result, 8))
            self.update_label()
        except Exception as e:
            self.formula = "Ошибка"
            self.eval_formula = "0"
            self.update_label()

    def clear_all(self, instance):
        self.formula = "0"
        self.eval_formula = "0"
        self.auto_close_stack = 0
        self.just_opened_sqrt = False
        self.just_opened_log = False
        self.update_label()

    def clear_enrty(self, instance):
        self.formula = "0"
        self.eval_formula = "0"
        self.update_label()

    def backspace(self, instance):
        if self.formula in ("0", "Ошибка"):
            return

        self.formula = self.formula[:-1]
        self.eval_formula = self.eval_formula[-1]

        if not self.formula:
            self.formula = "0"
            self.eval_formula = "0"

        self.update_label()

    def build(self):
        self.formula = "0"
        self.eval_formula = "0"
        self.auto_close_stack = 0
        self.just_opened_sqrt = False
        self.just_opened_log = False
        boxlay = BoxLayout(orientation = "vertical", padding = 10)
        gridlay = GridLayout(cols = 4, spacing = 3, size_hint = (1, 0.6), )

        self.lebalboxlay = Label(text="0", font_size = 40, halign = "right", valign = "bottom",
                                size_hint = (1, 0.4), text_size = (400 - 20, 500 * 0.4 - 20))
        boxlay.add_widget(self.lebalboxlay)

        buttons = [ "%", "CE", "C", "⌫",
                    "log", "ln", "xʸ", "¹/x",
                    "√", "(", ")", "÷",
                    "7", "8", "9", "×",
                    "4", "5", "6", "-",
                    "1", "2", "3", "+",
                    "π", "0", ".", "="
                    ]
        for btn in buttons:
            if btn in ".0123456789π":
                gridlay.add_widget(Button(text=btn, on_press = self.add_number))
            elif btn in ("%", "√", "÷", "×", "-", "+", "(", ")", "log", "ln", "xʸ", "¹/x"):
                gridlay.add_widget(Button(text=btn, on_press = self.add_operation))
            elif btn == "CE":
                gridlay.add_widget(Button(text = btn, on_press = self.clear_all))
            elif btn == "C":
                gridlay.add_widget(Button(text = btn, on_press = self.clear_enrty))
            elif btn in "⌫":
                gridlay.add_widget(Button(text = btn, on_press = self.backspace))
            else:
                gridlay.add_widget(Button(text=btn, on_press = self.calc_result))
        boxlay.add_widget(gridlay)
        return boxlay

if __name__ == "__main__":
    CustomCalculatorApp().run()
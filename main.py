import math
import re

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
        self.lebalboxlay.text_size = (self.lebalboxlay.width - 10, self.lebalboxlay.height - 10)

        try:
            if self.formula[-1] in ("÷", "×", "-", "+"):
                preview = eval(self.eval_formula[:-1])
            else:
                preview = eval(self.eval_formula)

            if isinstance(preview, float) and preview % 1 == 0:
                preview = int(preview)
            elif isinstance(preview, float):
                preview = round(preview, 8)
            self.preview_label.text = f"= {preview}"
        except (ZeroDivisionError, ValueError, NameError, TypeError, OverflowError):
            self.preview_label.text = "Ошибка"
        except Exception:
            self.preview_label.text = ""

        self.preview_label.text_size = (self.preview_label.width - 10, self.preview_label.height - 10)

    def add_number(self, instance):
        num_eval_map = {"π": "math.pi"}
        symbol = instance.text
        match = re.search(r'(\d+\.?\d*|π)$', self.formula)
        if match:
            clean_number = match.group().replace('.', '').replace('π', '')
            if len(clean_number) >= 15:
                return

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

        if op_display == "ln":
            if self.formula in ("0", "", "Ошибка"):
                self.formula = "ln("
                self.eval_formula = op_eval
            else:
                self.formula += "ln("
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

            if self.formula[-1] in ("÷", "×", "-", "+"):
                result = eval(self.eval_formula[:-1])
            else:
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
            self.eval_formula = "Ошибка"
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
        if self.eval_formula[-12:-2] == "math.sqrt(":
            self.formula = self.formula[:-1]
            if self.auto_close_stack > 0:
                self.auto_close_stack -= 1
            self.just_opened_sqrt = True
            self.eval_formula = self.eval_formula[:-2]
        elif self.formula[-1] == "π":
            self.formula = self.formula[:-1]
            self.eval_formula = self.eval_formula[:-7]
        elif self.formula[-1] == "√":
            self.formula = self.formula[:-1]
            self.eval_formula = self.eval_formula[:-10]
            if self.auto_close_stack > 0:
                self.auto_close_stack -= 1
        elif self.eval_formula[-11:] == "math.log10(":
            self.formula = self.formula[:-4]
            self.eval_formula = self.eval_formula[:-11]
            if self.auto_close_stack > 0:
                self.auto_close_stack -= 1
        elif self.eval_formula[-9:] == "math.log(":
            self.formula = self.formula[:-3]
            self.eval_formula = self.eval_formula[:-9]
            if self.auto_close_stack > 0:
                self.auto_close_stack -= 1
        elif self.formula[-1] in ("^(-1)", "%"):
            self.formula = self.formula[:-1]
            self.eval_formula = self.eval_formula[:-4]
        elif self.formula[-1] == "^":
            self.formula = self.formula[:-1]
            self.eval_formula = self.eval_formula[:-2]
        else:
            self.formula = self.formula[:-1]
            self.eval_formula = self.eval_formula[:-1]


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

        self.lebalboxlay = Label(text="0", font_size=40, halign="right", valign="bottom", size_hint=(1, 0.4),
                                 text_size=(0, 0), shorten=True, max_lines=2)
        self.preview_label = Label( text="", font_size=20, halign="right", valign="top", color=(0.6, 0.6, 0.6, 1),
                                    size_hint=(1, 0.1), text_size=(0, 0))
        self.lebalboxlay.bind(size=lambda *args: self.update_label())
        self.preview_label.bind(size=lambda *args: self.update_label())
        boxlay.add_widget(self.lebalboxlay)
        boxlay.add_widget(self.preview_label)

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
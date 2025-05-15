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
            if self.formula[-1] not in "÷×-+" and self.formula != "0":
                return
            if self.formula == "0" or self.formula == "0.0":
                self.formula = ""
                self.eval_formula = ""
            self.formula += "π"
            self.eval_formula += num_eval_map["π"]
        else:
            if self.formula == "0" or self.formula == "0.0" and symbol != ".":
                self.formula = ""
                self.eval_formula = ""
            self.formula += symbol
            self.eval_formula += symbol

        self.update_label()

    def add_operation(self, instance):
        op_display = instance.text
        op_eval_map = {"÷": "/", "×": "*", "+": "+", "-": "-", "√": "math.sqrt("}
        op_eval = op_eval_map.get(op_display)

        if op_display == "√":
            self.auto_close_sqrt = True

        if op_display == "√":
            if self.formula == "0" or self.formula == "" or self.formula == "0.0":
                self.formula = "√"
                self.eval_formula = op_eval
            else:
                self.formula += "√"
                self.eval_formula += op_eval
            self.auto_close_sqrt = True
        elif self.formula[-1] in ".0123456789√π":
            self.formula += op_display
            self.eval_formula += op_eval
        elif self.formula[-1] in "÷×-+" and op_display in "÷×-+":
           self.formula = self.formula[:-1] + op_display
           self.eval_formula = self.eval_formula[:-1] + op_eval

        self.update_label()

    def calc_result(self, instance):
        try:
            if self.auto_close_sqrt:
                self.eval_formula += ")"
                self.auto_close_sqrt = False
            result = eval(self.eval_formula)
            self.formula = str(round(result, 8))
            self.eval_formula = str(round(result, 8))
            self.update_label()
        except Exception as e:
            self.formula = "Ошибка"
            self.eval_formula = "0"
            self.update_label()

    def build(self):
        self.formula = "0"
        self.eval_formula = "0"
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
            elif btn in "%√÷×-+()" or btn == "log" or btn == "ln":
                gridlay.add_widget(Button(text=btn, on_press = self.add_operation))
            else:
                gridlay.add_widget(Button(text=btn, on_press = self.calc_result))
        boxlay.add_widget(gridlay)
        return boxlay

if __name__ == "__main__":
    CustomCalculatorApp().run()
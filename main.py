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
    def build(self):
        boxlay = BoxLayout(orientation = "vertical", padding = 10)
        gridlay = GridLayout(cols = 4, spacing = 3, size_hint = (1, 0.6), )

        boxlay.add_widget(Label(text="0", font_size = 40, halign = "right", valign = "bottom",
                                size_hint = (1, 0.4), text_size = (400 - 20, 500 * 0.4 - 20)))

        buttons = [ "%", "√", "x²", "¹/x",
                    "CE", "C", "⌫", "÷",
                    "7", "8", "9", "×",
                    "4", "5", "6", "-",
                    "1", "2", "3", "+",
                    "±", "0", ".", "="
                    ]
        for btn in buttons:
            gridlay.add_widget(Button(text=btn))

        boxlay.add_widget(gridlay)
        return boxlay

if __name__ == "__main__":
    CustomCalculatorApp().run()
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

class CalculatorApp(App):
    def build(self):
        gridlay = GridLayout(cols = 6)

        gridlay.add_widget(Button(text="%"))
        gridlay.add_widget(Button(text="√"))
        gridlay.add_widget(Button(text="x²"))
        gridlay.add_widget(Button(text="¹/ₓ"))

        gridlay.add_widget(Button(text="CE"))
        gridlay.add_widget(Button(text="C"))
        gridlay.add_widget(Button(text="⌫"))
        gridlay.add_widget(Button(text="÷"))

        gridlay.add_widget(Button(text="7"))
        gridlay.add_widget(Button(text="8"))
        gridlay.add_widget(Button(text="9"))
        gridlay.add_widget(Button(text="×"))

        gridlay.add_widget(Button(text="4"))
        gridlay.add_widget(Button(text="5"))
        gridlay.add_widget(Button(text="6"))
        gridlay.add_widget(Button(text="-"))

        gridlay.add_widget(Button(text="1"))
        gridlay.add_widget(Button(text="2"))
        gridlay.add_widget(Button(text="3"))
        gridlay.add_widget(Button(text="+"))

        gridlay.add_widget(Button(text="±"))
        gridlay.add_widget(Button(text="0"))
        gridlay.add_widget(Button(text="."))
        gridlay.add_widget(Button(text="="))

        return gridlay

if __name__ == "_main__":
    CalculatorApp().run()
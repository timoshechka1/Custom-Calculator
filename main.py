from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

class CustomCalculatorApp(App):
    def build(self):
        boxlay = BoxLayout(orientation = "vertical")
        gridlay = GridLayout(cols = 4)

        boxlay.add_widget(Label(text="0"))

        gridlay.add_widget(Button(text="%"))
        gridlay.add_widget(Button(text="√"))
        gridlay.add_widget(Button(text="x²"))
        gridlay.add_widget(Button(text="¹/x"))

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

        boxlay.add_widget(gridlay)
        return boxlay

if __name__ == "__main__":
    CustomCalculatorApp().run()
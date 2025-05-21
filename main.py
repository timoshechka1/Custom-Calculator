from kivy.config import Config
from settings import THEMES

Config.set("graphics", "resizable", 1)
Config.set("graphics", "width", 400)
Config.set("graphics", "height", 500)
Config.set('graphics', 'borderless', 0)

import math
import re
import os
import json
from pathlib import Path

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import sp


SETTINGS_FILE = "calculator_settings.json"
HISTORY_FILE = "calculator_history.txt"

def load_settings():
    try:
        if Path(SETTINGS_FILE).exists():
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading settings: {e}")
    return {'theme': 'Theme 1'}


def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
    except Exception as e:
        print(f"Error saving settings: {e}")


class CustomCalculatorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        settings = load_settings()
        self.current_theme = settings.get('theme', 'Theme 1')
        theme = THEMES[self.current_theme]
        self.bg_color = theme['bg_color']
        self.text_color = theme['text_color']

    def update_label(self, *args):
        formatted_input = self.triad_separator(self.formula)
        self.lebalboxlay.text = formatted_input
        self.lebalboxlay.text_size = (self.lebalboxlay.width - 10, self.lebalboxlay.height - 10)
        self.scroll_to_bottom()
        self.lebalboxlay.text_size = (self.lebalboxlay.width - 10, None)
        self.lebalboxlay.texture_update()
        text_height = self.lebalboxlay.texture_size[1]
        min_height = sp(40)
        self.lebalboxlay.height = max(text_height, min_height)

        self.scroll_to_bottom()

        try:
            if self.formula[-1] in ("÷", "×", "-", "+"):
                preview = eval(self.eval_formula[:-1])
            else:
                preview = eval(self.eval_formula)

            if isinstance(preview, (int, float)):
                if preview.is_integer():
                    preview = int(preview)
                else:
                    preview = round(preview, 8)

                if abs(preview) >= 1000:
                    formatted_preview = "{:,}".format(preview).replace(",", " ")
                else:
                    formatted_preview = str(preview)
                self.preview_label.text = f"= {formatted_preview}"
            else:
                self.preview_label.text = f"= {preview}"
        except (ZeroDivisionError, ValueError, NameError, TypeError, OverflowError):
            self.preview_label.text = "Error"
        except Exception:
            self.preview_label.text = ""

        self.preview_label.text_size = (self.preview_label.width - 10, self.preview_label.height - 10)

    def update_label_height(self, instance, value):
        instance.height = value[1] + 10

    def load_history(self):
        self.history_box.clear_widgets()
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line:
                        lbl = Label(
                            text=line,
                            font_size=14,
                            size_hint_y=None,
                            height=20,
                            halign="right",
                            valign="middle"
                        )
                        lbl.text_size = (self.history_scroll.width - 20, None)
                        lbl.bind(size=lambda lbl, size: setattr(lbl, 'text_size', (size[0], None)))
                        self.history_box.add_widget(lbl)
                Clock.schedule_once(self.scroll_to_bottom)

    def save_to_history(self, expression, result):
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"{expression} = {result}\n")
        lbl = Label(
            text=f"{expression} = {result}",
            font_size=14,
            size_hint_y=None,
            height=20,
            halign="right",
            valign="middle",
            color = self.text_color
        )
        lbl.text_size = (self.history_scroll.width - 20, None)
        lbl.bind(size=lambda lbl, size: setattr(lbl, 'text_size', (size[0], None)))
        self.history_box.add_widget(lbl)

        Clock.schedule_once(self.scroll_to_bottom)

    def scroll_to_bottom(self, *args):
        self.history_scroll.scroll_y = 0
        self.formula_scroll.scroll_y = 0

    def on_start(self):
        self.update_widget_colors()

    def change_theme(self, spinner, text):
        if text in THEMES:
            self.current_theme = text
            self.bg_color = THEMES[text]['bg_color']
            self.text_color = THEMES[text]['text_color']
            self.update_widget_colors()
            save_settings({'theme': text})

    def update_spinner_dropdown(self, spinner):
        if hasattr(spinner, '_dropdown') and spinner._dropdown:
            dropdown = spinner._dropdown
            dropdown.background_color = self.bg_color
            if hasattr(dropdown, 'container'):
                for child in dropdown.container.children:
                    if isinstance(child, Button):
                        child.background_color = self.bg_color
                        child.color = self.text_color

    def update_widget_colors(self):
        theme = THEMES[self.current_theme]
        self.bg_color = theme['bg_color']
        self.text_color = theme['text_color']

        if self.current_theme in ("Theme 4", "Theme 7", "Theme 9"):
            Window.clearcolor = (0.95, 0.85, 0.7, 1)
        elif self.current_theme in ("Theme 3"):
            Window.clearcolor = (0.0, 0.0, 0.6667, 1)
        else:
            Window.clearcolor = (0.05, 0.05, 0.05, 1)

        if not hasattr(self, 'root'):
            return

        for widget in self.root.walk():
            if isinstance(widget, (Button, Label, Spinner)):
                widget.background_color = self.bg_color
                widget.color = self.text_color

        self.update_spinner_dropdown(self.font_spinner)
        self.update_spinner_dropdown(self.theme_spinner)

    def change_font(self, spinner, text):
        filename = None
        for short_name, full_name in self.font_items:
            if short_name == text:
                filename = full_name
                break

        if filename is None:
            return

        font_path = f"fonts/{filename}"

        if not os.path.exists(font_path):
            print(f"Font file not found: {font_path}")
            return

        kv_path = "customcalculator.kv"
        with open(kv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if "font_name:" in line:
                indent = line[:line.find("font_name:")]
                new_line = f'{indent}font_name: "{font_path}"\n'
                new_lines.append(new_line)
            else:
                new_lines.append(line)

        with open(kv_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        self.update_fonts(font_path)
        self.update_label()

    def update_fonts(self, font_path):
        self.lebalboxlay.font_name = font_path
        self.preview_label.font_name = font_path
        self.font_spinner.font_name = font_path
        self.theme_spinner.font_name = font_path

        for spinner in [self.font_spinner, self.theme_spinner]:
            if hasattr(spinner, '_dropdown') and spinner._dropdown:
                dropdown = spinner._dropdown
                if hasattr(dropdown, 'container'):
                    for item in dropdown.container.children:
                        if isinstance(item, Button):
                            item.font_name = font_path
                            item.font_size = spinner.font_size

        if hasattr(self, 'root') and self.root:
            for child in self.root.children:
                if isinstance(child, GridLayout):
                    for widget in child.children:
                        if isinstance(widget, Button):
                            widget.font_name = font_path

    def triad_separator(self, entered_number):
        operators = ["÷", "×", "+", "-", "(", ")", "π", "√", "log", "ln"]
        escaped_operators = [re.escape(op) for op in operators]
        operators_patterns = "(" + "|".join(escaped_operators) + ")"

        parts = re.split(operators_patterns, entered_number)
        formatted_parts = []

        for part in parts:
            if not part:
                continue

            if part.replace(".", "", 1).isdigit():
                if "." in part:
                    integer_part, fractional_part = part.split(".", 1)
                else:
                    integer_part, fractional_part = part, ""

                formatted_integer = integer_part
                if len(integer_part) > 3:
                    try:
                        formatted_integer = "{:,}".format(int(integer_part)).replace(",", " ")
                    except ValueError:
                        pass

                formatted_number = formatted_integer
                if fractional_part:
                    formatted_number += f".{fractional_part}"

                formatted_parts.append(formatted_number)
            else:
                formatted_parts.append(part)

        return ''.join(formatted_parts)

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
            if self.formula in ("0", "Error") and symbol != ".":
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
            if self.formula in ("0", "", "Error"):
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
            if self.formula in ("0", "", "Error"):
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
            if self.formula in ("0", "", "Error"):
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
            if self.formula in ("0", "", "Error"):
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
            if self.formula in ("0", "", "Error"):
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

            if self.formula[-1] in ("÷", "×", "-", "+"):
                result = eval(self.eval_formula[:-1])
            else:
                result = eval(self.eval_formula)

            if result % 1 == 0:
                result_to_display = str(int(result))
            else:
                result_to_display = str(round(result, 8))

            self.save_to_history(self.formula, result_to_display)
            self.formula = result_to_display
            self.eval_formula = result_to_display
            self.update_label()
        except Exception as e:
            self.formula = "Error"
            self.eval_formula = "Error"
            self.update_label()

    def clear_all(self, instance):
        self.formula = "0"
        self.eval_formula = "0"
        self.auto_close_stack = 0
        self.just_opened_sqrt = False
        self.just_opened_log = False
        self.update_label()
        open(HISTORY_FILE, "w", encoding="utf-8").close()
        self.history_box.clear_widgets()

    def clear_enrty(self, instance):
        self.formula = "0"
        self.eval_formula = "0"
        self.update_label()

    def backspace(self, instance):
        if self.formula in ("0", "Error"):
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
            if self.auto_close_stack > 0:
                self.auto_close_stack -= 1

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
        boxlay = BoxLayout(orientation="vertical", padding=10)
        spinner_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=5)

        kv_path = "customcalculator.kv"
        current_font_path = None
        if os.path.exists(kv_path):
            with open(kv_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("font_name:"):
                        parts = line.strip().split(":")
                        if len(parts) > 1:
                            current_font_path = parts[1].strip().strip('"').strip("'")
                        break

        font_folder = "fonts"
        if not os.path.exists(font_folder):
            os.makedirs(font_folder)

        font_files = [f for f in os.listdir(font_folder) if f.endswith(('.ttf', '.otf', '.ttc'))]
        self.font_items = [(os.path.splitext(f)[0], f) for f in font_files]

        initial_font = None
        initial_font_path = None

        if current_font_path and os.path.exists(current_font_path):
            font_filename = os.path.basename(current_font_path)
            font_name = os.path.splitext(font_filename)[0]
            if font_name in [item[0] for item in self.font_items]:
                initial_font = font_name
                initial_font_path = current_font_path

        if not initial_font and self.font_items:
            initial_font = self.font_items[0][0]
            initial_font_path = f"fonts/{self.font_items[0][1]}"

        self.font_spinner = Spinner(
            text=initial_font if initial_font else "No fonts found",
            values=[item[0] for item in self.font_items] if self.font_items else ["No fonts available"],
            size_hint=(0.7, 1),
            option_cls='SpinnerOption'
        )
        self.font_spinner.bind(text=self.change_font)

        self.theme_spinner = Spinner(
            text=self.current_theme,
            values=list(THEMES.keys()),
            size_hint=(0.3, 1),
            option_cls='SpinnerOption'
        )
        self.theme_spinner.font_name = initial_font_path if initial_font_path else None
        self.theme_spinner.bind(text=self.change_theme)

        self.theme_spinner.bind(text=self.change_theme)
        spinner_box.add_widget(self.font_spinner)
        spinner_box.add_widget(self.theme_spinner)
        boxlay.add_widget(spinner_box)


        self.history_box = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=2)
        self.history_box.bind(minimum_height=self.history_box.setter('height'))
        self.history_scroll = ScrollView(size_hint=(1, 0.3) )
        self.history_scroll.add_widget(self.history_box)
        boxlay.add_widget(self.history_scroll)

        gridlay = GridLayout(cols=4, spacing=3, size_hint=(1, 0.8))

        self.lebalboxlay = Label(
            text="0",
            font_size=40,
            halign="right",
            valign="bottom",
            size_hint=(1, None),
        )
        self.lebalboxlay.bind(texture_size=self.update_label_height)
        self.lebalboxlay.bind(
            width=lambda instance, width: setattr(instance, 'text_size', (width, None))
        )

        self.formula_scroll = ScrollView(
            size_hint=(1, 0.4),
            do_scroll_x=False,
            do_scroll_y=True,
        )

        self.formula_scroll.add_widget(self.lebalboxlay)

        boxlay.add_widget(self.formula_scroll)

        self.preview_label = Label(text="", font_size=20, halign="right", valign="top",
                                   color=self.text_color, size_hint=(1, 0.1), text_size=(0, 0),)

        if initial_font_path:
            self.update_fonts(initial_font_path)

        self.lebalboxlay.bind(size=lambda *args: self.update_label())
        self.preview_label.bind(size=lambda *args: self.update_label())
        boxlay.add_widget(self.preview_label)

        buttons = [
            "%", "CE", "C", "⌫",
            "log", "ln", "xʸ", "¹/x",
            "√", "(", ")", "÷",
            "7", "8", "9", "×",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "π", "0", ".", "="
        ]

        for btn in buttons:
            button = Button(text=btn, background_color=self.bg_color, color=self.text_color)
            if initial_font_path:
                button.font_name = initial_font_path

            if btn in ".0123456789π":
                button.bind(on_press=self.add_number)
            elif btn in ("%", "√", "÷", "×", "-", "+", "(", ")", "log", "ln", "xʸ", "¹/x"):
                button.bind(on_press=self.add_operation)
            elif btn == "CE":
                button.bind(on_press=self.clear_all)
            elif btn == "C":
                button.bind(on_press=self.clear_enrty)
            elif btn in "⌫":
                button.bind(on_press=self.backspace)
            else:
                button.bind(on_press=self.calc_result)

            gridlay.add_widget(button)

        self.load_history()
        boxlay.add_widget(gridlay)
        return boxlay


if __name__ == "__main__":
    CustomCalculatorApp().run()
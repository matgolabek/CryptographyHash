from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabs
from kivymd.uix.scrollview import MDScrollView
from kivy.clock import Clock
from kivy.core.window import Window

import md4
import md5
import numpy as np

class TabMD4(MDStackLayout, MDTabsBase):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.title="MD4"

        scroll = MDScrollView(do_scroll_x=True, do_scroll_y=True)
        content = ContentMD4(orientation=orientation)

        scroll.add_widget(content)
        self.add_widget(scroll)


class ContentMD4(MDStackLayout):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'lr-tb'
        self.adaptive_height = True
        self.padding = 20
        # self.adaptive_width = True # RAM eater

        self.widget_height = 0.03
        self.md = md4.MD4()
        self.disable_calc = False

        hello_label = MDLabel(text=f"MD4 algorithm", font_style="H4", size_hint=(0.55, self.widget_height * 4), halign="right", valign="middle")
        hello_label.bind(size=hello_label.setter("text_size"))
        self.add_widget(hello_label)

        hello_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="aaabbcc",
            size_hint=(None, self.widget_height * 4),
            halign='left'
        )
        self.add_widget(hello_info)

        self.add_widget(MDIconButton(
            icon="blank",
            icon_color=(1, 1, 1, 0),
            size_hint=(0.35, self.widget_height * 4),
        ))

        self.add_widget(MDIconButton(icon="theme-light-dark", size_hint=(None, self.widget_height * 4), on_release=self.toggle_theme, halign='right'))
        self.add_widget(MDIconButton(icon="restore", size_hint=(None, self.widget_height * 4), on_release=self.reset_variables))
        
        # Chain constraints
        chain_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        chain_row.add_widget(MDLabel(text="Enter chain constants:", size_hint=(0.09, self.widget_height)))
        chain_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="lalalala",
            size_hint=(None, self.widget_height * 4)
        )
        chain_row.add_widget(chain_info)
        self.add_widget(chain_row)
        self.add_widget(MDLabel(text="h1:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="h2:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="h3:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="h4:", halign='left', size_hint=(0.25, self.widget_height)))

        h1_def = '67452301'
        self.h1_ti = MDTextField(text=h1_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h1_ti)

        h2_def = 'efcdab89'
        self.h2_ti = MDTextField(text=h2_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h2_ti)

        h3_def, h4_def = md4.chain_constraints(h1_def, h2_def)
        self.h3_ti = MDTextField(text=h3_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_chain_const, readonly=True)
        self.add_widget(self.h3_ti)

        self.h4_ti = MDTextField(text=h4_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_chain_const, readonly=True)
        self.add_widget(self.h4_ti)

        # Additivie constaints
        add_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        add_row.add_widget(MDLabel(text="Enter additive constants:", halign='left', size_hint=(0.11, self.widget_height)))
        add_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="bebebbe",
            size_hint=(None, self.widget_height * 4)
        )
        add_row.add_widget(add_info)
        self.add_widget(add_row)
        self.add_widget(MDLabel(text="y1:", halign='left', size_hint=(0.33, self.widget_height)))
        self.add_widget(MDLabel(text="y2:", halign='left', size_hint=(0.33, self.widget_height)))
        self.add_widget(MDLabel(text="y3:", halign='left', size_hint=(0.33, self.widget_height)))

        y1_def = '00000000'
        self.y1_ti = MDTextField(text=y1_def, multiline=False, size_hint=(0.33, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y1_ti)

        y2_def = '5a827999'
        self.y2_ti = MDTextField(text=y2_def, multiline=False, size_hint=(0.33, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y2_ti)

        y3_def = '6ed9eba1'
        self.y3_ti = MDTextField(text=y3_def, multiline=False, size_hint=(0.34, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y3_ti)

        # Order lists
        order_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        order_row.add_widget(MDLabel(text="Enter order lists:", halign='left', size_hint=(0.08, self.widget_height)))
        order_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="cycycyccycy",
            size_hint=(None, self.widget_height * 4)
        )
        order_row.add_widget(order_info)
        self.add_widget(order_row)
        self.add_widget(MDLabel(text="z1:", halign='left', size_hint=(0.8 * 0.33, self.widget_height)))
        self.add_widget(MDLabel(text="z2:", halign='left', size_hint=(0.8 * 0.33, self.widget_height)))
        self.add_widget(MDLabel(text="z3:", halign='left', size_hint=(0.8 * 0.34, self.widget_height)))

        self.z1_def = str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        self.z1_ti = MDTextField(text=self.z1_def, multiline=False, size_hint=(0.8 * 0.33, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z1_ti)

        self.z2_def = str([0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15])
        self.z2_ti = MDTextField(text=self.z2_def, multiline=False, size_hint=(0.8 * 0.33, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z2_ti)

        self.z3_def = str([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15])
        self.z3_ti = MDTextField(text=self.z3_def, multiline=False, size_hint=(0.8 * 0.34, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z3_ti)

        self.add_widget(MDRaisedButton(text="Shuffle", on_press=self.shuffle_z, size_hint=(0.2, self.widget_height)))

        # Shuffle lists
        shuffle_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        shuffle_row.add_widget(MDLabel(text="Enter shuffle lists:", halign='left', size_hint=(0.08, self.widget_height)))
        shuffle_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="dididididi",
            size_hint=(None, self.widget_height * 4)
        )
        shuffle_row.add_widget(shuffle_info)
        self.add_widget(shuffle_row)
        self.add_widget(MDLabel(text="s1:", halign='left', size_hint=(0.8*0.33, self.widget_height)))
        self.add_widget(MDLabel(text="s2:", halign='left', size_hint=(0.8*0.33, self.widget_height)))
        self.add_widget(MDLabel(text="s3:", halign='left', size_hint=(0.8*0.33, self.widget_height)))

        self.s1_def = str([3, 7, 11, 19])
        self.s1_ti = MDTextField(text=self.s1_def, multiline=False, size_hint=(0.8*0.33, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s1_ti)

        self.s2_def = str([3, 5, 9, 13])
        self.s2_ti = MDTextField(text=self.s2_def, multiline=False, size_hint=(0.8*0.33, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s2_ti)

        self.s3_def = str([3, 9, 11, 15])
        self.s3_ti = MDTextField(text=self.s3_def, multiline=False, size_hint=(0.8*0.34, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s3_ti)

        self.add_widget(MDRaisedButton(text="Shuffle", on_press=self.shuffle_s, size_hint=(0.2, self.widget_height)))

        mess_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        mess_row.add_widget(MDLabel(text="Enter message to encrypt:", halign='left', size_hint=(0.1, self.widget_height)))
        mess_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="eeeeeeeeee",
            size_hint=(None, self.widget_height * 4)
        )
        mess_row.add_widget(mess_info)
        self.add_widget(mess_row)
        self.message = MDTextField(text="Password to hash", size_hint=(0.8, self.widget_height))
        self.add_widget(self.message)
        
        self.add_widget(MDRaisedButton(text="Enter", on_press=self.initialize, size_hint=(0.2, self.widget_height)))

        self.add_widget(MDRaisedButton(text="Run one iteration",
                               on_press=self.run_iter,
                               size_hint=(0.5, self.widget_height)))
        self.add_widget(MDRaisedButton(text="Run all",
                               on_press=self.run_all,
                               size_hint=(0.5, self.widget_height)))
        
        # Display results
        reg_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        reg_row.add_widget(MDLabel(text="\nRegisters:", halign='left', size_hint=(0.05, self.widget_height)))
        reg_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="ffffffff",
            size_hint=(None, self.widget_height * 24)
        )
        reg_row.add_widget(reg_info)
        self.add_widget(reg_row)

        self.add_widget(MDLabel(text="a:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="b:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="c:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="d:", halign='left', size_hint=(0.25, self.widget_height)))

        self.a_ti = MDTextField(text=str(self.md.a),
                               multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.a_ti)

        self.b_ti = MDTextField(text=str(self.md.b),
                               multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.b_ti)

        self.c_ti = MDTextField(text=str(self.md.c),
                               multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.c_ti)

        self.d_ti = MDTextField(text=str(self.md.d),
                               multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.d_ti)

        final_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        final_row.add_widget(MDLabel(text="Final output:", halign='left', size_hint=(0.06, self.widget_height)))
        final_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="ggggggggggggggg",
            size_hint=(None, self.widget_height * 4)
        )
        final_row.add_widget(final_info)
        self.add_widget(final_row)
        
        r = self.md.get_registers()
        self.r_l = [None for _ in range(32)]
        for i in range(32):
            self.r_l[i] = MDTextField(text=r[i], size_hint=(1/32, self.widget_height), multiline=False,  on_text_validate=self.update_out, readonly=True)
            self.add_widget(self.r_l[i])

    def update_chain_const(self, instance):
        try:
            if len(instance.text) > 8:
                raise ValueError
            int(instance.text, 16)
        except ValueError:
            self.show_popup("Not a valid 8-bit hexadecimal constant.")
            instance.text = '00000000'
            return
        self.h3_ti.text, self.h4_ti.text = md4.chain_constraints(self.h1_ti.text, self.h2_ti.text)

    def shuffle_z(self, instance):
        self.z1_ti.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z2_ti.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z3_ti.text = str(np.random.permutation(np.arange(16)).tolist())

    def shuffle_s(self, instance):
        self.s1_ti.text = str(np.sort(np.random.choice([3, 5, 7, 9, 11, 13, 15, 17, 19], size=4, replace=False)).tolist())
        self.s2_ti.text = str(np.sort(np.random.choice([3, 5, 7, 9, 11, 13, 15, 17, 19], size=4, replace=False)).tolist())
        self.s3_ti.text = str(np.sort(np.random.choice([3, 5, 7, 9, 11, 13, 15, 17, 19], size=4, replace=False)).tolist())

    def initialize(self, instance):
        def parse_str_to_int(s):
            return [int(x.strip()) for x in s.strip('[]').split(',') if x.strip()]
        try:
            self.md = md4.MD4(self.message.text, self.h1_ti.text, self.h2_ti.text, self.y1_ti.text, self.y2_ti.text, self.y3_ti.text,
                        parse_str_to_int(self.z1_ti.text),
                        parse_str_to_int(self.z2_ti.text),
                        parse_str_to_int(self.z3_ti.text),
                        parse_str_to_int(self.s1_ti.text),
                        parse_str_to_int(self.s2_ti.text),
                        parse_str_to_int(self.s3_ti.text))
        except ValueError:
            self.show_popup("The message can't be empty.")
            return
        self.disable_calc = False

    def update_reg(self, instance):
        self.a_ti.text = self.md.a
        self.b_ti.text = self.md.b
        self.c_ti.text = self.md.c
        self.d_ti.text = self.md.d

    def update_out(self, instance):
        r = self.md.get_registers()
        for i in range(32):
            self.r_l[i].text = r[i]

    def run_iter(self, instance):
        if self.disable_calc:
            self.show_popup("Calculations have been completed. Type a new password to hash and press enter to run again.")
            return
        try:
            finished = self.md.run_iter()
        except TypeError:
            self.show_popup("The message hasn't been acknowledged. Type a new password to hash and press enter to start.")
            return
        self.a_ti.text = str(self.md.a)
        self.b_ti.text = str(self.md.b)
        self.c_ti.text = str(self.md.c)
        self.d_ti.text = str(self.md.d)
        if finished:
            self.disable_calc = True
            r = self.md.get_registers()
            for i in range(32):
                self.r_l[i].text = r[i]

    def run_all(self, instance):
        if self.disable_calc:
            self.show_popup("Calculations have been completed. Type a new password to hash and press enter to run again.")
            return
        try:
            self.md.run_iter()
        except TypeError:
            self.show_popup("The message hasn't been acknowledged. Type a new password to hash and press enter to start.")
            return
        Clock.schedule_interval(self.run_all_async, 0.05)

    def run_all_async(self, dt):
        finished = self.md.run_iter()
        self.a_ti.text = str(self.md.a)    
        self.b_ti.text = str(self.md.b)
        self.c_ti.text = str(self.md.c)
        self.d_ti.text = str(self.md.d)
        if finished:
            self.disable_calc = True
            r = self.md.get_registers()
            for i in range(32):
                self.r_l[i].text = r[i]
        return not finished
    
    def show_popup(self, label_text=str):
        self.dialog = MDDialog(
            title='Warning',
            text=label_text,
            buttons=[
                MDFlatButton(text="OK", on_release=self.close_popup)
            ],
        )
        self.dialog.open()

    def close_popup(self, *args):
        self.dialog.dismiss()

    def toggle_theme(self, *args):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"

    def reset_variables(self, *args):
        self.h1_ti.text = '67452301'
        self.h2_ti.text = 'efcdab89'
        self.y1_ti.text = '00000000'
        self.y2_ti.text = '5a827999'
        self.y3_ti.text = '6ed9eba1'
        self.z1_ti.text = str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        self.z2_ti.text = str([0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15])
        self.z3_ti.text = str([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15])
        self.s1_ti.text = str([3, 7, 11, 19])
        self.s2_ti.text = str([3, 5, 9, 13])
        self.s3_ti.text = str([3, 9, 11, 15])
        self.message.text = "Password to hash"

    def check_if_number(self, instance):
        try:
            if len(instance.text) > 8:
                raise ValueError
            int(instance.text, 16)
        except ValueError:
            self.show_popup("Not a valid 8-bit hexadecimal constant.")
            instance.text = '00000000'

    def check_if_correct_z(self, instance):
        def parse_str_to_int(s):
            return [int(x.strip()) for x in s.strip('[]').split(',') if x.strip()]
        try:
            arr = parse_str_to_int(instance.text)
            if len(arr) < 16:
                self.show_popup("Not a valid 16 number array. Too short.")
                instance.text = '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'
                return
            elif len(arr) > 16:
                self.show_popup("Not a valid 16 number array. Too long.")
                instance.text = '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'
                return
            for i in arr:
                if i < 0 or i > 15:
                    self.show_popup("Not a valid 16 number array. Numbers must be in range from 0 to 15.")
                    instance.text = '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'
                    return
        except ValueError:
            self.show_popup("Not a valid 16 number array.")
            instance.text = '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'

    def check_if_correct_s(self, instance):
        def parse_str_to_int(s):
            return [int(x.strip()) for x in s.strip('[]').split(',') if x.strip()]
        try:
            arr = parse_str_to_int(instance.text)
            if len(arr) < 4:
                self.show_popup("Not a valid 4 number array. Too short.")
                instance.text = '[3, 7, 11, 19]'
                return
            elif len(arr) > 4:
                self.show_popup("Not a valid 4 number array. Too long.")
                instance.text = '[3, 7, 11, 19]'
                return
            for i in arr:
                if i < 0:
                    self.show_popup("Not a valid 16 number array. Numbers must be greater than 0 and should be less than 19.")
                    instance.text = '[3, 7, 11, 19]'
                    return
        except ValueError:
            self.show_popup("Not a valid 4 number array.")
            instance.text = '[3, 7, 11, 19]'


class TabMD5(MDStackLayout, MDTabsBase):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.title="MD5"

        scroll = MDScrollView(do_scroll_x=True, do_scroll_y=True)
        content = ContentMD5(orientation=orientation)

        scroll.add_widget(content)
        self.add_widget(scroll)


class ContentMD5(MDStackLayout):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'lr-tb'
        self.adaptive_height = True
        self.padding = 20
        # self.adaptive_width = True # RAM eater

        self.widget_height = 0.03
        self.md = md5.MD5()
        self.disable_calc = False

        hello_label = MDLabel(text=f"MD5 algorithm", font_style="H4", size_hint=(0.55, self.widget_height * 4), halign="right", valign="middle")
        hello_label.bind(size=hello_label.setter("text_size"))
        self.add_widget(hello_label)

        hello_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="aaabbcc",
            size_hint=(None, self.widget_height * 4),
            halign='left'
        )
        self.add_widget(hello_info)

        self.add_widget(MDIconButton(
            icon="blank",
            icon_color=(1, 1, 1, 0),
            size_hint=(0.35, self.widget_height * 4),
        ))
        
        self.add_widget(MDIconButton(icon="theme-light-dark", size_hint=(None, self.widget_height * 4), on_release=self.toggle_theme, halign='right'))
        self.add_widget(MDIconButton(icon="restore", size_hint=(None, self.widget_height * 4), on_release=self.reset_variables))
        
        # Chain constraints
        chain_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        chain_row.add_widget(MDLabel(text="Enter chain constants:", size_hint=(0.09, self.widget_height)))
        chain_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="lalalala",
            size_hint=(None, self.widget_height * 4)
        )
        chain_row.add_widget(chain_info)
        self.add_widget(chain_row)
        self.add_widget(MDLabel(text="h1:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="h2:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="h3:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="h4:", halign='left', size_hint=(0.25, self.widget_height)))

        h1_def = '67452301'
        self.h1_ti = MDTextField(text=h1_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h1_ti)

        h2_def = 'efcdab89'
        self.h2_ti = MDTextField(text=h2_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h2_ti)

        h3_def, h4_def = md4.chain_constraints(h1_def, h2_def)
        self.h3_ti = MDTextField(text=h3_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_chain_const, readonly=True)
        self.add_widget(self.h3_ti)

        self.h4_ti = MDTextField(text=h4_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_chain_const, readonly=True)
        self.add_widget(self.h4_ti)

        # Additivie constaints
        add_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        add_row.add_widget(MDLabel(text="Select additive constant type:", halign='left', size_hint=(0.11, self.widget_height)))
        add_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="bebebbe",
            size_hint=(None, self.widget_height * 4)
        )
        add_row.add_widget(add_info)
        self.add_widget(add_row)


        self.add_const = 'sin'

        self.checkbox = MDCheckbox(group="additive", size_hint=(0.33 * 0.3, self.widget_height * 2))
        self.checkbox.active = True
        self.checkbox.label_text = 'sin'
        self.checkbox.bind(active=self.on_checkbox_active)

        label = MDLabel(
            text="sin",
            halign='left',
            valign = 'top',
            size_hint=(0.33 * 0.7, self.widget_height * 2)
        )

        self.add_widget(self.checkbox)
        self.add_widget(label)

        checkbox = MDCheckbox(group="additive", size_hint=(0.33 * 0.3, self.widget_height * 2))
        checkbox.label_text = 'cos'
        checkbox.bind(active=self.on_checkbox_active)

        label = MDLabel(
            text="cos",
            halign='left',
            valign = 'top',
            size_hint=(0.33 * 0.7, self.widget_height * 2)
        )

        self.add_widget(checkbox)
        self.add_widget(label)

        checkbox = MDCheckbox(group="additive", size_hint=(0.33 * 0.3, self.widget_height * 2))
        checkbox.label_text = 'tan'
        checkbox.bind(active=self.on_checkbox_active)

        label = MDLabel(
            text="tan",
            halign='left',
            valign = 'top',
            size_hint=(0.33 * 0.7, self.widget_height * 2)
        )

        self.add_widget(checkbox)
        self.add_widget(label)

        # Order lists
        order_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        order_row.add_widget(MDLabel(text="Enter order lists:", halign='left', size_hint=(0.08, self.widget_height)))
        order_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="cycycyccycy",
            size_hint=(None, self.widget_height * 4)
        )
        order_row.add_widget(order_info)
        self.add_widget(order_row)
        self.add_widget(MDLabel(text="z1:", halign='left', size_hint=(0.8 * 0.25, self.widget_height)))
        self.add_widget(MDLabel(text="z2:", halign='left', size_hint=(0.8 * 0.25, self.widget_height)))
        self.add_widget(MDLabel(text="z3:", halign='left', size_hint=(0.8 * 0.25, self.widget_height)))
        self.add_widget(MDLabel(text="z4:", halign='left', size_hint=(0.25, self.widget_height)))

        self.z1_def = str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        self.z1_ti = MDTextField(text=self.z1_def, multiline=False, size_hint=(0.8 * 0.25, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z1_ti)

        self.z2_def = str([1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12])
        self.z2_ti = MDTextField(text=self.z2_def, multiline=False, size_hint=(0.8 * 0.25, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z2_ti)

        self.z3_def = str([5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2])
        self.z3_ti = MDTextField(text=self.z3_def, multiline=False, size_hint=(0.8 * 0.25, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z3_ti)

        self.z4_def = str([0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9])
        self.z4_ti = MDTextField(text=self.z4_def, multiline=False, size_hint=(0.8 * 0.25, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z4_ti)

        self.add_widget(MDRaisedButton(text="Shuffle", on_press=self.shuffle_z, size_hint=(0.2, self.widget_height)))

        # Shuffle lists
        shuffle_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        shuffle_row.add_widget(MDLabel(text="Enter shuffle lists:", halign='left', size_hint=(0.08, self.widget_height)))
        shuffle_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="dididididi",
            size_hint=(None, self.widget_height * 4)
        )
        shuffle_row.add_widget(shuffle_info)
        self.add_widget(shuffle_row)
        self.add_widget(MDLabel(text="s1:", halign='left', size_hint=(0.8 * 0.25, self.widget_height)))
        self.add_widget(MDLabel(text="s2:", halign='left', size_hint=(0.8 * 0.25, self.widget_height)))
        self.add_widget(MDLabel(text="s3:", halign='left', size_hint=(0.8 * 0.25, self.widget_height)))
        self.add_widget(MDLabel(text="s4:", halign='left', size_hint=(0.25, self.widget_height)))

        self.s1_def = str([7, 12, 17, 22])
        self.s1_ti = MDTextField(text=self.s1_def, multiline=False, size_hint=(0.8*0.25, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s1_ti)

        self.s2_def = str([5, 9, 14, 20])
        self.s2_ti = MDTextField(text=self.s2_def, multiline=False, size_hint=(0.8*0.25, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s2_ti)

        self.s3_def = str([4, 11, 16, 23])
        self.s3_ti = MDTextField(text=self.s3_def, multiline=False, size_hint=(0.8*0.25, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s3_ti)

        self.s4_def = str([6, 10, 15, 21])
        self.s4_ti = MDTextField(text=self.s4_def, multiline=False, size_hint=(0.8*0.25, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s4_ti)

        self.add_widget(MDRaisedButton(text="Shuffle", on_press=self.shuffle_s, size_hint=(0.2, self.widget_height)))

        mess_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        mess_row.add_widget(MDLabel(text="Enter message to encrypt:", halign='left', size_hint=(0.1, self.widget_height)))
        mess_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="eeeeeeeeee",
            size_hint=(None, self.widget_height * 4)
        )
        mess_row.add_widget(mess_info)
        self.add_widget(mess_row)
        self.message = MDTextField(text="Password to hash", size_hint=(0.8, self.widget_height))
        self.add_widget(self.message)
        
        self.add_widget(MDRaisedButton(text="Enter", on_press=self.initialize, size_hint=(0.2, self.widget_height)))

        self.add_widget(MDRaisedButton(text="Run one iteration",
                               on_press=self.run_iter,
                               size_hint=(0.5, self.widget_height)))
        self.add_widget(MDRaisedButton(text="Run all",
                               on_press=self.run_all,
                               size_hint=(0.5, self.widget_height)))
        
        # Display results
        reg_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        reg_row.add_widget(MDLabel(text="\nRegisters:", halign='left', size_hint=(0.05, self.widget_height)))
        reg_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="ffffffff",
            size_hint=(None, self.widget_height * 24)
        )
        reg_row.add_widget(reg_info)
        self.add_widget(reg_row)

        self.add_widget(MDLabel(text="a:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="b:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="c:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="d:", halign='left', size_hint=(0.25, self.widget_height)))

        self.a_ti = MDTextField(text=str(self.md.a),
                               multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.a_ti)

        self.b_ti = MDTextField(text=str(self.md.b),
                               multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.b_ti)

        self.c_ti = MDTextField(text=str(self.md.c),
                               multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.c_ti)

        self.d_ti = MDTextField(text=str(self.md.d),
                               multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.d_ti)

        final_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        final_row.add_widget(MDLabel(text="Final output:", halign='left', size_hint=(0.06, self.widget_height)))
        final_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="ggggggggggggggg",
            size_hint=(None, self.widget_height * 4)
        )
        final_row.add_widget(final_info)
        self.add_widget(final_row)
        
        r = self.md.get_registers()
        self.r_l = [None for _ in range(32)]
        for i in range(32):
            self.r_l[i] = MDTextField(text=r[i], size_hint=(1/32, self.widget_height), multiline=False,  on_text_validate=self.update_out, readonly=True)
            self.add_widget(self.r_l[i])

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.add_const = checkbox.label_text  # MDLabel is the second widget in layout

    def update_chain_const(self, instance):
        try:
            if len(instance.text) > 8:
                raise ValueError
            int(instance.text, 16)
        except ValueError:
            self.show_popup("Not a valid 8-bit hexadecimal constant.")
            instance.text = '00000000'
            return
        self.h3_ti.text, self.h4_ti.text = md4.chain_constraints(self.h1_ti.text, self.h2_ti.text)

    def shuffle_z(self, instance):
        self.z1_ti.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z2_ti.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z3_ti.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z4_ti.text = str(np.random.permutation(np.arange(16)).tolist())

    def shuffle_s(self, instance):
        self.s1_ti.text = str(np.sort(np.random.choice([4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 20, 21, 22, 23], size=4, replace=False)).tolist())
        self.s2_ti.text = str(np.sort(np.random.choice([4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 20, 21, 22, 23], size=4, replace=False)).tolist())
        self.s3_ti.text = str(np.sort(np.random.choice([4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 20, 21, 22, 23], size=4, replace=False)).tolist())
        self.s4_ti.text = str(np.sort(np.random.choice([4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 20, 21, 22, 23], size=4, replace=False)).tolist())

    def initialize(self, instance):
        def parse_str_to_int(s):
            return [int(x.strip()) for x in s.strip('[]').split(',') if x.strip()]
        try:
            self.md = md5.MD5(self.message.text, self.h1_ti.text, self.h2_ti.text, self.add_const,
                        parse_str_to_int(self.z1_ti.text),
                        parse_str_to_int(self.z2_ti.text),
                        parse_str_to_int(self.z3_ti.text),
                        parse_str_to_int(self.z4_ti.text),
                        parse_str_to_int(self.s1_ti.text),
                        parse_str_to_int(self.s2_ti.text),
                        parse_str_to_int(self.s3_ti.text),
                        parse_str_to_int(self.s4_ti.text))
        except ValueError:
            self.show_popup("The message can't be empty.")
            return
        self.disable_calc = False

    def update_reg(self, instance):
        self.a_ti.text = self.md.a
        self.b_ti.text = self.md.b
        self.c_ti.text = self.md.c
        self.d_ti.text = self.md.d

    def update_out(self, instance):
        r = self.md.get_registers()
        for i in range(32):
            self.r_l[i].text = r[i]

    def run_iter(self, instance):
        if self.disable_calc:
            self.show_popup("Calculations have been completed. Type a new password to hash and press enter to run again.")
            return
        try:
            finished = self.md.run_iter()
        except TypeError:
            self.show_popup("The message hasn't been acknowledged. Type a new password to hash and press enter to start.")
            return
        self.a_ti.text = str(self.md.a)
        self.b_ti.text = str(self.md.b)
        self.c_ti.text = str(self.md.c)
        self.d_ti.text = str(self.md.d)
        if finished:
            self.disable_calc = True
            r = self.md.get_registers()
            for i in range(32):
                self.r_l[i].text = r[i]

    def run_all(self, instance):
        if self.disable_calc:
            self.show_popup("Calculations have been completed. Type a new password to hash and press enter to run again.")
            return
        try:
            self.md.run_iter()
        except TypeError:
            self.show_popup("The message hasn't been acknowledged. Type a new password to hash and press enter to start.")
            return
        Clock.schedule_interval(self.run_all_async, 0.05)

    def run_all_async(self, dt):
        finished = self.md.run_iter()
        self.a_ti.text = str(self.md.a)    
        self.b_ti.text = str(self.md.b)
        self.c_ti.text = str(self.md.c)
        self.d_ti.text = str(self.md.d)
        if finished:
            self.disable_calc = True
            r = self.md.get_registers()
            for i in range(32):
                self.r_l[i].text = r[i]
        return not finished
    
    def show_popup(self, label_text=str):
        self.dialog = MDDialog(
            title='Warning',
            text=label_text,
            buttons=[
                MDFlatButton(text="OK", on_release=self.close_popup)
            ],
        )
        self.dialog.open()

    def close_popup(self, *args):
        self.dialog.dismiss()

    def toggle_theme(self, *args):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"

    def reset_variables(self, *args):
        self.h1_ti.text = '67452301'
        self.h2_ti.text = 'efcdab89'
        self.checkbox.active = True
        self.z1_ti.text = str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        self.z2_ti.text = str([1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12])
        self.z3_ti.text = str([5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2])
        self.z4_ti.text = str([0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9])
        self.s1_ti.text = str([7, 12, 17, 22])
        self.s2_ti.text = str([5, 9, 14, 20])
        self.s3_ti.text = str([4, 11, 16, 23])
        self.s4_ti.text = str([6, 10, 15, 21])
        self.message.text = "Password to hash"

    def check_if_number(self, instance):
        try:
            if len(instance.text) > 8:
                raise ValueError
            int(instance.text, 16)
        except ValueError:
            self.show_popup("Not a valid 8-bit hexadecimal constant.")
            instance.text = '00000000'

    def check_if_correct_z(self, instance):
        def parse_str_to_int(s):
            return [int(x.strip()) for x in s.strip('[]').split(',') if x.strip()]
        try:
            arr = parse_str_to_int(instance.text)
            if len(arr) < 16:
                self.show_popup("Not a valid 16 number array. Too short.")
                instance.text = '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'
                return
            elif len(arr) > 16:
                self.show_popup("Not a valid 16 number array. Too long.")
                instance.text = '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'
                return
            for i in arr:
                if i < 0 or i > 15:
                    self.show_popup("Not a valid 16 number array. Numbers must be in range from 0 to 15.")
                    instance.text = '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'
                    return
        except ValueError:
            self.show_popup("Not a valid 16 number array.")
            instance.text = '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'

    def check_if_correct_s(self, instance):
        def parse_str_to_int(s):
            return [int(x.strip()) for x in s.strip('[]').split(',') if x.strip()]
        try:
            arr = parse_str_to_int(instance.text)
            if len(arr) < 4:
                self.show_popup("Not a valid 4 number array. Too short.")
                instance.text = '[7, 12, 17, 22]'
                return
            elif len(arr) > 4:
                self.show_popup("Not a valid 4 number array. Too long.")
                instance.text = '[7, 12, 17, 22]'
                return
            for i in arr:
                if i < 0:
                    self.show_popup("Not a valid 16 number array. Numbers must be greater than 0 and should be less than 23.")
                    instance.text = '[7, 12, 17, 22]'
                    return
        except ValueError:
            self.show_popup("Not a valid 4 number array.")
            instance.text = '[7, 12, 17, 22]'
        



class InfoTooltipButton(MDIconButton, MDTooltip):
    pass
        

class MyTabbedPanel(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.tabs = MDTabs()
        self.add_widget(self.tabs)

        self.tabs.add_widget(TabMD4())
        self.tabs.add_widget(TabMD5())



class MyApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = np.random.choice(["Teal", "Amber", "DeepPurple", "Cyan", "Indigo", "Red", "Green"])
        self.theme_cls.theme_style = np.random.choice(["Light", "Dark"])
        Window.maximize()
        return MyTabbedPanel()
    
MyApp().run()

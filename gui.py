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
import ripemd160 as ripemd
import sha1
import hashlib
import numpy as np

class WelocomePanel(MDBoxLayout, MDTabsBase):
    def __init__(self, orientation: str ='vertical', **kwargs):
        super().__init__(**kwargs)
        self.icon='home'
        self.orientation = orientation
        self.padding = 20
        self.spacing = 20

        self.header = MDBoxLayout(size_hint_y=0.2, orientation='vertical')
        self.header.add_widget(
            MDLabel(
                text="Welcome to the Hash Functions Educational App!",
                halign="center",
                valign="middle",
                font_style="H4"
            )
        )
        self.header.add_widget(
            MDLabel(
                text="Explore the algorithms listed in the tabs above. Don't forget to see what's hidden under the info icon.",
                theme_text_color="Hint",
                halign="center",
                valign="middle",
            )
        )

        scroll = MDScrollView(size_hint_y=0.8, md_bg_color=self.theme_cls.primary_color)
        definition = MDLabel(
            text=(
                "[b]What is a hash function?[/b]\n"
                "A hash function is any function that can be used to map data of arbitrary size "
                "to fixed-size values. Hash functions are widely used in computer science, "
                "especially in cryptography, for tasks such as digital signatures and checksums.\n"
                "A one-way function is a function for which, given an input x, it is easy to compute "
                "the value f(x), but given a result y, it is computationally hard to find any x such that f(x) = y. "
                "When such a function takes messages M of arbitrary length and always produces outputs of fixed length, "
                "it is referred to as a hash function.\n\n"
                "In general, one-way hash functions should satisfy the following properties:\n"
                "- Given a message M, it is easy to compute f(M).\n"
                "- Given a hash value y = f(M), it is hard to find the original message M.\n"
                "- Given a message M, it is hard to find a different message M′ such that f(M) = f(M′).\n\n"
                "These properties make hash functions essential in cryptography, especially in ensuring "
                "data integrity and authenticity."
                "In real-world applications, cryptographic hash functions are used to securely store passwords, "
                "verify file integrity, and form the foundation of digital signatures and blockchain technologies. "
                "A good hash function should behave like a 'digital fingerprint': even a tiny change in the input "
                "should produce a completely different output, making it highly sensitive to input variations. "
                "Moreover, hash functions must be fast, deterministic, and resistant to collision attacks to be suitable "
                "for security-critical systems."
            ),
            markup=True,
            text_color=(1, 1, 1, 1),
            valign="top",
            padding=40
            # halign="center",
        )
        scroll.add_widget(definition)

        self.add_widget(self.header)
        self.add_widget(scroll)


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
            tooltip_text="Message Digest 4 was developed by Ronald Rivest in 1990. The security of MD4 has been severely compromised.\n" \
            "The first full collision attack against MD4 was published in 1995, and several newer attacks have been published since then.\n" \
            "As of 2007, an attack can generate collisions in less than two MD4 hash operations. A theoretical preimage attack also exists.\n" \
            "Operating principle:\n" \
            " - The message is padded to a multiple of 512 bits.\n" \
            " - For each 512-bit block, a transformation is applied that calculates a new internal state based on the current state and the block.\n" \
            " - After processing all blocks, the final state is returned as the result of the function.\n" \
            " - The transformation consists of rounds during which the following functions are executed: (x&y | ~x&z), (x&y | x&z | y&z), (x^y^z)\n" \
            " - Each round, beside main function, other operations are also made:\n" \
            "       t <- (A + f(B, C, D) + X[z[j]] + y[j])" \
            "       (A, B, C, D) <- (D, t << s[j], B, C)",
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
        
        # Chain constants
        chain_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        chain_row.add_widget(MDLabel(text="Enter chain constants:", size_hint=(0.09, self.widget_height)))
        chain_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The chain constants are used to initialize operating registers a, b, c, d and output registers h1, h2, h3, h4\n" \
            "The values of third and fourth constants are reversed respectively to second and first number.",
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

        # Additivie constants
        add_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        add_row.add_widget(MDLabel(text="Enter additive constants:", halign='left', size_hint=(0.11, self.widget_height)))
        add_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The additive constants adds up to the temporary register.\n" \
            "Three constants are given, each for one round.\n" \
            "Originally these constants are 0, square root of 2 and square root of 3.",
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
            tooltip_text="Each round there is a different order of taking message block part for computing. \n" \
            "When setting your own, make sure to do a permutation containing all indices from 0 to 15.",
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
            tooltip_text="Also each round the left shift is by other number.",
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
            tooltip_text="The output digest size will be same length every time, regardless the length of this message.",
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
            tooltip_text="The operating registers. Keeping track of what's happening inside.",
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
            tooltip_text="The final state displayed in little-endian (as typical).\n" \
            "After each transformation the output registers update (H1, H2, H3, H4) <- (H1 + A, H2 + B, H3 + C, H4 + D)",
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
            tooltip_text="Message Digest 5 was designed by Ronald Rivest in 1991 to replace an earlier and less secure hash function MD4.\n" \
                         "However it has been found to suffer from extensive vulnerabilities\n." \
                         "It remains suitable for other non-cryptographic purposes, for example for determining the partition for a particular key in a partitioned database, \n"
                         "and may be preferred due to lower computational requirements than more recent Secure Hash Algorithms. \n" \
                         "Main change to the MD4 is fourth round and executed functions: (x&y | ~x&z), (x&z | y&~z), (x^y^z), (y ^ x|~z)",
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
            tooltip_text="The chain constants are used to initialize operating registers a, b, c, d and output registers h1, h2, h3, h4\n" \
            "The values of third and fourth constants are reversed respectively to second and first number.",
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
            tooltip_text="Different to MD4, the MD5 additive constants are unique not only for each round, but also for each iteration. \n" \
            "Originally they are stated as abs(sin(j)) for j from 1 to 64.",
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
            tooltip_text="In MD5 there are 4 rounds of calculations, so 4 permutation arrays.",
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
            tooltip_text="Also 4 shuffle arrays.",
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
            tooltip_text="The output digest size will be same length every time, regardless the length of this message.",
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
            tooltip_text="The operating registers. Keeping track of what's happening inside.",
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
            tooltip_text="The final state displayed in little-endian (as typical).\n" \
            "After each transformation the output registers update (H1, H2, H3, H4) <- (H1 + A, H2 + B, H3 + C, H4 + D)",
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


class TabSHA1(MDStackLayout, MDTabsBase):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.title="SHA-1"

        scroll = MDScrollView(do_scroll_x=True, do_scroll_y=True)
        content = ContentSHA1(orientation=orientation)

        scroll.add_widget(content)
        self.add_widget(scroll)


class ContentSHA1(MDStackLayout):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'lr-tb'
        self.adaptive_height = True
        self.padding = 20
        # self.adaptive_width = True # RAM eater

        self.widget_height = 0.03
        self.sha = sha1.SHA1()
        self.disable_calc = False

        hello_label = MDLabel(text=f"SHA-1 algorithm", font_style="H4", size_hint=(0.55, self.widget_height * 4), halign="right", valign="middle")
        hello_label.bind(size=hello_label.setter("text_size"))
        self.add_widget(hello_label)

        hello_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="Secure Hash Algorithm 1 was designed in 1995 by the United States National Security Agency. \n" \
            "Since 2005, SHA-1 has not been considered secure against well-funded opponents. \n" \
            "SHA-1 produces a message digest based on principles similar to those used in the design of the MD4\\5 message digest algorithms, but generates a larger hash value (160 bits vs. 128 bits). \n" \
            "Similarly to MD5 there are 4 rounds with functions: (x&y | ~x&z), (x^y^z), (x&y ^ x&z ^ y&z), (x^y^z)," \
            "but the shuffle and order arrays are not in use.",
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
            tooltip_text="As there is a 160 bit output, the fifth chain constant has been introduced.",
            size_hint=(None, self.widget_height * 4)
        )
        chain_row.add_widget(chain_info)
        self.add_widget(chain_row)
        self.add_widget(MDLabel(text="h1:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="h2:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="h3:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="h4:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="h5:", halign='left', size_hint=(0.2, self.widget_height)))

        h1_def = '67452301'
        self.h1_ti = MDTextField(text=h1_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h1_ti)

        h2_def = 'efcdab89'
        self.h2_ti = MDTextField(text=h2_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h2_ti)

        h3_def, h4_def = md4.chain_constraints(h1_def, h2_def)
        self.h3_ti = MDTextField(text=h3_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const, readonly=True)
        self.add_widget(self.h3_ti)

        self.h4_ti = MDTextField(text=h4_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const, readonly=True)
        self.add_widget(self.h4_ti)

        h5_def = 'c3d2e1f0'
        self.h5_ti = MDTextField(text=h5_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h5_ti)

        # Additivie constaints
        add_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        add_row.add_widget(MDLabel(text="Enter additive constants:", halign='left', size_hint=(0.1, self.widget_height)))
        add_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="These constants were hand-chosen constants, likely for cryptographic properties and balance in bitwise logic,\n" \
            "but not mathematically derived from irrational numbers (like in MD algorithms).",
            size_hint=(None, self.widget_height * 4)
        )
        add_row.add_widget(add_info)
        self.add_widget(add_row)
        self.add_widget(MDLabel(text="y1:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="y2:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="y3:", halign='left', size_hint=(0.25, self.widget_height)))
        self.add_widget(MDLabel(text="y4:", halign='left', size_hint=(0.25, self.widget_height)))


        y1_def = '5a827999'
        self.y1_ti = MDTextField(text=y1_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y1_ti)

        y2_def = '6ed9eba1'
        self.y2_ti = MDTextField(text=y2_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y2_ti)

        y3_def = '8f1bbcdc'
        self.y3_ti = MDTextField(text=y3_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y3_ti)

        y4_def = 'ca62c1d6'
        self.y4_ti = MDTextField(text=y4_def, multiline=False, size_hint=(0.25, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y4_ti)

        mess_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        mess_row.add_widget(MDLabel(text="Enter message to encrypt:", halign='left', size_hint=(0.1, self.widget_height)))
        mess_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The output digest size will be same length every time, regardless the length of this message.",
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
            tooltip_text="The operating registers. Keeping track of what's happening inside.",
            size_hint=(None, self.widget_height * 30)
        )
        reg_row.add_widget(reg_info)
        self.add_widget(reg_row)

        self.add_widget(MDLabel(text="a:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="b:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="c:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="d:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="e:", halign='left', size_hint=(0.2, self.widget_height)))

        self.a_ti = MDTextField(text=str(self.sha.a),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.a_ti)

        self.b_ti = MDTextField(text=str(self.sha.b),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.b_ti)

        self.c_ti = MDTextField(text=str(self.sha.c),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.c_ti)

        self.d_ti = MDTextField(text=str(self.sha.d),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.d_ti)

        self.e_ti = MDTextField(text=str(self.sha.e),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.e_ti)

        final_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        final_row.add_widget(MDLabel(text="Final output:", halign='left', size_hint=(0.06, self.widget_height)))
        final_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The final state displayed in little-endian (as typical).",
            size_hint=(None, self.widget_height * 4)
        )
        final_row.add_widget(final_info)
        self.add_widget(final_row)
        
        r = self.sha.get_registers()
        self.r_l = [None for _ in range(40)]
        for i in range(40):
            self.r_l[i] = MDTextField(text=r[i], size_hint=(1/40, self.widget_height), multiline=False,  on_text_validate=self.update_out, readonly=True)
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


    def initialize(self, instance):
        try:
            self.sha = sha1.SHA1(self.message.text, self.h1_ti.text, self.h2_ti.text, self.h5_ti.text,
                                            self.y1_ti.text, self.y2_ti.text, self.y3_ti.text, self.y4_ti.text)

        except ValueError:
            self.show_popup("The message can't be empty.")
            return
        self.disable_calc = False

    def update_reg(self, instance):
        self.a_ti.text = str(self.sha.a)
        self.b_ti.text = str(self.sha.b)
        self.c_ti.text = str(self.sha.c)
        self.d_ti.text = str(self.sha.d)
        self.e_ti.text = str(self.sha.e)

    def update_out(self, instance):
        r = self.ripemd.get_registers()
        for i in range(40):
            self.r_l[i].text = r[i]

    def run_iter(self, instance):
        if self.disable_calc:
            self.show_popup("Calculations have been completed. Type a new password to hash and press enter to run again.")
            return
        try:
            finished = self.sha.run_iter()
        except AttributeError:
            self.show_popup("The message hasn't been acknowledged. Type a new password to hash and press enter to start.")
            return
        self.a_ti.text = str(self.sha.a)
        self.b_ti.text = str(self.sha.b)
        self.c_ti.text = str(self.sha.c)
        self.d_ti.text = str(self.sha.d)
        self.e_ti.text = str(self.sha.e)
        if finished:
            self.disable_calc = True
            r = self.sha.get_registers()
            for i in range(40):
                self.r_l[i].text = r[i]

    def run_all(self, instance):
        if self.disable_calc:
            self.show_popup("Calculations have been completed. Type a new password to hash and press enter to run again.")
            return
        try:
            self.sha.run_iter()
        except AttributeError:
            self.show_popup("The message hasn't been acknowledged. Type a new password to hash and press enter to start.")
            return
        Clock.schedule_interval(self.run_all_async, 0.05)

    def run_all_async(self, dt):
        finished = self.sha.run_iter()
        self.a_ti.text = str(self.sha.a)
        self.b_ti.text = str(self.sha.b)
        self.c_ti.text = str(self.sha.c)
        self.d_ti.text = str(self.sha.d)
        self.e_ti.text = str(self.sha.e)
        if finished:
            self.disable_calc = True
            r = self.sha.get_registers()
            for i in range(40):
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
        self.h5_ti.text = 'c3d2e1f0'
        self.y1_ti.text = '5a827999'
        self.y2_ti.text = '6ed9eba1'
        self.y3_ti.text = '8f1bbcdc'
        self.y4_ti.text = 'ca62c1d6'
        self.message.text = "Password to hash"

    def check_if_number(self, instance):
        try:
            if len(instance.text) > 8:
                raise ValueError
            int(instance.text, 16)
        except ValueError:
            self.show_popup("Not a valid 8-bit hexadecimal constant.")
            instance.text = '00000000'


class TabRIPEMD(MDStackLayout, MDTabsBase):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.title="RIPEMD-160"

        scroll = MDScrollView(do_scroll_x=True, do_scroll_y=True)
        content = ContentRIPEMD(orientation=orientation)

        scroll.add_widget(content)
        self.add_widget(scroll)


class ContentRIPEMD(MDStackLayout):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'lr-tb'
        self.adaptive_height = True
        self.padding = 20
        # self.adaptive_width = True # RAM eater

        self.widget_height = 0.03
        self.ripemd = ripemd.RIPEMD160()
        self.disable_calc = False

        hello_label = MDLabel(text=f"RIPEMD-160 algorithm", font_style="H4", size_hint=(0.55, self.widget_height * 4), halign="right", valign="middle")
        hello_label.bind(size=hello_label.setter("text_size"))
        self.add_widget(hello_label)

        hello_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="RIPE Message Digest is a family of cryptographic hash functions developed between 1992 and 1996. RIPEMD-160 is the most common. They were designed to be more durable than MD4\\5. \n" \
                         "The original RIPEMD, as well as RIPEMD-128, is not considered secure because 128-bit result is too small and also (for the original RIPEMD) because of design weaknesses.\n" \
                         "The 256- and 320-bit versions of RIPEMD provide the same level of security as RIPEMD-128 and RIPEMD-160, respectively; they are designed for applications where the security level is sufficient but longer hash result is necessary. \n" \
                         "While RIPEMD functions are less popular than SHA-1 and SHA-2, they are used, among others, in Bitcoin and other cryptocurrencies based on Bitcoin. \n" \
                         "In this algorithm, each data block is computed in parallel by left and right path, which differ in constants.",
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
            tooltip_text="As there is a 160 bit output, the fifth chain constant is needed.",
            size_hint=(None, self.widget_height * 4)
        )
        chain_row.add_widget(chain_info)
        self.add_widget(chain_row)
        self.add_widget(MDLabel(text="h1:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="h2:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="h3:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="h4:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="h5:", halign='left', size_hint=(0.2, self.widget_height)))

        h1_def = '67452301'
        self.h1_ti = MDTextField(text=h1_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h1_ti)

        h2_def = 'efcdab89'
        self.h2_ti = MDTextField(text=h2_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h2_ti)

        h3_def, h4_def = md4.chain_constraints(h1_def, h2_def)
        self.h3_ti = MDTextField(text=h3_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const, readonly=True)
        self.add_widget(self.h3_ti)

        self.h4_ti = MDTextField(text=h4_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const, readonly=True)
        self.add_widget(self.h4_ti)

        h5_def = 'c3d2e1f0'
        self.h5_ti = MDTextField(text=h5_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_chain_const)
        self.add_widget(self.h5_ti)

        # Additivie constants L
        add_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        add_row.add_widget(MDLabel(text="Enter additive constants left:", halign='left', size_hint=(0.11, self.widget_height)))
        add_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The left constants are respectively squre roots of 0, 2, 3, 5, 7 (First prime numbers + 0).",
            size_hint=(None, self.widget_height * 4)
        )
        add_row.add_widget(add_info)
        self.add_widget(add_row)
        self.add_widget(MDLabel(text="yL1:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="yL2:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="yL3:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="yL4:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="yL5:", halign='left', size_hint=(0.2, self.widget_height)))


        y1_def = '00000000'
        self.y1_ti = MDTextField(text=y1_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y1_ti)

        y2_def = '5a827999'
        self.y2_ti = MDTextField(text=y2_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y2_ti)

        y3_def = '6ed9eba1'
        self.y3_ti = MDTextField(text=y3_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y3_ti)

        y4_def = '8f1bbcdc'
        self.y4_ti = MDTextField(text=y4_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y4_ti)

        y5_def = '0953fd4e'
        self.y5_ti = MDTextField(text=y5_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y5_ti)

        # Additivie constaints R
        add_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        add_row.add_widget(MDLabel(text="Enter additive constants right:", halign='left', size_hint=(0.13, self.widget_height)))
        add_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The right constants are respectively cube roots of same numbers: 0, 2, 3, 5, 7.",
            size_hint=(None, self.widget_height * 4)
        )
        add_row.add_widget(add_info)
        self.add_widget(add_row)
        self.add_widget(MDLabel(text="yR1:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="yR2:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="yR3:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="yR4:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="yR5:", halign='left', size_hint=(0.2, self.widget_height)))


        y1_def = '50a28be6'
        self.y1_tir = MDTextField(text=y1_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y1_tir)

        y2_def = '5c4dd124'
        self.y2_tir = MDTextField(text=y2_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y2_tir)

        y3_def = '6d703ef3'
        self.y3_tir = MDTextField(text=y3_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y3_tir)

        y4_def = '7a6d76e9'
        self.y4_tir = MDTextField(text=y4_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y4_tir)

        y5_def = '00000000'
        self.y5_tir = MDTextField(text=y5_def, multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.check_if_number)
        self.add_widget(self.y5_tir)

        # Order lists left
        order_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        order_row.add_widget(MDLabel(text="Enter order lists left:", halign='left', size_hint=(0.08, self.widget_height)))
        order_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="Permutations",
            size_hint=(None, self.widget_height * 4)
        )
        order_row.add_widget(order_info)
        self.add_widget(order_row)
        self.add_widget(MDLabel(text="zL1:", halign='left', size_hint=(0.9 * 0.2, self.widget_height)))
        self.add_widget(MDLabel(text="zL2:", halign='left', size_hint=(0.9 * 0.2, self.widget_height)))
        self.add_widget(MDLabel(text="zL3:", halign='left', size_hint=(0.9 * 0.2, self.widget_height)))
        self.add_widget(MDLabel(text="zL4:", halign='left', size_hint=(0.9 * 0.2, self.widget_height)))
        self.add_widget(MDLabel(text="zL5:", halign='left', size_hint=(0.28, self.widget_height)))

        self.z1_def = str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        self.z1_ti = MDTextField(text=self.z1_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z1_ti)

        self.z2_def = str([7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8])
        self.z2_ti = MDTextField(text=self.z2_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z2_ti)

        self.z3_def = str([3,10,14, 4, 9,15, 8, 1, 2, 7, 0, 6,13,11, 5,12])
        self.z3_ti = MDTextField(text=self.z3_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z3_ti)

        self.z4_def = str([1, 9,11,10, 0, 8,12, 4,13, 3, 7,15,14, 5, 6, 2])
        self.z4_ti = MDTextField(text=self.z4_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z4_ti)

        self.z5_def = str([4, 0, 5, 9, 7,12, 2,10,14, 1, 3, 8,11, 6,15,13])
        self.z5_ti = MDTextField(text=self.z5_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z5_ti)

        self.add_widget(MDRaisedButton(text="Shuffle", on_press=self.shuffle_zl, size_hint=(0.1, self.widget_height)))

        # Order lists right
        order_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        order_row.add_widget(MDLabel(text="Enter order lists left:", halign='left', size_hint=(0.08, self.widget_height)))
        order_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="Permutations",
            size_hint=(None, self.widget_height * 4)
        )
        order_row.add_widget(order_info)
        self.add_widget(order_row)
        self.add_widget(MDLabel(text="zR1:", halign='left', size_hint=(0.9 * 0.2, self.widget_height)))
        self.add_widget(MDLabel(text="zR2:", halign='left', size_hint=(0.9 * 0.2, self.widget_height)))
        self.add_widget(MDLabel(text="zR3:", halign='left', size_hint=(0.9 * 0.2, self.widget_height)))
        self.add_widget(MDLabel(text="zR4:", halign='left', size_hint=(0.9 * 0.2, self.widget_height)))
        self.add_widget(MDLabel(text="zR5:", halign='left', size_hint=(0.28, self.widget_height)))

        self.z1_def = str([5,14, 7, 0, 9, 2,11, 4,13, 6,15, 8, 1,10, 3,12])
        self.z1_tir = MDTextField(text=self.z1_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z1_tir)

        self.z2_def = str([6,11, 3, 7, 0,13, 5,10,14,15, 8,12, 4, 9, 1, 2])
        self.z2_tir = MDTextField(text=self.z2_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z2_tir)

        self.z3_def = str([15, 5, 1, 3, 7,14, 6, 9,11, 8,12, 2,10, 0, 4,13])
        self.z3_tir = MDTextField(text=self.z3_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z3_tir)

        self.z4_def = str([8, 6, 4, 1, 3,11,15, 0, 5,12, 2,13, 9, 7,10,14])
        self.z4_tir = MDTextField(text=self.z4_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z4_tir)

        self.z5_def = str([12,15,10, 4, 1, 5, 8, 7, 6, 2,13,14, 0, 3, 9,11])
        self.z5_tir = MDTextField(text=self.z5_def, multiline=False, size_hint=(0.9 * 0.2, self.widget_height), on_text_validate=self.check_if_correct_z)
        self.add_widget(self.z5_tir)

        self.add_widget(MDRaisedButton(text="Shuffle", on_press=self.shuffle_zr, size_hint=(0.1, self.widget_height)))


        # Shuffle lists left
        shuffle_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        shuffle_row.add_widget(MDLabel(text="Enter shuffle lists left:", halign='left', size_hint=(0.1, self.widget_height)))
        shuffle_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="Random integers to decide by how many to shift",
            size_hint=(None, self.widget_height * 4)
        )
        shuffle_row.add_widget(shuffle_info)
        self.add_widget(shuffle_row)
        self.add_widget(MDLabel(text="sL1:", halign='left', size_hint=(0.9*0.2, self.widget_height)))
        self.add_widget(MDLabel(text="sL2:", halign='left', size_hint=(0.9*0.2, self.widget_height)))
        self.add_widget(MDLabel(text="sL3:", halign='left', size_hint=(0.9*0.2, self.widget_height)))
        self.add_widget(MDLabel(text="sL4:", halign='left', size_hint=(0.9*0.2, self.widget_height)))
        self.add_widget(MDLabel(text="sL5:", halign='left', size_hint=(0.28, self.widget_height)))

        self.s1_def = str([11,14,15,12, 5, 8, 7, 9,11,13,14,15, 6, 7, 9, 8])
        self.s1_ti = MDTextField(text=self.s1_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s1_ti)

        self.s2_def = str([7, 6, 8,13,11, 9, 7,15, 7,12,15, 9,11, 7,13,12])
        self.s2_ti = MDTextField(text=self.s2_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s2_ti)

        self.s3_def = str([11,13, 6, 7,14, 9,13,15,14, 8,13, 6, 5,12, 7, 5])
        self.s3_ti = MDTextField(text=self.s3_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s3_ti)

        self.s4_def = str([11,12,14,15,14,15, 9, 8, 9,14, 5, 6, 8, 6, 5,12])
        self.s4_ti = MDTextField(text=self.s4_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s4_ti)

        self.s5_def = str([9,15, 5,11, 6, 8,13,12, 5,12,13,14,11, 8, 5, 6])
        self.s5_ti = MDTextField(text=self.s5_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s5_ti)

        self.add_widget(MDRaisedButton(text="Shuffle", on_press=self.shuffle_sl, size_hint=(0.1, self.widget_height)))

        # Shuffle lists right
        shuffle_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        shuffle_row.add_widget(MDLabel(text="Enter shuffle lists right:", halign='left', size_hint=(0.1, self.widget_height)))
        shuffle_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="Random integers to decide by how many to shift",
            size_hint=(None, self.widget_height * 4)
        )
        shuffle_row.add_widget(shuffle_info)
        self.add_widget(shuffle_row)
        self.add_widget(MDLabel(text="sR1:", halign='left', size_hint=(0.9*0.2, self.widget_height)))
        self.add_widget(MDLabel(text="sR2:", halign='left', size_hint=(0.9*0.2, self.widget_height)))
        self.add_widget(MDLabel(text="sR3:", halign='left', size_hint=(0.9*0.2, self.widget_height)))
        self.add_widget(MDLabel(text="sR4:", halign='left', size_hint=(0.9*0.2, self.widget_height)))
        self.add_widget(MDLabel(text="sR5:", halign='left', size_hint=(0.28, self.widget_height)))

        self.s1_def = str([8, 9, 9,11,13,15,15, 5, 7, 7, 8,11,14,14,12, 6])
        self.s1_tir = MDTextField(text=self.s1_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s1_tir)

        self.s2_def = str([9,13,15, 7,12, 8, 9,11, 7, 7,12, 7, 6,15,13,11])
        self.s2_tir = MDTextField(text=self.s2_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s2_tir)

        self.s3_def = str([9, 7,15,11, 8, 6, 6,14,12,13, 5,14,13,13, 7, 5])
        self.s3_tir = MDTextField(text=self.s3_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s3_tir)

        self.s4_def = str([15, 5, 8,11,14,14, 6,14, 6, 9,12, 9,12, 5,15, 8])
        self.s4_tir = MDTextField(text=self.s4_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s4_tir)

        self.s5_def = str([8, 5,12, 9,12, 5,14, 6, 8,13, 6, 5,15,13,11,11])
        self.s5_tir = MDTextField(text=self.s5_def, multiline=False, size_hint=(0.9*0.2, self.widget_height), on_text_validate=self.check_if_correct_s)
        self.add_widget(self.s5_tir)

        self.add_widget(MDRaisedButton(text="Shuffle", on_press=self.shuffle_sr, size_hint=(0.1, self.widget_height)))

        mess_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        mess_row.add_widget(MDLabel(text="Enter message to encrypt:", halign='left', size_hint=(0.1, self.widget_height)))
        mess_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The output digest size will be same length every time, regardless the length of this message.",
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
            tooltip_text="The operating registers. Keeping track of what's happening inside.",
            size_hint=(None, self.widget_height * 24)
        )
        reg_row.add_widget(reg_info)
        self.add_widget(reg_row)

        self.add_widget(MDLabel(text="a:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="b:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="c:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="d:", halign='left', size_hint=(0.2, self.widget_height)))
        self.add_widget(MDLabel(text="e:", halign='left', size_hint=(0.2, self.widget_height)))

        self.a_ti = MDTextField(text=str(self.ripemd.A),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.a_ti)

        self.b_ti = MDTextField(text=str(self.ripemd.B),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.b_ti)

        self.c_ti = MDTextField(text=str(self.ripemd.C),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.c_ti)

        self.d_ti = MDTextField(text=str(self.ripemd.D),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.d_ti)

        self.e_ti = MDTextField(text=str(self.ripemd.E),
                               multiline=False, size_hint=(0.2, self.widget_height), on_text_validate=self.update_reg, readonly=True)
        self.add_widget(self.e_ti)

        final_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        final_row.add_widget(MDLabel(text="Final output:", halign='left', size_hint=(0.06, self.widget_height)))
        final_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The final state displayed in little-endian (as typical).",
            size_hint=(None, self.widget_height * 4)
        )
        final_row.add_widget(final_info)
        self.add_widget(final_row)
        
        r = self.ripemd.get_registers()
        self.r_l = [None for _ in range(40)]
        for i in range(40):
            self.r_l[i] = MDTextField(text=r[i], size_hint=(1/40, self.widget_height), multiline=False,  on_text_validate=self.update_out, readonly=True)
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

    def shuffle_zl(self, instance):
        self.z1_ti.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z2_ti.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z3_ti.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z4_ti.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z5_ti.text = str(np.random.permutation(np.arange(16)).tolist())

    def shuffle_zr(self, instance):
        self.z1_tir.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z2_tir.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z3_tir.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z4_tir.text = str(np.random.permutation(np.arange(16)).tolist())
        self.z5_tir.text = str(np.random.permutation(np.arange(16)).tolist())

    def shuffle_sl(self, instance):
        self.s1_ti.text = str(np.random.random_integers(15, size=(16,)).tolist())
        self.s2_ti.text = str(np.random.random_integers(15, size=(16,)).tolist())
        self.s3_ti.text = str(np.random.random_integers(15, size=(16,)).tolist())
        self.s4_ti.text = str(np.random.random_integers(15, size=(16,)).tolist())
        self.s5_ti.text = str(np.random.random_integers(15, size=(16,)).tolist())

    def shuffle_sr(self, instance):
        self.s1_tir.text = str(np.random.random_integers(15, size=(16,)).tolist())
        self.s2_tir.text = str(np.random.random_integers(15, size=(16,)).tolist())
        self.s3_tir.text = str(np.random.random_integers(15, size=(16,)).tolist())
        self.s4_tir.text = str(np.random.random_integers(15, size=(16,)).tolist())
        self.s5_tir.text = str(np.random.random_integers(15, size=(16,)).tolist())

    

    def initialize(self, instance):
        def parse_str_to_int(s):
            return [int(x.strip()) for x in s.strip('[]').split(',') if x.strip()]
        try:
            self.ripemd = ripemd.RIPEMD160(self.message.text, self.h1_ti.text, self.h2_ti.text, self.h5_ti.text,
                                            self.y1_ti.text, self.y2_ti.text, self.y3_ti.text, self.y4_ti.text, self.y5_ti.text,
                                            self.y1_tir.text, self.y2_tir.text, self.y3_tir.text, self.y4_tir.text, self.y5_tir.text,
                        parse_str_to_int(self.z1_ti.text),
                        parse_str_to_int(self.z2_ti.text),
                        parse_str_to_int(self.z3_ti.text),
                        parse_str_to_int(self.z4_ti.text),
                        parse_str_to_int(self.z5_ti.text),
                        parse_str_to_int(self.z1_tir.text),
                        parse_str_to_int(self.z2_tir.text),
                        parse_str_to_int(self.z3_tir.text),
                        parse_str_to_int(self.z4_tir.text),
                        parse_str_to_int(self.z5_tir.text),
                        parse_str_to_int(self.s1_ti.text),
                        parse_str_to_int(self.s2_ti.text),
                        parse_str_to_int(self.s3_ti.text),
                        parse_str_to_int(self.s4_ti.text),
                        parse_str_to_int(self.s5_ti.text),
                        parse_str_to_int(self.s1_tir.text),
                        parse_str_to_int(self.s2_tir.text),
                        parse_str_to_int(self.s3_tir.text),
                        parse_str_to_int(self.s4_tir.text),
                        parse_str_to_int(self.s5_tir.text))
        except ValueError:
            self.show_popup("The message can't be empty.")
            return
        self.disable_calc = False

    def update_reg(self, instance):
        self.a_ti.text = self.ripemd.A
        self.b_ti.text = self.ripemd.B
        self.c_ti.text = self.ripemd.C
        self.d_ti.text = self.ripemd.D
        self.e_ti.text = self.ripemd.E

    def update_out(self, instance):
        r = self.ripemd.get_registers()
        for i in range(40):
            self.r_l[i].text = r[i]

    def run_iter(self, instance):
        if self.disable_calc:
            self.show_popup("Calculations have been completed. Type a new password to hash and press enter to run again.")
            return
        try:
            finished = self.ripemd.run_iter()
        except TypeError:
            self.show_popup("The message hasn't been acknowledged. Type a new password to hash and press enter to start.")
            return
        self.a_ti.text = str(self.ripemd.A)
        self.b_ti.text = str(self.ripemd.B)
        self.c_ti.text = str(self.ripemd.C)
        self.d_ti.text = str(self.ripemd.D)
        self.e_ti.text = str(self.ripemd.E)
        if finished:
            self.disable_calc = True
            r = self.ripemd.get_registers()
            for i in range(40):
                self.r_l[i].text = r[i]

    def run_all(self, instance):
        if self.disable_calc:
            self.show_popup("Calculations have been completed. Type a new password to hash and press enter to run again.")
            return
        try:
            self.ripemd.run_iter()
        except TypeError:
            self.show_popup("The message hasn't been acknowledged. Type a new password to hash and press enter to start.")
            return
        Clock.schedule_interval(self.run_all_async, 0.05)

    def run_all_async(self, dt):
        finished = self.ripemd.run_iter()
        self.a_ti.text = str(self.ripemd.A)
        self.b_ti.text = str(self.ripemd.B)
        self.c_ti.text = str(self.ripemd.C)
        self.d_ti.text = str(self.ripemd.D)
        self.e_ti.text = str(self.ripemd.E)
        if finished:
            self.disable_calc = True
            r = self.ripemd.get_registers()
            for i in range(40):
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
        self.h5_ti.text = 'c3d2e1f0'
        self.y1_ti.text = '00000000'
        self.y2_ti.text = '5a827999'
        self.y3_ti.text = '6ed9eba1'
        self.y4_ti.text = '8f1bbcdc'
        self.y5_ti.text = '0953fd4e'
        self.y1_tir.text = '50a28be6'
        self.y2_tir.text = '5c4dd124'
        self.y3_tir.text = '6d703ef3'
        self.y4_tir.text = '7a6d76e9'
        self.y5_tir.text = '00000000'
        self.z1_ti.text = str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        self.z2_ti.text = str([7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8])
        self.z3_ti.text = str([3,10,14, 4, 9,15, 8, 1, 2, 7, 0, 6,13,11, 5,12])
        self.z4_ti.text = str([1, 9,11,10, 0, 8,12, 4,13, 3, 7,15,14, 5, 6, 2])
        self.z5_ti.text = str([4, 0, 5, 9, 7,12, 2,10,14, 1, 3, 8,11, 6,15,13])
        self.z1_tir.text = str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        self.z2_tir.text = str([7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8])
        self.z3_tir.text = str([3,10,14, 4, 9,15, 8, 1, 2, 7, 0, 6,13,11, 5,12])
        self.z4_tir.text = str([1, 9,11,10, 0, 8,12, 4,13, 3, 7,15,14, 5, 6, 2])
        self.z5_tir.text = str([4, 0, 5, 9, 7,12, 2,10,14, 1, 3, 8,11, 6,15,13])
        self.s1_ti.text = str([11,14,15,12, 5, 8, 7, 9,11,13,14,15, 6, 7, 9, 8])
        self.s2_ti.text = str([7, 6, 8,13,11, 9, 7,15, 7,12,15, 9,11, 7,13,12])
        self.s3_ti.text = str([11,13, 6, 7,14, 9,13,15,14, 8,13, 6, 5,12, 7, 5])
        self.s4_ti.text = str([11,12,14,15,14,15, 9, 8, 9,14, 5, 6, 8, 6, 5,12])
        self.s5_ti.text = str([9,15, 5,11, 6, 8,13,12, 5,12,13,14,11, 8, 5, 6])
        self.s1_tir.text = str([8, 9, 9,11,13,15,15, 5, 7, 7, 8,11,14,14,12, 6])
        self.s2_tir.text = str([9,13,15, 7,12, 8, 9,11, 7, 7,12, 7, 6,15,13,11])
        self.s3_tir.text = str([9, 7,15,11, 8, 6, 6,14,12,13, 5,14,13,13, 7, 5])
        self.s4_tir.text = str([15, 5, 8,11,14,14, 6,14, 6, 9,12, 9,12, 5,15, 8])
        self.s5_tir.text = str([8, 5,12, 9,12, 5,14, 6, 8,13, 6, 5,15,13,11,11])
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

        
class TabWhirlpool(MDStackLayout, MDTabsBase):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.title="Whirlpool"

        scroll = MDScrollView(do_scroll_x=True, do_scroll_y=True)
        content = ContentWhirlpool(orientation=orientation)

        scroll.add_widget(content)
        self.add_widget(scroll)


class ContentWhirlpool(MDStackLayout):
    def __init__(self, orientation: str ='lr-tb', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'lr-tb'
        self.adaptive_height = True
        self.padding = 20
        # self.adaptive_width = True # RAM eater

        self.widget_height = 0.03
        self.disable_calc = False

        self.alg = '0' * 128

        hello_label = MDLabel(text=f"Whirlpool algorithm", font_style="H4", size_hint=(0.55, self.widget_height * 4), halign="right", valign="middle")
        hello_label.bind(size=hello_label.setter("text_size"))
        self.add_widget(hello_label)

        hello_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="Whirlpool was designed by Vincent Rijmen and Paulo S. L. M. Barreto, who first described it in 2000. \n" \
            "Whirlpool is a hash designed after the Square block cipher, and is considered to be in that family of block cipher functions and also is based on a substantially modified Advanced Encryption Standard (AES). \n" \
            "Whirlpool takes a message of any length less than 2256 bits and returns a 512-bit message digest. \n" \
            "Internal structure: \n" \
            " - The input message is split into 512-bit blocks.\n" \
            " - Each block is processed through a 10-round transformation.\n" \
            " - Each round includes: \n" \
            "    - SubBytes - byte-wise substitution using a fixed 8-bit S-box.\n" \
            "    - ShiftColumns - cyclic permutation of columns.\n" \
            "    - MixRows - diffusion step using a fixed binary matrix over GF(2^8)\n" \
            "    - AddRoundKey - XOR with round key derived from the message block and round constants.",
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

        mess_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height))
        mess_row.add_widget(MDLabel(text="Enter message to encrypt:", halign='left', size_hint=(0.1, self.widget_height)))
        mess_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The output digest size will be same length every time, regardless the length of this message.",
            size_hint=(None, self.widget_height * 4)
        )
        mess_row.add_widget(mess_info)
        self.add_widget(mess_row)
        self.message = MDTextField(text="Password to hash", size_hint=(0.8, self.widget_height))
        self.add_widget(self.message)
        
        self.add_widget(MDRaisedButton(text="Enter", on_press=self.initialize, size_hint=(0.2, self.widget_height)))


        self.add_widget(MDRaisedButton(text="Run all",
                               on_press=self.run_all,
                               size_hint=(1, self.widget_height)))

        final_row = MDStackLayout(orientation='lr-tb', size_hint=(1, self.widget_height * 6))
        final_row.add_widget(MDLabel(text="Final output:", halign='left', size_hint=(0.06, self.widget_height * 6)))
        final_info = InfoTooltipButton(
            icon="information-outline",
            tooltip_text="The final state displayed in little-endian (as typical).",
            size_hint=(None, self.widget_height * 6)
        )
        final_row.add_widget(final_info)
        self.add_widget(final_row)
        
        r = self.alg
        self.r_l = [None for _ in range(128)]
        for i in range(128):
            self.r_l[i] = MDTextField(text=r[i], size_hint=(1/32, self.widget_height), multiline=False,  on_text_validate=self.update_out, readonly=True)
            self.add_widget(self.r_l[i])

    def initialize(self, instance):
        try:
            self.alg = hashlib.new('whirlpool', self.message.text.encode()).hexdigest()

        except ValueError:
            self.show_popup("The message can't be empty.")
            return
        self.disable_calc = False

    def update_out(self, instance):
        r = self.alg
        for i in range(128):
            self.r_l[i].text = r[i]

    def run_all(self, instance):
        if self.disable_calc:
            self.show_popup("Calculations have been completed. Type a new password to hash and press enter to run again.")
            return
        if self.alg == '0' * 128:
            self.show_popup("The message hasn't been acknowledged. Type a new password to hash and press enter to start.")
            return
        r = self.alg
        for i in range(128):
            self.r_l[i].text = r[i]
    
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




class InfoTooltipButton(MDIconButton, MDTooltip):
    pass
        

class MyTabbedPanel(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.tabs = MDTabs()
        self.add_widget(self.tabs)

        self.tabs.add_widget(WelocomePanel())
        self.tabs.add_widget(TabMD4())
        self.tabs.add_widget(TabMD5())
        self.tabs.add_widget(TabSHA1())
        self.tabs.add_widget(TabRIPEMD())
        self.tabs.add_widget(TabWhirlpool())



class MyApp(MDApp):

    def build(self):
        self.title = "HashFunEdu"
        self.theme_cls.primary_palette = np.random.choice(["Teal", "Amber", "DeepPurple", "Cyan", "Indigo", "Red", "Green"])
        self.theme_cls.theme_style = np.random.choice(["Light", "Dark"])
        Window.set_icon("pound-box.png")
        Window.maximize()
        return MyTabbedPanel()
    
MyApp().run()

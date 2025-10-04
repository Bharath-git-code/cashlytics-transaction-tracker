from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "settings"
        self.db_manager = None
        self.dialog = None
        self.current_setting_type = None
        self.build_ui()

    def build_ui(self):
        """Build the settings screen UI"""
        main_layout = MDBoxLayout(orientation="vertical")

        # Top App Bar
        toolbar = MDTopAppBar(
            title="Cashlytics - Settings",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
        )
        main_layout.add_widget(toolbar)

        # Content
        content_layout = MDBoxLayout(
            orientation="vertical", padding="15dp", spacing="15dp"
        )

        # Settings sections
        settings_scroll = MDScrollView()
        settings_layout = MDBoxLayout(
            orientation="vertical", adaptive_height=True, spacing="15dp"
        )

        # Transaction Types Section
        types_card = self.create_settings_section(
            "Transaction Types",
            "Manage categories for your transactions",
            lambda: self.manage_dropdown_options(
                "transaction_type", "Transaction Types"
            ),
        )
        settings_layout.add_widget(types_card)

        # Payment Modes Section
        payment_card = self.create_settings_section(
            "Payment Modes",
            "Manage payment methods",
            lambda: self.manage_dropdown_options("payment_mode", "Payment Modes"),
        )
        settings_layout.add_widget(payment_card)

        # About Section
        about_card = self.create_settings_section(
            "About", "Transaction Tracker v1.0", self.show_about
        )
        settings_layout.add_widget(about_card)

        settings_scroll.add_widget(settings_layout)
        content_layout.add_widget(settings_scroll)
        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def create_settings_section(self, title, subtitle, callback):
        """Create a settings section card"""
        card = MDCard(
            size_hint_y=None,
            height="80dp",
            padding="15dp",
            elevation=2,
            radius=[8],
            md_bg_color=[1, 1, 1, 1],
        )

        card_layout = MDBoxLayout(orientation="horizontal", spacing="10dp")

        # Text layout
        text_layout = MDBoxLayout(orientation="vertical", spacing="2dp")

        title_label = MDLabel(
            text=title,
            font_style="Subtitle1",
            theme_text_color="Primary",
            size_hint_y=None,
            height="25dp",
        )

        subtitle_label = MDLabel(
            text=subtitle,
            font_style="Caption",
            theme_text_color="Hint",
            size_hint_y=None,
            height="20dp",
            text_size=(None, None),
        )
        # Enable text wrapping for subtitle
        subtitle_label.bind(
            width=lambda *x: setattr(
                subtitle_label, "text_size", (subtitle_label.width, None)
            )
        )

        text_layout.add_widget(title_label)
        text_layout.add_widget(subtitle_label)

        # Arrow button
        arrow_button = MDRaisedButton(
            text=">",
            size_hint_x=None,
            width="40dp",
            height="40dp",
            md_bg_color=[0.2, 0.6, 1, 1],
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
        )
        arrow_button.bind(on_release=lambda x: callback())

        card_layout.add_widget(text_layout)
        card_layout.add_widget(arrow_button)
        card.add_widget(card_layout)

        return card

    def manage_dropdown_options(self, setting_type, title):
        """Show dropdown options management dialog"""
        self.current_setting_type = setting_type

        # Use the shared database manager from the app
        if self.db_manager is None:
            # This shouldn't happen if properly initialized, but fallback
            from database import DatabaseManager

            self.db_manager = DatabaseManager()
            print("WARNING: Settings screen had to create its own database manager!")

        # Get current options
        try:
            options = self.db_manager.get_dropdown_options(setting_type)
        except Exception as e:
            options = []

        # Use basic Kivy Popup instead of MDDialog
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput
        from kivy.uix.scrollview import ScrollView
        from kivy.graphics import Color, Rectangle

        # Main layout with white background
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Add white background
        with main_layout.canvas.before:
            Color(1, 1, 1, 1)  # White background
            main_layout.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(
            size=lambda instance, value: setattr(main_layout.bg_rect, "size", value)
        )
        main_layout.bind(
            pos=lambda instance, value: setattr(main_layout.bg_rect, "pos", value)
        )

        # Title
        title_label = Label(
            text=title, size_hint_y=None, height=40, color=[0, 0, 0, 1], bold=True
        )
        main_layout.add_widget(title_label)

        # Add new option section
        add_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )
        self.new_option_field = TextInput(
            hint_text="Enter new option",
            multiline=False,
            size_hint_x=0.7,
            background_color=[1, 1, 1, 1],
            foreground_color=[0, 0, 0, 1],
        )
        add_btn = Button(
            text="ADD",
            size_hint_x=0.3,
            background_color=[0.2, 0.8, 0.2, 1],
            color=[1, 1, 1, 1],
        )
        add_btn.bind(on_release=self.add_new_option_simple)
        add_layout.add_widget(self.new_option_field)
        add_layout.add_widget(add_btn)
        main_layout.add_widget(add_layout)

        # Options list label
        options_label = Label(
            text="Current Options:",
            size_hint_y=None,
            height=30,
            color=[0, 0, 0, 1],
            bold=True,
        )
        main_layout.add_widget(options_label)

        # Scrollable options list
        scroll = ScrollView()
        self.options_list = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=5
        )
        self.options_list.bind(minimum_height=self.options_list.setter("height"))

        # Add options
        for option in options:
            option_layout = BoxLayout(
                orientation="horizontal", size_hint_y=None, height=50, spacing=10
            )
            option_label = Label(text=option, size_hint_x=0.7, color=[0, 0, 0, 1])
            delete_btn = Button(
                text="DELETE",
                size_hint_x=0.3,
                background_color=[0.8, 0.2, 0.2, 1],
                color=[1, 1, 1, 1],
            )
            delete_btn.bind(
                on_release=lambda x, opt=option: self.delete_option_simple(opt)
            )
            option_layout.add_widget(option_label)
            option_layout.add_widget(delete_btn)
            self.options_list.add_widget(option_layout)

        scroll.add_widget(self.options_list)
        main_layout.add_widget(scroll)

        # Close button
        close_btn = Button(
            text="CLOSE",
            size_hint_y=None,
            height=50,
            background_color=[0.2, 0.6, 1, 1],
            color=[1, 1, 1, 1],
        )
        close_btn.bind(on_release=self.close_popup_simple)
        main_layout.add_widget(close_btn)

        # Create popup with white background
        self.popup = Popup(
            content=main_layout,
            title="",
            size_hint=(0.9, 0.8),
            auto_dismiss=False,
            background_color=[1, 1, 1, 1],
            separator_color=[0.2, 0.2, 0.2, 1],
        )
        self.popup.open()

    def create_option_card(self, option):
        """Create a card for each option with delete button"""
        card = MDCard(
            size_hint_y=None,
            height="60dp",
            padding="10dp",
            elevation=1,
            radius=[5],
            md_bg_color=[0.95, 0.95, 0.95, 1],
        )

        card_layout = MDBoxLayout(orientation="horizontal", spacing="10dp")

        option_label = MDLabel(text=option, theme_text_color="Primary")

        delete_button = MDRaisedButton(
            text="DELETE",
            size_hint_x=None,
            width="80dp",
            height="40dp",
            md_bg_color=[0.8, 0.2, 0.2, 1],
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
        )
        delete_button.bind(on_release=lambda x: self.delete_option(option))

        card_layout.add_widget(option_label)
        card_layout.add_widget(delete_button)
        card.add_widget(card_layout)

        return card

    def add_new_option(self, *args):
        """Add new dropdown option"""
        new_option = self.new_option_field.text.strip()
        if new_option:
            success = self.db_manager.add_dropdown_option(
                self.current_setting_type, new_option
            )
            if success:
                # Refresh the options list
                self.refresh_options_list()
                self.new_option_field.text = ""
            else:
                error_dialog = MDDialog(
                    title="Error",
                    text="This option already exists!",
                    buttons=[
                        MDRaisedButton(
                            text="OK", on_release=lambda x: error_dialog.dismiss()
                        )
                    ],
                )
                error_dialog.open()

    def delete_option(self, option):
        """Delete dropdown option with confirmation"""
        confirm_dialog = MDDialog(
            title="Confirm Delete",
            text=f"Are you sure you want to delete '{option}'?",
            buttons=[
                MDRaisedButton(
                    text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=[0.8, 0.2, 0.2, 1],
                    on_release=lambda x: self.confirm_delete_option(
                        option, confirm_dialog
                    ),
                ),
            ],
        )
        confirm_dialog.open()

    def confirm_delete_option(self, option, dialog):
        """Confirm and delete option"""
        self.db_manager.remove_dropdown_option(self.current_setting_type, option)
        self.refresh_options_list()
        dialog.dismiss()

    def refresh_options_list(self):
        """Refresh the options list in dialog"""
        self.options_list.clear_widgets()
        try:
            options = self.db_manager.get_dropdown_options(self.current_setting_type)

            # Add each option as a simple row
            for option in options:
                option_row = MDBoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height="50dp",
                    spacing="10dp",
                )

                option_label = MDLabel(text=option, size_hint_x=0.7)
                delete_btn = MDRaisedButton(
                    text="DELETE",
                    size_hint_x=0.3,
                    height="40dp",
                    md_bg_color=[0.8, 0.2, 0.2, 1],
                    theme_text_color="Custom",
                    text_color=[1, 1, 1, 1],
                )
                delete_btn.bind(
                    on_release=lambda x, opt=option: self.delete_option(opt)
                )

                option_row.add_widget(option_label)
                option_row.add_widget(delete_btn)
                self.options_list.add_widget(option_row)

        except Exception as e:
            # Add error label if refresh fails
            error_label = MDLabel(
                text=f"Error loading options: {str(e)}", theme_text_color="Error"
            )
            self.options_list.add_widget(error_label)

    def show_about(self):
        """Show about dialog"""
        about_text = """*** TRANSACTION TRACKER v1.0 ***

>> Crafted with passion by Bharathkumar K <<
>> Created on October 2, 2025 <<

*** Your personal finance companion for smart money management! ***

Track your income and expenses across multiple books with style and ease. Every transaction tells a story, and every saving brings you closer to your dreams!

"Small savings today, big dreams tomorrow!"

Built with love using Python, Kivy & KivyMD
(C) 2025 Bharathkumar K - All rights reserved

>>> HAPPY SAVINGS! <<<"""

        about_dialog = MDDialog(
            title="About Transaction Tracker",
            text=about_text,
            buttons=[
                MDRaisedButton(
                    text="AWESOME!",
                    md_bg_color=[0.2, 0.8, 0.2, 1],
                    theme_text_color="Custom",
                    text_color=[1, 1, 1, 1],
                    on_release=lambda x: about_dialog.dismiss(),
                )
            ],
        )
        about_dialog.open()

    def close_dialog(self, *args):
        """Close the dialog"""
        if self.dialog:
            self.dialog.dismiss()

    def close_popup_simple(self, *args):
        """Close the simple popup"""
        if hasattr(self, "popup") and self.popup:
            self.popup.dismiss()

    def add_new_option_simple(self, *args):
        """Add new option using simple popup"""
        new_option = self.new_option_field.text.strip()
        if new_option:
            success = self.db_manager.add_dropdown_option(
                self.current_setting_type, new_option
            )
            if success:
                self.refresh_options_list_simple()
                self.new_option_field.text = ""
            else:
                # Simple error handling
                from kivy.uix.popup import Popup
                from kivy.uix.label import Label
                from kivy.uix.button import Button
                from kivy.uix.boxlayout import BoxLayout

                layout = BoxLayout(orientation="vertical")
                layout.add_widget(Label(text="This option already exists!"))
                btn = Button(text="OK", size_hint_y=None, height=50)
                layout.add_widget(btn)

                error_popup = Popup(title="Error", content=layout, size_hint=(0.6, 0.3))
                btn.bind(on_release=error_popup.dismiss)
                error_popup.open()

    def delete_option_simple(self, option):
        """Delete option using simple popup"""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout

        layout = BoxLayout(orientation="vertical", spacing=10)
        layout.add_widget(Label(text=f"Delete '{option}'?"))

        btn_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        cancel_btn = Button(text="CANCEL")
        delete_btn = Button(text="DELETE", background_color=[0.8, 0.2, 0.2, 1])

        def do_delete(*args):
            self.db_manager.remove_dropdown_option(self.current_setting_type, option)
            self.refresh_options_list_simple()
            confirm_popup.dismiss()

        def do_cancel(*args):
            confirm_popup.dismiss()

        cancel_btn.bind(on_release=do_cancel)
        delete_btn.bind(on_release=do_delete)

        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(delete_btn)
        layout.add_widget(btn_layout)

        confirm_popup = Popup(title="Confirm", content=layout, size_hint=(0.7, 0.4))
        confirm_popup.open()

    def refresh_options_list_simple(self):
        """Refresh options list in simple popup"""
        self.options_list.clear_widgets()
        try:
            options = self.db_manager.get_dropdown_options(self.current_setting_type)

            for option in options:
                from kivy.uix.boxlayout import BoxLayout
                from kivy.uix.label import Label
                from kivy.uix.button import Button

                option_layout = BoxLayout(
                    orientation="horizontal", size_hint_y=None, height=50, spacing=10
                )
                option_label = Label(text=option, size_hint_x=0.7, color=[0, 0, 0, 1])
                delete_btn = Button(
                    text="DELETE",
                    size_hint_x=0.3,
                    background_color=[0.8, 0.2, 0.2, 1],
                    color=[1, 1, 1, 1],
                )
                delete_btn.bind(
                    on_release=lambda x, opt=option: self.delete_option_simple(opt)
                )
                option_layout.add_widget(option_label)
                option_layout.add_widget(delete_btn)
                self.options_list.add_widget(option_layout)
        except Exception as e:
            from kivy.uix.label import Label

            error_label = Label(text=f"Error: {str(e)}", color=[1, 0, 0, 1])
            self.options_list.add_widget(error_label)

    def go_back(self):
        """Go back to previous screen"""
        self.manager.current = "book_list"

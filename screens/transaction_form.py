from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp


def format_indian_commas(number):
    """Add commas according to Indian numbering system"""
    # Convert to string and handle decimals
    if isinstance(number, float):
        if number.is_integer():
            num_str = str(int(number))
        else:
            num_str = f"{number:.2f}"
            integer_part, decimal_part = num_str.split(".")
            formatted_integer = format_indian_commas(int(integer_part))
            return f"{formatted_integer}.{decimal_part}"
    else:
        num_str = str(int(number))

    if len(num_str) <= 3:
        return num_str

    # Indian system: first comma after 3 digits from right, then every 2 digits
    result = num_str[-3:]  # Last 3 digits
    remaining = num_str[:-3]

    while remaining:
        if len(remaining) <= 2:
            result = remaining + "," + result
            break
        else:
            result = remaining[-2:] + "," + result
            remaining = remaining[:-2]

    return result


def remove_commas(text):
    """Remove commas from text to get numeric value"""
    return text.replace(",", "")


class TransactionFormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "transaction_form"
        self.current_book_id = None
        self.is_cash_in = True
        self.db_manager = None
        self.type_menu = None
        self.payment_menu = None
        self.build_ui()

    def build_ui(self):
        """Build the transaction form screen UI"""
        main_layout = MDBoxLayout(orientation="vertical")

        # Top App Bar
        self.toolbar = MDTopAppBar(
            title="Cashlytics - Add Transaction",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
        )
        main_layout.add_widget(self.toolbar)

        # Background with form content overlay
        from kivy.uix.floatlayout import FloatLayout

        background_layout = FloatLayout()

        # Background decorative elements - subtle and behind content
        self.bg_circle1 = MDCard(
            size_hint=(None, None),
            size=("150dp", "150dp"),
            pos_hint={"center_x": 0.85, "center_y": 0.8},
            elevation=0,
            radius=[75],
            md_bg_color=[0.1, 0.5, 0.9, 0.05],  # Very transparent blue
        )

        self.bg_circle2 = MDCard(
            size_hint=(None, None),
            size=("100dp", "100dp"),
            pos_hint={"center_x": 0.2, "center_y": 0.3},
            elevation=0,
            radius=[50],
            md_bg_color=[0.1, 0.5, 0.9, 0.08],  # Slightly more visible
        )

        # Large background symbol
        self.bg_symbol = MDLabel(
            text="₹",
            font_style="H1",
            theme_text_color="Custom",
            text_color=[0.1, 0.5, 0.9, 0.06],  # Very light blue
            pos_hint={"center_x": 0.85, "center_y": 0.8},
            size_hint=(None, None),
            size=("150dp", "150dp"),
            halign="center",
            valign="middle",
        )

        background_layout.add_widget(self.bg_circle1)
        background_layout.add_widget(self.bg_circle2)
        background_layout.add_widget(self.bg_symbol)

        # Form content - now in a scrollable container
        from kivy.uix.scrollview import ScrollView

        content_scroll = ScrollView()

        content_layout = MDBoxLayout(
            orientation="vertical", padding="15dp", spacing="12dp", adaptive_height=True
        )

        # Transaction type indicator
        self.type_card = MDCard(
            size_hint_y=None,
            height="60dp",
            padding="15dp",
            elevation=3,
            radius=[10],
            md_bg_color=[0.2, 0.7, 0.2, 1],  # Green for cash in
        )

        self.type_label = MDLabel(
            text="CASH IN",
            font_style="H6",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            halign="center",
        )
        self.type_card.add_widget(self.type_label)
        content_layout.add_widget(self.type_card)

        # Amount field
        self.amount_field = MDTextField(
            hint_text="Enter amount (₹)",
            helper_text="Amount in Rupees",
            helper_text_mode="on_focus",
            input_filter=None,  # We'll handle input validation manually
            size_hint_y=None,
            height="56dp",
        )
        self.amount_field.bind(text=self.on_amount_text_change)
        content_layout.add_widget(self.amount_field)

        # Description field
        self.description_field = MDTextField(
            hint_text="Description",
            helper_text="What is this transaction for?",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height="56dp",
        )
        content_layout.add_widget(self.description_field)

        # Transaction type dropdown
        type_layout = MDBoxLayout(
            orientation="vertical", spacing="5dp", size_hint_y=None, height="65dp"
        )

        type_label = MDLabel(
            text="Transaction Type:",
            font_style="Caption",
            theme_text_color="Primary",
            size_hint_y=None,
            height="20dp",
        )

        self.type_button = MDRaisedButton(
            text="Select Type",
            size_hint_y=None,
            height="40dp",
            md_bg_color=[0.9, 0.9, 0.9, 1],
            theme_text_color="Primary",
        )
        self.type_button.bind(on_release=self.show_type_menu)

        type_layout.add_widget(type_label)
        type_layout.add_widget(self.type_button)
        content_layout.add_widget(type_layout)

        # Payment mode dropdown
        payment_layout = MDBoxLayout(
            orientation="vertical", spacing="5dp", size_hint_y=None, height="65dp"
        )

        payment_label = MDLabel(
            text="Payment Mode:",
            font_style="Caption",
            theme_text_color="Primary",
            size_hint_y=None,
            height="20dp",
        )

        self.payment_button = MDRaisedButton(
            text="Select Payment Mode",
            size_hint_y=None,
            height="40dp",
            md_bg_color=[0.9, 0.9, 0.9, 1],
            theme_text_color="Primary",
        )
        self.payment_button.bind(on_release=self.show_payment_menu)

        payment_layout.add_widget(payment_label)
        payment_layout.add_widget(self.payment_button)
        content_layout.add_widget(payment_layout)

        # Save button
        save_button = MDRaisedButton(
            text="SAVE TRANSACTION",
            size_hint_y=None,
            height="50dp",
            md_bg_color=[0.2, 0.6, 1, 1],
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size="16sp",
        )
        save_button.bind(on_release=self.save_transaction)
        content_layout.add_widget(save_button)

        content_scroll.add_widget(content_layout)
        background_layout.add_widget(content_scroll)
        main_layout.add_widget(background_layout)
        self.add_widget(main_layout)

    def on_amount_text_change(self, instance, value):
        """Format amount field with Indian commas as user types"""
        # Remove commas and non-numeric characters except decimal point
        clean_text = "".join(c for c in value if c.isdigit() or c == ".")

        if not clean_text:
            return

        try:
            # Handle decimal places
            if "." in clean_text:
                integer_part, decimal_part = clean_text.split(".", 1)
                # Limit decimal places to 2
                if len(decimal_part) > 2:
                    decimal_part = decimal_part[:2]

                if integer_part:
                    formatted_integer = format_indian_commas(int(integer_part))
                    formatted_text = f"{formatted_integer}.{decimal_part}"
                else:
                    formatted_text = f"0.{decimal_part}"
            else:
                if clean_text:
                    formatted_text = format_indian_commas(int(clean_text))
                else:
                    formatted_text = ""

            # Update text only if it's different to avoid infinite loop
            if instance.text != formatted_text:
                # Store cursor position
                cursor_pos = instance.cursor_col
                instance.text = formatted_text
                # Restore cursor position (approximately)
                instance.cursor = (min(cursor_pos, len(formatted_text)), 0)

        except (ValueError, TypeError):
            # If parsing fails, keep the current text
            pass

    def set_transaction_data(self, book_id, is_cash_in):
        """Set the transaction data"""
        self.current_book_id = book_id
        self.is_cash_in = is_cash_in

        # Import database manager here to avoid circular imports
        if self.db_manager is None:
            from database import DatabaseManager

            self.db_manager = DatabaseManager()

        # Update UI based on transaction type
        if is_cash_in:
            self.toolbar.title = "Cash In"
            self.type_label.text = "CASH IN"
            self.type_card.md_bg_color = [0.2, 0.7, 0.2, 1]  # Green
            self.bg_symbol.text = "+"
            self.bg_symbol.text_color = [0.2, 0.7, 0.2, 0.06]  # Green tint
            self.bg_circle1.md_bg_color = [0.2, 0.7, 0.2, 0.05]
            self.bg_circle2.md_bg_color = [0.2, 0.7, 0.2, 0.08]
        else:
            self.toolbar.title = "Cash Out"
            self.type_label.text = "CASH OUT"
            self.type_card.md_bg_color = [0.8, 0.2, 0.2, 1]  # Red
            self.bg_symbol.text = "-"
            self.bg_symbol.text_color = [0.8, 0.2, 0.2, 0.06]  # Red tint
            self.bg_circle1.md_bg_color = [0.8, 0.2, 0.2, 0.05]
            self.bg_circle2.md_bg_color = [0.8, 0.2, 0.2, 0.08]

        # Clear form
        self.clear_form()

        # Load dropdown options
        self.load_dropdown_options()

    def clear_form(self):
        """Clear all form fields"""
        self.amount_field.text = ""
        self.description_field.text = ""
        self.type_button.text = "Select Type"
        self.payment_button.text = "Select Payment Mode"

    def load_dropdown_options(self):
        """Load dropdown options from database"""
        self.transaction_types = self.db_manager.get_dropdown_options(
            "transaction_type"
        )
        self.payment_modes = self.db_manager.get_dropdown_options("payment_mode")

    def show_type_menu(self, button):
        """Show transaction type dropdown menu"""
        menu_items = []
        for type_option in self.transaction_types:
            menu_items.append(
                {
                    "text": type_option,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=type_option: self.select_type(x),
                }
            )

        self.type_menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=4,
        )
        self.type_menu.open()

    def select_type(self, type_text):
        """Select transaction type"""
        self.type_button.text = type_text
        self.type_menu.dismiss()

    def show_payment_menu(self, button):
        """Show payment mode dropdown menu"""
        menu_items = []
        for payment_option in self.payment_modes:
            menu_items.append(
                {
                    "text": payment_option,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=payment_option: self.select_payment(x),
                }
            )

        self.payment_menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=4,
        )
        self.payment_menu.open()

    def select_payment(self, payment_text):
        """Select payment mode"""
        self.payment_button.text = payment_text
        self.payment_menu.dismiss()

    def save_transaction(self, *args):
        """Save the transaction"""
        # Validate form
        if not self.validate_form():
            return

        # Get form data
        amount = float(remove_commas(self.amount_field.text))
        description = self.description_field.text.strip()
        trans_type = self.type_button.text
        payment_mode = self.payment_button.text

        # Save to database
        self.db_manager.add_transaction(
            self.current_book_id,
            amount,
            description,
            trans_type,
            payment_mode,
            self.is_cash_in,
        )

        # Show success dialog
        success_dialog = MDDialog(
            title="Success!",
            text="Transaction saved successfully.",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.on_transaction_saved(success_dialog),
                )
            ],
        )
        success_dialog.open()

    def validate_form(self):
        """Validate form data"""
        errors = []

        # Validate amount
        try:
            amount = float(remove_commas(self.amount_field.text))
            if amount <= 0:
                errors.append("Amount must be greater than 0")
        except (ValueError, TypeError):
            errors.append("Please enter a valid amount")

        # Validate description
        if not self.description_field.text.strip():
            errors.append("Please enter a description")

        # Validate type selection
        if self.type_button.text == "Select Type":
            errors.append("Please select a transaction type")

        # Validate payment mode selection
        if self.payment_button.text == "Select Payment Mode":
            errors.append("Please select a payment mode")

        # Show errors if any
        if errors:
            error_text = "\n".join(errors)
            error_dialog = MDDialog(
                title="Validation Error",
                text=error_text,
                buttons=[
                    MDRaisedButton(
                        text="OK", on_release=lambda x: error_dialog.dismiss()
                    )
                ],
            )
            error_dialog.open()
            return False

        return True

    def on_transaction_saved(self, dialog):
        """Handle transaction saved"""
        dialog.dismiss()
        self.go_back()

    def go_back(self):
        """Go back to transaction list"""
        self.manager.current = "transaction_list"

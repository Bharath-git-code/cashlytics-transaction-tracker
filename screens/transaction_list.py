from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from datetime import datetime


def format_indian_currency(amount, short_format=False):
    """Format number according to Indian numbering system with commas"""
    if amount == 0:
        return "₹0"

    abs_amount = abs(amount)
    sign = "" if amount >= 0 else "-"

    if short_format:
        # Short format for display in cards
        if abs_amount >= 10000000:  # 1 crore
            return f"{sign}₹{amount/10000000:.1f}Cr"
        elif abs_amount >= 100000:  # 1 lakh
            return f"{sign}₹{amount/100000:.1f}L"
        else:
            # For small amounts, still add commas
            formatted = format_indian_commas(abs_amount)
            return f"{sign}₹{formatted}"
    else:
        # Full format with Indian comma system
        formatted = format_indian_commas(abs_amount)
        return f"{sign}₹{formatted}"


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


class TransactionListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "transaction_list"
        self.current_book_id = None
        self.current_book_name = ""
        self.db_manager = None

        # Filter variables
        self.filter_from_date = None
        self.filter_to_date = None
        self.filter_payment_type = "All"
        self.filter_expense_type = "All"
        self.filter_active = False

        self.build_ui()

    def build_ui(self):
        """Build the transaction list screen UI"""
        main_layout = MDBoxLayout(orientation="vertical")

        # Top App Bar with filter button
        self.toolbar = MDTopAppBar(
            title="Cashlytics",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["filter", lambda x: self.show_filter_dialog()]],
        )
        main_layout.add_widget(self.toolbar)

        # Centered Logo and Title Header (no background)
        header_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height="80dp",
            padding="10dp",
            spacing="8dp",
        )

        # Logo centered
        logo_layout = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height="40dp"
        )

        # Spacers to center the logo
        logo_layout.add_widget(MDLabel())  # Left spacer

        try:
            from kivy.uix.image import Image

            logo_img = Image(
                source="assets/icons/logo.png",
                size_hint=(None, None),
                size=("40dp", "40dp"),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
            logo_layout.add_widget(logo_img)
        except:
            # Fallback to icon if image not available
            logo_icon = MDIconButton(
                icon="currency-usd",
                size_hint=(None, None),
                size=("40dp", "40dp"),
                theme_icon_color="Custom",
                icon_color=[0.2, 0.6, 1, 1],
                disabled=True,
            )
            logo_layout.add_widget(logo_icon)

        logo_layout.add_widget(MDLabel())  # Right spacer
        header_layout.add_widget(logo_layout)

        # Title centered below logo
        title_label = MDLabel(
            text="Cashlytics",
            font_style="H6",
            theme_text_color="Primary",
            halign="center",
            valign="center",
            bold=True,
            size_hint_y=None,
            height="30dp",
        )
        header_layout.add_widget(title_label)

        # Content layout
        content_layout = MDBoxLayout(
            orientation="vertical", padding="10dp", spacing="15dp"
        )

        # Add header layout directly to content
        content_layout.add_widget(header_layout)

        # Balance display
        self.balance_card = MDCard(
            size_hint_y=None,
            height="80dp",
            padding="15dp",
            elevation=5,
            radius=[15],
            md_bg_color=[0.9, 0.95, 1, 1],
        )

        balance_layout = MDBoxLayout(orientation="vertical", spacing="5dp")

        balance_title = MDLabel(
            text="Current Balance",
            font_style="Subtitle2",
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height="25dp",
        )

        self.balance_label = MDLabel(
            text="₹0.00",
            font_style="H5",
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height="35dp",
            text_size=(None, None),
        )

        balance_layout.add_widget(balance_title)
        balance_layout.add_widget(self.balance_label)
        self.balance_card.add_widget(balance_layout)
        content_layout.add_widget(self.balance_card)

        # Cash In/Out buttons
        button_layout = MDBoxLayout(
            orientation="horizontal", spacing="12dp", size_hint_y=None, height="48dp"
        )

        cash_in_btn = MDRaisedButton(
            text="CASH IN",
            md_bg_color=[0.2, 0.7, 0.2, 1],
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_x=0.5,
            height="48dp",
            font_size="14sp",
        )
        cash_in_btn.bind(on_release=lambda x: self.open_transaction_form(True))

        cash_out_btn = MDRaisedButton(
            text="CASH OUT",
            md_bg_color=[0.8, 0.2, 0.2, 1],
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_x=0.5,
            height="48dp",
            font_size="14sp",
        )
        cash_out_btn.bind(on_release=lambda x: self.open_transaction_form(False))

        button_layout.add_widget(cash_in_btn)
        button_layout.add_widget(cash_out_btn)
        content_layout.add_widget(button_layout)

        # Transactions list
        transactions_title = MDLabel(
            text="Transaction History",
            font_style="Subtitle1",
            theme_text_color="Primary",
            size_hint_y=None,
            height="35dp",
        )
        content_layout.add_widget(transactions_title)

        # Filter status indicator
        self.filter_status_label = MDLabel(
            text="",
            font_style="Caption",
            theme_text_color="Primary",
            size_hint_y=None,
            height="0dp",  # Initially hidden
            halign="center",
        )
        content_layout.add_widget(self.filter_status_label)

        self.transactions_scroll = MDScrollView()
        self.transactions_layout = MDBoxLayout(
            orientation="vertical", adaptive_height=True, spacing="8dp"
        )
        self.transactions_scroll.add_widget(self.transactions_layout)
        content_layout.add_widget(self.transactions_scroll)

        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def set_current_book(self, book_id, book_name):
        """Set the current book and refresh data"""
        self.current_book_id = book_id
        self.current_book_name = book_name
        self.toolbar.title = book_name

        # Import database manager here to avoid circular imports
        if self.db_manager is None:
            from database import DatabaseManager

            self.db_manager = DatabaseManager()

        self.refresh_data()

    def refresh_data(self):
        """Refresh balance and transactions"""
        if self.current_book_id is None:
            return

        # Update balance with proper formatting for large numbers
        balance = self.db_manager.get_balance(self.current_book_id)
        balance_color = [0, 0.6, 0, 1] if balance >= 0 else [0.8, 0, 0, 1]

        # Format balance for display with Indian comma system
        display_balance = format_indian_currency(balance, short_format=True)

        self.balance_label.text = display_balance
        self.balance_label.text_color = balance_color  # Update transactions list
        self.refresh_transactions()

    def refresh_transactions(self):
        """Refresh the transactions list with applied filters"""
        self.transactions_layout.clear_widgets()

        transactions = self.db_manager.get_transactions(self.current_book_id)

        # Apply filters if active
        if self.filter_active and transactions:
            transactions = self.apply_filters(transactions)

        # Update filter status
        self.update_filter_status(len(transactions) if transactions else 0)

        if not transactions:
            no_transactions_label = MDLabel(
                text=(
                    "No transactions match the current filters!"
                    if self.filter_active
                    else "No transactions yet. Add your first transaction!"
                ),
                theme_text_color="Hint",
                halign="center",
            )
            self.transactions_layout.add_widget(no_transactions_label)
        else:
            for transaction in transactions:
                card = self.create_transaction_card(transaction)
                self.transactions_layout.add_widget(card)

    def create_transaction_card(self, transaction):
        """Create a card for each transaction"""
        trans_id, amount, description, trans_type, payment_mode, trans_date = (
            transaction
        )

        card = MDCard(
            size_hint_y=None,
            height="85dp",
            padding="10dp",
            elevation=2,
            radius=[8],
            md_bg_color=[1, 1, 1, 1],
        )

        card_layout = MDBoxLayout(orientation="horizontal", spacing="8dp")

        # Left side - Transaction info
        info_layout = MDBoxLayout(orientation="vertical", spacing="2dp")

        # Amount and description row
        amount_desc_layout = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height="25dp"
        )

        amount_color = [0, 0.6, 0, 1] if amount > 0 else [0.8, 0, 0, 1]
        amount_symbol = "+" if amount > 0 else ""

        # Format amount with Indian currency formatting
        display_amount = format_indian_currency(abs(amount), short_format=True)
        # Remove the ₹ symbol since we'll add it with the + sign
        display_amount = display_amount[1:]  # Remove ₹

        amount_label = MDLabel(
            text=f"{amount_symbol}₹{display_amount}",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=amount_color,
            size_hint_x=None,
            width="100dp",
            halign="left",
            valign="middle",
            text_size=("100dp", None),
        )

        description_label = MDLabel(
            text=description[:25] + "..." if len(description) > 25 else description,
            font_style="Body2",
            theme_text_color="Primary",
            halign="left",
            valign="middle",
            text_size=(None, None),
        )

        amount_desc_layout.add_widget(amount_label)
        amount_desc_layout.add_widget(description_label)

        # Details row: Type and Payment mode
        details_label = MDLabel(
            text=f"{trans_type} • {payment_mode}",
            font_style="Caption",
            theme_text_color="Hint",
            size_hint_y=None,
            height="16dp",
            halign="left",
        )

        # Date row
        date_label = MDLabel(
            text=trans_date[:16].replace("T", " "),
            font_style="Caption",
            theme_text_color="Hint",
            size_hint_y=None,
            height="16dp",
            halign="left",
        )

        info_layout.add_widget(amount_desc_layout)
        info_layout.add_widget(details_label)
        info_layout.add_widget(date_label)

        # Right side - Edit button and type indicator
        right_layout = MDBoxLayout(
            orientation="vertical", size_hint_x=None, width="60dp", spacing="5dp"
        )

        edit_btn = MDIconButton(
            icon="pencil",
            size_hint_x=None,
            width="30dp",
            theme_icon_color="Custom",
            icon_color=[0.2, 0.6, 1, 1],
            on_release=lambda x: self.edit_transaction(trans_id),
        )

        type_indicator = MDLabel(
            text="IN" if amount > 0 else "OUT",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=amount_color,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height="20dp",
        )

        right_layout.add_widget(edit_btn)
        right_layout.add_widget(type_indicator)

        card_layout.add_widget(info_layout)
        card_layout.add_widget(right_layout)
        card.add_widget(card_layout)

        return card

    def open_transaction_form(self, is_cash_in):
        """Open transaction form screen"""
        form_screen = self.manager.get_screen("transaction_form")
        form_screen.set_transaction_data(self.current_book_id, is_cash_in)
        self.manager.current = "transaction_form"

    def go_back(self):
        """Go back to book list"""
        self.manager.current = "book_list"

    def edit_transaction(self, trans_id):
        """Edit an existing transaction"""
        # Get transaction details
        transaction = self.db_manager.get_transaction_by_id(trans_id)
        if not transaction:
            return

        trans_id, amount, description, trans_type, payment_mode, trans_date = (
            transaction
        )
        is_cash_in = amount > 0
        amount = abs(amount)

        # Show edit dialog
        self.show_edit_dialog(
            trans_id,
            amount,
            description,
            trans_type,
            payment_mode,
            is_cash_in,
            trans_date,
        )

    def show_edit_dialog(
        self,
        trans_id,
        amount,
        description,
        trans_type,
        payment_mode,
        is_cash_in,
        trans_date,
    ):
        """Show transaction edit dialog"""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput
        from kivy.uix.spinner import Spinner
        from datetime import datetime

        # Parse current date
        try:
            current_date = datetime.fromisoformat(trans_date.replace("Z", "+00:00"))
        except:
            current_date = datetime.now()

        # Main layout with white background
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
        with main_layout.canvas.before:
            from kivy.graphics import Color, Rectangle

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
            text="Edit Transaction",
            size_hint_y=None,
            height=40,
            color=[0, 0, 0, 1],
            bold=True,
        )
        main_layout.add_widget(title_label)

        # Amount input with comma formatting
        amount_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )
        amount_layout.add_widget(
            Label(text="Amount:", size_hint_x=0.3, color=[0, 0, 0, 1])
        )

        # Format amount with commas for display
        formatted_amount = format_indian_commas(amount)
        self.edit_amount_field = TextInput(
            text=formatted_amount,
            multiline=False,
            size_hint_x=0.7,
            background_color=[1, 1, 1, 1],
            foreground_color=[0, 0, 0, 1],
        )
        self.edit_amount_field.bind(text=self.on_edit_amount_change)
        amount_layout.add_widget(self.edit_amount_field)
        main_layout.add_widget(amount_layout)

        # Description input
        desc_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )
        desc_layout.add_widget(
            Label(text="Description:", size_hint_x=0.3, color=[0, 0, 0, 1])
        )
        self.edit_desc_field = TextInput(
            text=description,
            multiline=False,
            size_hint_x=0.7,
            background_color=[1, 1, 1, 1],
            foreground_color=[0, 0, 0, 1],
        )
        desc_layout.add_widget(self.edit_desc_field)
        main_layout.add_widget(desc_layout)

        # Transaction type spinner
        type_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )
        type_layout.add_widget(Label(text="Type:", size_hint_x=0.3, color=[0, 0, 0, 1]))
        transaction_types = self.db_manager.get_dropdown_options("transaction_type")
        self.edit_type_spinner = Spinner(
            text=trans_type,
            values=transaction_types,
            size_hint_x=0.7,
            background_color=[1, 1, 1, 1],
        )
        type_layout.add_widget(self.edit_type_spinner)
        main_layout.add_widget(type_layout)

        # Payment mode spinner
        payment_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )
        payment_layout.add_widget(
            Label(text="Payment:", size_hint_x=0.3, color=[0, 0, 0, 1])
        )
        payment_modes = self.db_manager.get_dropdown_options("payment_mode")
        self.edit_payment_spinner = Spinner(
            text=payment_mode,
            values=payment_modes,
            size_hint_x=0.7,
            background_color=[1, 1, 1, 1],
        )
        payment_layout.add_widget(self.edit_payment_spinner)
        main_layout.add_widget(payment_layout)

        # Cash In/Out toggle
        cash_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )
        cash_layout.add_widget(Label(text="Type:", size_hint_x=0.3, color=[0, 0, 0, 1]))
        self.edit_cash_in_btn = Button(
            text="CASH IN" if is_cash_in else "CASH OUT",
            size_hint_x=0.7,
            background_color=[0.2, 0.8, 0.2, 1] if is_cash_in else [0.8, 0.2, 0.2, 1],
            color=[1, 1, 1, 1],
        )
        self.edit_is_cash_in = is_cash_in
        self.edit_cash_in_btn.bind(on_release=self.toggle_edit_cash_type)
        cash_layout.add_widget(self.edit_cash_in_btn)
        main_layout.add_widget(cash_layout)

        # Date selection
        date_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )
        date_layout.add_widget(Label(text="Date:", size_hint_x=0.3, color=[0, 0, 0, 1]))
        self.edit_selected_date = current_date
        self.edit_date_btn = Button(
            text=current_date.strftime("%Y-%m-%d"),
            size_hint_x=0.7,
            background_color=[0.2, 0.6, 1, 1],
            color=[1, 1, 1, 1],
        )
        self.edit_date_btn.bind(on_release=self.show_edit_date_picker)
        date_layout.add_widget(self.edit_date_btn)
        main_layout.add_widget(date_layout)

        # Buttons
        button_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )
        cancel_btn = Button(
            text="CANCEL", background_color=[0.7, 0.7, 0.7, 1], color=[1, 1, 1, 1]
        )
        save_btn = Button(
            text="SAVE", background_color=[0.2, 0.8, 0.2, 1], color=[1, 1, 1, 1]
        )
        delete_btn = Button(
            text="DELETE", background_color=[0.8, 0.2, 0.2, 1], color=[1, 1, 1, 1]
        )

        def save_changes(*args):
            try:
                new_amount = float(remove_commas(self.edit_amount_field.text.strip()))
                new_desc = self.edit_desc_field.text.strip()
                new_type = self.edit_type_spinner.text
                new_payment = self.edit_payment_spinner.text

                if new_amount <= 0 or not new_desc:
                    return

                success = self.db_manager.update_transaction(
                    trans_id,
                    new_amount,
                    new_desc,
                    new_type,
                    new_payment,
                    self.edit_is_cash_in,
                    self.edit_selected_date.isoformat(),
                )

                if success:
                    self.refresh_transactions()
                    edit_popup.dismiss()
            except ValueError:
                pass

        def delete_transaction(*args):
            # Add delete confirmation
            confirm_layout = BoxLayout(orientation="vertical", spacing=10)
            confirm_layout.add_widget(
                Label(text="Delete this transaction?", color=[0, 0, 0, 1])
            )
            confirm_buttons = BoxLayout(
                orientation="horizontal", size_hint_y=None, height=50
            )

            def do_delete(*args):
                conn = self.db_manager.db_name
                import sqlite3

                conn = sqlite3.connect(conn)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
                conn.commit()
                conn.close()
                self.refresh_transactions()
                confirm_popup.dismiss()
                edit_popup.dismiss()

            confirm_cancel = Button(text="CANCEL")
            confirm_delete = Button(text="DELETE", background_color=[0.8, 0.2, 0.2, 1])
            confirm_cancel.bind(on_release=lambda x: confirm_popup.dismiss())
            confirm_delete.bind(on_release=do_delete)

            confirm_buttons.add_widget(confirm_cancel)
            confirm_buttons.add_widget(confirm_delete)
            confirm_layout.add_widget(confirm_buttons)

            confirm_popup = Popup(
                title="Confirm Delete", content=confirm_layout, size_hint=(0.7, 0.4)
            )
            confirm_popup.open()

        cancel_btn.bind(on_release=lambda x: edit_popup.dismiss())
        save_btn.bind(on_release=save_changes)
        delete_btn.bind(on_release=delete_transaction)

        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(save_btn)
        button_layout.add_widget(delete_btn)
        main_layout.add_widget(button_layout)

        # Create popup
        edit_popup = Popup(
            content=main_layout, title="", size_hint=(0.95, 0.9), auto_dismiss=False
        )
        edit_popup.open()

    def toggle_edit_cash_type(self, *args):
        """Toggle between cash in and cash out for edit"""
        self.edit_is_cash_in = not self.edit_is_cash_in
        self.edit_cash_in_btn.text = "CASH IN" if self.edit_is_cash_in else "CASH OUT"
        self.edit_cash_in_btn.background_color = (
            [0.2, 0.8, 0.2, 1] if self.edit_is_cash_in else [0.8, 0.2, 0.2, 1]
        )

    def on_edit_amount_change(self, instance, value):
        """Format amount field with Indian commas as user types in edit dialog"""
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

    def show_edit_date_picker(self, *args):
        """Show date picker for editing transaction date"""
        # Simple date picker using spinners
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.spinner import Spinner

        # Main layout with white background and reduced spacing
        date_layout = BoxLayout(orientation="vertical", spacing=5, padding=15)
        with date_layout.canvas.before:
            from kivy.graphics import Color, Rectangle

            Color(1, 1, 1, 1)  # White background
            date_layout.bg_rect = Rectangle(size=date_layout.size, pos=date_layout.pos)
        date_layout.bind(
            size=lambda instance, value: setattr(date_layout.bg_rect, "size", value)
        )
        date_layout.bind(
            pos=lambda instance, value: setattr(date_layout.bg_rect, "pos", value)
        )

        # Title
        date_layout.add_widget(
            Label(
                text="Select Date",
                size_hint_y=None,
                height=30,
                color=[0, 0, 0, 1],
                bold=True,
                font_size="16sp",
            )
        )

        # Headers for the date components
        headers_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=25, spacing=5
        )
        headers_layout.add_widget(
            Label(
                text="Year",
                size_hint_x=0.33,
                color=[0.3, 0.3, 0.3, 1],
                font_size="12sp",
                bold=True,
            )
        )
        headers_layout.add_widget(
            Label(
                text="Month",
                size_hint_x=0.33,
                color=[0.3, 0.3, 0.3, 1],
                font_size="12sp",
                bold=True,
            )
        )
        headers_layout.add_widget(
            Label(
                text="Day",
                size_hint_x=0.33,
                color=[0.3, 0.3, 0.3, 1],
                font_size="12sp",
                bold=True,
            )
        )
        date_layout.add_widget(headers_layout)

        # Date selectors with compact height
        selectors_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40, spacing=5
        )

        # Year spinner
        current_year = self.edit_selected_date.year
        years = [str(y) for y in range(2020, 2031)]
        year_spinner = Spinner(
            text=str(current_year),
            values=years,
            size_hint_x=0.33,
            background_color=[1, 1, 1, 1],
            color=[0, 0, 0, 1],
        )

        # Month spinner
        current_month = self.edit_selected_date.month
        months = [f"{i:02d}" for i in range(1, 13)]
        month_spinner = Spinner(
            text=f"{current_month:02d}",
            values=months,
            size_hint_x=0.33,
            background_color=[1, 1, 1, 1],
            color=[0, 0, 0, 1],
        )

        # Day spinner
        current_day = self.edit_selected_date.day
        days = [f"{i:02d}" for i in range(1, 32)]
        day_spinner = Spinner(
            text=f"{current_day:02d}",
            values=days,
            size_hint_x=0.33,
            background_color=[1, 1, 1, 1],
            color=[0, 0, 0, 1],
        )

        selectors_layout.add_widget(year_spinner)
        selectors_layout.add_widget(month_spinner)
        selectors_layout.add_widget(day_spinner)
        date_layout.add_widget(selectors_layout)

        # Buttons with reduced height
        button_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40, spacing=10
        )
        cancel_btn = Button(
            text="CANCEL", background_color=[0.7, 0.7, 0.7, 1], color=[1, 1, 1, 1]
        )
        ok_btn = Button(
            text="OK", background_color=[0.2, 0.6, 1, 1], color=[1, 1, 1, 1]
        )

        def save_date(*args):
            try:
                from datetime import datetime

                year = int(year_spinner.text)
                month = int(month_spinner.text)
                day = int(day_spinner.text)
                self.edit_selected_date = datetime(year, month, day)
                self.edit_date_btn.text = self.edit_selected_date.strftime("%Y-%m-%d")
                date_popup.dismiss()
            except ValueError:
                pass

        cancel_btn.bind(on_release=lambda x: date_popup.dismiss())
        ok_btn.bind(on_release=save_date)

        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(ok_btn)
        date_layout.add_widget(button_layout)

        date_popup = Popup(
            title="", content=date_layout, size_hint=(0.7, 0.4), auto_dismiss=False
        )
        date_popup.open()

    def on_edit_date_save(self, instance, value, date_range):
        """Handle date selection for edit"""
        self.edit_selected_date = value
        self.edit_date_btn.text = value.strftime("%Y-%m-%d")

    def apply_filters(self, transactions):
        """Apply active filters to transactions list"""
        filtered = []

        for transaction in transactions:
            trans_id, amount, description, trans_type, payment_mode, trans_date = (
                transaction
            )

            # Parse transaction date
            try:
                trans_datetime = datetime.fromisoformat(
                    trans_date.replace("Z", "+00:00")
                )
                trans_date_only = trans_datetime.date()
            except:
                continue

            # Check date range filter
            if self.filter_from_date and trans_date_only < self.filter_from_date:
                continue
            if self.filter_to_date and trans_date_only > self.filter_to_date:
                continue

            # Check payment type filter
            if (
                self.filter_payment_type != "All"
                and payment_mode != self.filter_payment_type
            ):
                continue

            # Check expense type filter
            if (
                self.filter_expense_type != "All"
                and trans_type != self.filter_expense_type
            ):
                continue

            filtered.append(transaction)

        return filtered

    def update_filter_status(self, count):
        """Update filter status indicator"""
        if not self.filter_active:
            self.filter_status_label.text = ""
            self.filter_status_label.height = "0dp"
            return

        # Build filter description
        filters = []
        if self.filter_from_date or self.filter_to_date:
            if self.filter_from_date and self.filter_to_date:
                filters.append(
                    f"Date: {self.filter_from_date} to {self.filter_to_date}"
                )
            elif self.filter_from_date:
                filters.append(f"From: {self.filter_from_date}")
            elif self.filter_to_date:
                filters.append(f"Until: {self.filter_to_date}")

        if self.filter_payment_type != "All":
            filters.append(f"Payment: {self.filter_payment_type}")

        if self.filter_expense_type != "All":
            filters.append(f"Type: {self.filter_expense_type}")

        filter_text = " • ".join(filters)
        self.filter_status_label.text = f"Filters: {filter_text} ({count} transactions)"
        self.filter_status_label.height = "25dp"

    def show_filter_dialog(self):
        """Show comprehensive filter dialog"""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.spinner import Spinner

        # Main layout with white background
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
        with main_layout.canvas.before:
            from kivy.graphics import Color, Rectangle

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
            text="Filter Transactions",
            size_hint_y=None,
            height=30,
            color=[0, 0, 0, 1],
            bold=True,
        )
        main_layout.add_widget(title_label)

        # Date range section
        date_header = Label(
            text="Date Range",
            size_hint_y=None,
            height=25,
            color=[0.3, 0.3, 0.3, 1],
            bold=True,
        )
        main_layout.add_widget(date_header)

        # From date
        from_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40, spacing=10
        )
        from_layout.add_widget(Label(text="From:", size_hint_x=0.3, color=[0, 0, 0, 1]))
        self.filter_from_btn = Button(
            text=(
                self.filter_from_date.strftime("%Y-%m-%d")
                if self.filter_from_date
                else "Select Date"
            ),
            size_hint_x=0.7,
            background_color=[0.9, 0.9, 0.9, 1],
            color=[0, 0, 0, 1],
        )
        self.filter_from_btn.bind(on_release=lambda x: self.show_date_picker("from"))
        from_layout.add_widget(self.filter_from_btn)
        main_layout.add_widget(from_layout)

        # To date
        to_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40, spacing=10
        )
        to_layout.add_widget(Label(text="To:", size_hint_x=0.3, color=[0, 0, 0, 1]))
        self.filter_to_btn = Button(
            text=(
                self.filter_to_date.strftime("%Y-%m-%d")
                if self.filter_to_date
                else "Select Date"
            ),
            size_hint_x=0.7,
            background_color=[0.9, 0.9, 0.9, 1],
            color=[0, 0, 0, 1],
        )
        self.filter_to_btn.bind(on_release=lambda x: self.show_date_picker("to"))
        to_layout.add_widget(self.filter_to_btn)
        main_layout.add_widget(to_layout)

        # Payment type section
        payment_header = Label(
            text="Payment Mode",
            size_hint_y=None,
            height=25,
            color=[0.3, 0.3, 0.3, 1],
            bold=True,
        )
        main_layout.add_widget(payment_header)

        payment_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40, spacing=10
        )
        payment_layout.add_widget(
            Label(text="Payment:", size_hint_x=0.3, color=[0, 0, 0, 1])
        )
        payment_modes = ["All"] + self.db_manager.get_dropdown_options("payment_mode")
        self.filter_payment_spinner = Spinner(
            text=self.filter_payment_type,
            values=payment_modes,
            size_hint_x=0.7,
            background_color=[1, 1, 1, 1],
            color=[0, 0, 0, 1],
        )
        payment_layout.add_widget(self.filter_payment_spinner)
        main_layout.add_widget(payment_layout)

        # Expense type section
        expense_header = Label(
            text="Transaction Type",
            size_hint_y=None,
            height=25,
            color=[0.3, 0.3, 0.3, 1],
            bold=True,
        )
        main_layout.add_widget(expense_header)

        expense_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40, spacing=10
        )
        expense_layout.add_widget(
            Label(text="Type:", size_hint_x=0.3, color=[0, 0, 0, 1])
        )
        expense_types = ["All"] + self.db_manager.get_dropdown_options(
            "transaction_type"
        )
        self.filter_expense_spinner = Spinner(
            text=self.filter_expense_type,
            values=expense_types,
            size_hint_x=0.7,
            background_color=[1, 1, 1, 1],
            color=[0, 0, 0, 1],
        )
        expense_layout.add_widget(self.filter_expense_spinner)
        main_layout.add_widget(expense_layout)

        # Buttons
        button_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )
        clear_btn = Button(
            text="CLEAR ALL", background_color=[0.7, 0.7, 0.7, 1], color=[1, 1, 1, 1]
        )
        apply_btn = Button(
            text="APPLY FILTERS", background_color=[0.2, 0.6, 1, 1], color=[1, 1, 1, 1]
        )
        cancel_btn = Button(
            text="CANCEL", background_color=[0.8, 0.2, 0.2, 1], color=[1, 1, 1, 1]
        )

        def clear_filters(*args):
            self.filter_from_date = None
            self.filter_to_date = None
            self.filter_payment_type = "All"
            self.filter_expense_type = "All"
            self.filter_active = False
            self.refresh_transactions()
            filter_popup.dismiss()

        def apply_filters(*args):
            self.filter_payment_type = self.filter_payment_spinner.text
            self.filter_expense_type = self.filter_expense_spinner.text

            # Check if any filters are actually set
            has_filters = (
                self.filter_from_date is not None
                or self.filter_to_date is not None
                or self.filter_payment_type != "All"
                or self.filter_expense_type != "All"
            )

            self.filter_active = has_filters
            self.refresh_transactions()
            filter_popup.dismiss()

        clear_btn.bind(on_release=clear_filters)
        apply_btn.bind(on_release=apply_filters)
        cancel_btn.bind(on_release=lambda x: filter_popup.dismiss())

        button_layout.add_widget(clear_btn)
        button_layout.add_widget(apply_btn)
        button_layout.add_widget(cancel_btn)
        main_layout.add_widget(button_layout)

        filter_popup = Popup(
            title="", content=main_layout, size_hint=(0.9, 0.8), auto_dismiss=False
        )
        filter_popup.open()

    def show_date_picker(self, date_type):
        """Show date picker for filter dates"""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.spinner import Spinner
        from datetime import date

        # Main layout with white background
        date_layout = BoxLayout(orientation="vertical", spacing=5, padding=15)
        with date_layout.canvas.before:
            from kivy.graphics import Color, Rectangle

            Color(1, 1, 1, 1)  # White background
            date_layout.bg_rect = Rectangle(size=date_layout.size, pos=date_layout.pos)
        date_layout.bind(
            size=lambda instance, value: setattr(date_layout.bg_rect, "size", value)
        )
        date_layout.bind(
            pos=lambda instance, value: setattr(date_layout.bg_rect, "pos", value)
        )

        # Title
        title = f"Select {date_type.capitalize()} Date"
        date_layout.add_widget(
            Label(
                text=title, size_hint_y=None, height=30, color=[0, 0, 0, 1], bold=True
            )
        )

        # Current date for default
        current_date = date.today()
        selected_date = getattr(self, f"filter_{date_type}_date") or current_date

        # Headers
        headers_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=25, spacing=5
        )
        headers_layout.add_widget(
            Label(text="Year", size_hint_x=0.33, color=[0.3, 0.3, 0.3, 1], bold=True)
        )
        headers_layout.add_widget(
            Label(text="Month", size_hint_x=0.33, color=[0.3, 0.3, 0.3, 1], bold=True)
        )
        headers_layout.add_widget(
            Label(text="Day", size_hint_x=0.33, color=[0.3, 0.3, 0.3, 1], bold=True)
        )
        date_layout.add_widget(headers_layout)

        # Date selectors
        selectors_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40, spacing=5
        )

        # Year spinner
        years = [str(y) for y in range(2020, 2031)]
        year_spinner = Spinner(
            text=str(selected_date.year),
            values=years,
            size_hint_x=0.33,
            background_color=[1, 1, 1, 1],
            color=[0, 0, 0, 1],
        )

        # Month spinner
        months = [f"{i:02d}" for i in range(1, 13)]
        month_spinner = Spinner(
            text=f"{selected_date.month:02d}",
            values=months,
            size_hint_x=0.33,
            background_color=[1, 1, 1, 1],
            color=[0, 0, 0, 1],
        )

        # Day spinner
        days = [f"{i:02d}" for i in range(1, 32)]
        day_spinner = Spinner(
            text=f"{selected_date.day:02d}",
            values=days,
            size_hint_x=0.33,
            background_color=[1, 1, 1, 1],
            color=[0, 0, 0, 1],
        )

        selectors_layout.add_widget(year_spinner)
        selectors_layout.add_widget(month_spinner)
        selectors_layout.add_widget(day_spinner)
        date_layout.add_widget(selectors_layout)

        # Buttons
        button_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40, spacing=10
        )
        clear_btn = Button(
            text="CLEAR", background_color=[0.7, 0.7, 0.7, 1], color=[1, 1, 1, 1]
        )
        ok_btn = Button(
            text="OK", background_color=[0.2, 0.6, 1, 1], color=[1, 1, 1, 1]
        )
        cancel_btn = Button(
            text="CANCEL", background_color=[0.8, 0.2, 0.2, 1], color=[1, 1, 1, 1]
        )

        def save_date(*args):
            try:
                from datetime import date as Date

                year = int(year_spinner.text)
                month = int(month_spinner.text)
                day = int(day_spinner.text)
                selected = Date(year, month, day)

                setattr(self, f"filter_{date_type}_date", selected)

                # Update button text
                button = getattr(self, f"filter_{date_type}_btn")
                button.text = selected.strftime("%Y-%m-%d")

                date_popup.dismiss()
            except ValueError:
                pass

        def clear_date(*args):
            setattr(self, f"filter_{date_type}_date", None)
            button = getattr(self, f"filter_{date_type}_btn")
            button.text = "Select Date"
            date_popup.dismiss()

        clear_btn.bind(on_release=clear_date)
        ok_btn.bind(on_release=save_date)
        cancel_btn.bind(on_release=lambda x: date_popup.dismiss())

        button_layout.add_widget(clear_btn)
        button_layout.add_widget(ok_btn)
        button_layout.add_widget(cancel_btn)
        date_layout.add_widget(button_layout)

        date_popup = Popup(
            title="", content=date_layout, size_hint=(0.7, 0.5), auto_dismiss=False
        )
        date_popup.open()

    def on_enter(self):
        """Refresh data when entering screen"""
        if self.current_book_id is not None:
            self.refresh_data()

from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView


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
        elif abs_amount >= 1000:  # 1 thousand
            return f"{sign}₹{amount/1000:.1f}K"
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


class BookListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "book_list"
        self.dialog = None
        self.db_manager = None
        self.build_ui()

    def build_ui(self):
        """Build the book list screen UI"""
        main_layout = MDBoxLayout(
            orientation="vertical", padding=[10, 10, 10, 10], spacing=15
        )

        # Header with settings button only
        header_layout = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height="48dp", spacing="10dp"
        )

        # Spacer to push settings button to the right
        header_layout.add_widget(MDLabel())

        settings_btn = MDIconButton(
            icon="cog",
            size_hint_x=None,
            width="50dp",
            theme_icon_color="Custom",
            icon_color=[0.2, 0.6, 1, 1],
            on_release=self.open_settings,
        )
        header_layout.add_widget(settings_btn)
        main_layout.add_widget(header_layout)

        # Centered Logo and Title Header (no background)
        header_section = MDBoxLayout(
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
        header_section.add_widget(logo_layout)

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
        header_section.add_widget(title_label)

        main_layout.add_widget(header_section)

        # Add book button
        add_book_btn = MDRaisedButton(
            text="Add New Book",
            size_hint_y=None,
            height="48dp",
            on_release=self.show_add_book_dialog,
        )
        main_layout.add_widget(add_book_btn)

        # Books scroll view
        self.books_scroll = MDScrollView()
        self.books_layout = MDBoxLayout(
            orientation="vertical", adaptive_height=True, spacing="10dp"
        )
        self.books_scroll.add_widget(self.books_layout)
        main_layout.add_widget(self.books_scroll)

        self.add_widget(main_layout)

    def on_enter(self):
        """Refresh books when entering screen"""
        # Import database manager here to avoid circular imports
        if self.db_manager is None:
            from database import DatabaseManager

            self.db_manager = DatabaseManager()
        self.refresh_books()

    def refresh_books(self):
        """Refresh the books list"""
        self.books_layout.clear_widgets()

        books = self.db_manager.get_books()

        if not books:
            no_books_label = MDLabel(
                text="No books created yet. Add your first book!",
                theme_text_color="Hint",
                halign="center",
            )
            self.books_layout.add_widget(no_books_label)
        else:
            for book_id, name, created_date in books:
                balance = self.db_manager.get_balance(book_id)
                card = self.create_book_card(book_id, name, balance, created_date)
                self.books_layout.add_widget(card)

    def create_book_card(self, book_id, name, balance, created_date):
        """Create a card for each book"""
        card = MDCard(
            size_hint_y=None,
            height="110dp",
            padding="12dp",
            elevation=3,
            radius=[10],
            md_bg_color=[0.95, 0.95, 0.95, 1],
        )

        card_layout = MDBoxLayout(orientation="vertical", spacing="8dp")

        # Top row with name and balance
        top_row = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height="30dp", spacing="5dp"
        )

        book_name = MDLabel(
            text=name if len(name) <= 20 else name[:17] + "...",
            font_style="Subtitle1",
            theme_text_color="Primary",
            halign="left",
            valign="middle",
            markup=True,
        )

        # Format balance with Indian currency formatting
        display_balance = format_indian_currency(balance, short_format=True)

        balance_color = [0, 0.7, 0, 1] if balance >= 0 else [0.8, 0, 0, 1]
        balance_label = MDLabel(
            text=display_balance,
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=balance_color,
            size_hint_x=None,
            width="100dp",
            halign="right",
            valign="middle",
            text_size=("100dp", None),
        )

        top_row.add_widget(book_name)
        top_row.add_widget(balance_label)

        # Middle row with date
        date_label = MDLabel(
            text=f"Created: {created_date[:10]}",
            font_style="Caption",
            theme_text_color="Hint",
            size_hint_y=None,
            height="18dp",
            halign="left",
        )

        # Bottom row with buttons - properly aligned
        button_layout = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height="40dp", spacing="8dp"
        )

        open_btn = MDRaisedButton(
            text="OPEN",
            size_hint_x=0.65,
            height="40dp",
            md_bg_color=[0.2, 0.6, 1, 1],
            font_size="12sp",
        )
        open_btn.bind(on_release=lambda x: self.open_book(book_id, name))

        delete_btn = MDRaisedButton(
            text="DELETE",
            size_hint_x=0.35,
            height="40dp",
            md_bg_color=[0.8, 0.2, 0.2, 1],
            font_size="12sp",
        )
        delete_btn.bind(on_release=lambda x: self.confirm_delete_book(book_id, name))

        button_layout.add_widget(open_btn)
        button_layout.add_widget(delete_btn)

        card_layout.add_widget(top_row)
        card_layout.add_widget(date_label)
        card_layout.add_widget(button_layout)
        card.add_widget(card_layout)

        return card

    def show_add_book_dialog(self, *args):
        """Show dialog to add new book"""
        # Use MDBoxLayout and MDTextField for proper KivyMD integration
        content = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            adaptive_height=True,
            size_hint_y=None,
            height="80dp",
        )

        self.book_name_field = MDTextField(
            hint_text="Enter book name", mode="line", size_hint_y=None, height="56dp"
        )
        content.add_widget(self.book_name_field)

        self.dialog = MDDialog(
            title="Add New Book",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(text="CANCEL", on_release=self.close_dialog),
                MDRaisedButton(text="ADD", on_release=self.add_book),
            ],
        )
        self.dialog.open()

    def add_book(self, *args):
        """Add new book to database"""
        book_name = self.book_name_field.text.strip()

        if not book_name:
            error_dialog = MDDialog(
                title="Error",
                text="Please enter a book name!",
                buttons=[
                    MDRaisedButton(
                        text="OK", on_release=lambda x: error_dialog.dismiss()
                    )
                ],
            )
            error_dialog.open()
            return

        if book_name:
            book_id = self.db_manager.create_book(book_name)
            if book_id:
                self.refresh_books()
                self.close_dialog()
            else:
                # Show error - book name already exists
                error_dialog = MDDialog(
                    title="Error",
                    text="A book with this name already exists!",
                    buttons=[
                        MDRaisedButton(
                            text="OK", on_release=lambda x: error_dialog.dismiss()
                        )
                    ],
                )
                error_dialog.open()

    def close_dialog(self, *args):
        """Close the dialog"""
        if self.dialog:
            self.dialog.dismiss()

    def open_book(self, book_id, book_name):
        """Open a book (go to transaction list)"""
        transaction_screen = self.manager.get_screen("transaction_list")
        transaction_screen.set_current_book(book_id, book_name)
        self.manager.current = "transaction_list"

    def confirm_delete_book(self, book_id, book_name):
        """Confirm book deletion"""
        confirm_dialog = MDDialog(
            title="Confirm Delete",
            text=f"Are you sure you want to delete '{book_name}'?\nAll transactions will be lost!",
            buttons=[
                MDRaisedButton(
                    text="CANCEL", on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=[0.8, 0.2, 0.2, 1],
                    on_release=lambda x: self.delete_book(book_id, confirm_dialog),
                ),
            ],
        )
        confirm_dialog.open()

    def delete_book(self, book_id, dialog):
        """Delete book from database"""
        self.db_manager.delete_book(book_id)
        self.refresh_books()
        dialog.dismiss()

    def open_settings(self, *args):
        """Open settings screen"""
        self.manager.current = "settings"

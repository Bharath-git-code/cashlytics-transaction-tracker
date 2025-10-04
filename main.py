from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from screens.book_list import BookListScreen
from screens.transaction_list import TransactionListScreen
from screens.transaction_form import TransactionFormScreen
from screens.settings import SettingsScreen
from database import DatabaseManager


class TransactionTrackerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Cashlytics - Personal Finance Tracker"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        # Create shared database manager
        self.db_manager = DatabaseManager()

        # Set window size for mobile simulation (optional - remove for actual mobile deployment)
        # Moto Edge 40 approximate resolution: 1080x2400 pixels
        # Window.size = (360, 800)  # Scaled down for desktop testing

    def build(self):
        """Build the app"""
        # Create screen manager
        screen_manager = ScreenManager()

        # Create screens
        book_list_screen = BookListScreen()
        transaction_list_screen = TransactionListScreen()
        transaction_form_screen = TransactionFormScreen()
        settings_screen = SettingsScreen()

        # Set shared database manager
        book_list_screen.db_manager = self.db_manager
        transaction_list_screen.db_manager = self.db_manager
        transaction_form_screen.db_manager = self.db_manager
        settings_screen.db_manager = self.db_manager

        # Add all screens
        screen_manager.add_widget(book_list_screen)
        screen_manager.add_widget(transaction_list_screen)
        screen_manager.add_widget(transaction_form_screen)
        screen_manager.add_widget(settings_screen)

        # Set initial screen
        screen_manager.current = "book_list"

        return screen_manager


def main():
    """Main function to run the app"""
    TransactionTrackerApp().run()


if __name__ == "__main__":
    main()

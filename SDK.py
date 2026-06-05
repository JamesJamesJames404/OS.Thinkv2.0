# SDK.py
# Reproduced Software Development Kit for Think OS Modding
# Rebuilt based on the HBREW Inc. Advanced SDK Reference Guide

import os
import time
import random
from datetime import datetime

class ModSDK:
    def __init__(self, os_instance):
        """Initializes the SDK components by linking to the current OS runtime instance."""
        self.os = os_instance
        self.screen = ScreenUtilities(self)
        self.input = InputUtilities(self)
        self.menu = MenuUtilities(self)
        self.storage = StorageUtilities(self)
        self.utils = GeneralUtilities(self)


class ScreenUtilities:
    def __init__(self, sdk):
        self.sdk = sdk

    def header(self, title):
        """Clears screen and prints a consistent, standard 58-character header."""
        # Check if the main OS has a built-in clear screen command, otherwise use standard terminal clear
        if hasattr(self.sdk.os, 'clear_screen'):
            self.sdk.os.clear_screen()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            
        print("=" * 58)
        # Center the title nicely within the header boundaries
        print(f" {title.upper().center(56)} ")
        print("=" * 58)
        print()


class InputUtilities:
    def __init__(self, sdk):
        self.sdk = sdk

    def get_string(self, prompt, allowed_chars=None):
        """Gets string input from the user with optional character validation loops."""
        while True:
            user_input = input(prompt)
            if allowed_chars:
                # If characters are limited (like menu choices '123'), validate them strictly
                if all(char in allowed_chars for char in user_input) and user_input.strip() != "":
                    return user_input
                print(f"[!] Invalid input. Allowed options: {', '.join(allowed_chars)}")
            else:
                return user_input


class MenuUtilities:
    def __init__(self, sdk):
        self.sdk = sdk

    def create_menu(self, title, options):
        """Displays a clean menu layout using a title and an array of string choices."""
        self.sdk.screen.header(title)
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        print()


class StorageUtilities:
    def __init__(self, sdk):
        self.sdk = sdk

    def save_document(self, name, content):
        """Direct connection to standard internal OS file storage."""
        if hasattr(self.sdk.os, 'user_files'):
            self.sdk.os.user_files[name] = content
            # Try to force the OS instance to commit save state to disk
            if hasattr(self.sdk.os, 'save_data'):
                self.sdk.os.save_data()
            return True
        return False

    def load_document(self, name):
        """Retrieves an internal document from the operating system's database."""
        if hasattr(self.sdk.os, 'user_files'):
            return self.sdk.os.user_files.get(name, None)
        return None

    def save_mod_data(self, mod_name, data):
        """Saves unique key-value configurations localized for a specific mod."""
        # Leverages standard game stat tracking / configuration storage in the core OS engine
        if hasattr(self.sdk.os, 'game_stats'):
            if "mod_data" not in self.sdk.os.game_stats:
                self.sdk.os.game_stats["mod_data"] = {}
            self.sdk.os.game_stats["mod_data"][mod_name] = data
            if hasattr(self.sdk.os, 'save_data'):
                self.sdk.os.save_data()
            return True
        return False

    def load_mod_data(self, mod_name):
        """Loads unique key-value configuration states localized for a specific mod."""
        if hasattr(self.sdk.os, 'game_stats'):
            mod_store = self.sdk.os.game_stats.get("mod_data", {})
            return mod_store.get(mod_name, {})
        return {}


class GeneralUtilities:
    def __init__(self, sdk):
        self.sdk = sdk

    def sleep(self, seconds):
        """Pauses execution."""
        time.sleep(seconds)

    def wrap_text(self, text, width=50):
        """Breaks down paragraph walls dynamically to fit standard terminal boundaries."""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            # +1 accounts for the space between words
            if current_length + len(word) + len(current_line) <= width:
                current_line.append(word)
                current_length += len(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        if current_line:
            lines.append(" ".join(current_line))
            
        return "\n".join(lines)

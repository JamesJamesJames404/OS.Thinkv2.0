# think_browser.py
# A Text-Mode Web Browser Mod for ThinkOS
# Treats local files as static web domains

import os
from SDK import ModSDK 
def run_mod(os_instance):
    sdk = ModSDK(os_instance)
    
    current_url = "HOME.txt"
    history = []
    
    while True:
        sdk.screen.header(f"THINK-BROWSER v1.0 | URL: {current_url}")
        
        if current_url.endswith(".txt") or current_url.endswith(".html"):
            if os.path.exists(current_url):
                try:
                    with open(current_url, "r", encoding="utf-8") as f:
                        page_content = f.read()
                    
                    print("\n" + "-"*60)
                    wrapped_text = sdk.utils.wrap_text(page_content, width=58)
                    print(wrapped_text)
                    print("-"*60 + "\n")
                    
                except Exception as e:
                    print(f"\n[!] BROWSER ERROR: Could not render page. ({e})\n")
            else:
          
                print("\n" + "="*58)
                print(" PROBLEM 404 - FILE NOT FOUND")
                print("="*58)
                print(f"The file called '{current_url}' could not be reached and opened.")
                print("Make sure the file exists in your folder.")
                print("="*58 + "\n")
        else:
            print("\n[!] BROWSER ERROR: Think-Browser only supports .txt and .html files.\n")
        
        print("BROWSER MENU:")
        print("1) Enter New URL")
        print("2) Go Back")
        print("3) Exit Browser")
        print()
        
        choice = sdk.input.get_string("Choose an option: ", allowed_chars="123")
        
        if choice == "1":
            new_url = sdk.input.get_string("Enter URL (e.g., TEST.txt): ")
            if new_url.strip():
                history.append(current_url)
                current_url = new_url
                
        elif choice == "2":
            if history:
                current_url = history.pop()
            else:
                print("\n[!] No history to go back to.\n")
                sdk.utils.sleep(1)
                
        elif choice == "3":
            print("\nClosing Think Browser... Returning to Desktop.")
            sdk.utils.sleep(1)
            break

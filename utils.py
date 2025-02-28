import os
from datetime import datetime

def save_content_to_file(content: str, title: str, folder: str = "output"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    sanitized_title = "".join(c if c.isalnum() else "_" for c in title)
    filename = f"{date_str}_{sanitized_title}.txt"
    filepath = os.path.join(folder, filename)
    
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
    
    print(f"Content saved to {filepath}")

import os
from datetime import datetime

def save_content_to_file(content: str, title: str = None) -> str:
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"{current_date}.txt"
    file_path = os.path.join(output_dir, filename)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nContent saved successfully to: {file_path}")
        return file_path
    except Exception as e:
        print(f"\nError saving content to file: {str(e)}")
        return None

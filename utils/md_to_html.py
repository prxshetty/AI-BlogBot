import markdown
import webbrowser
import os
import logging

logger = logging.getLogger(__name__)

# Define the CSS that "tricks" Medium into preserving formatting
# We map specific Markdown elements to the CSS styles Medium's paste parser expects.
MEDIUM_STYLE = """
<style>
    body { 
        font-family: Georgia, serif; /* Triggers Medium's serif detector */
        line-height: 1.5;
        max-width: 700px;
        margin: 0 auto;
        padding: 20px;
    }
    /* BLOCKS */
    h1 { font-size: 32px; font-weight: bold; margin-top: 2em; }
    h2 { font-size: 26px; font-weight: bold; margin-top: 1.5em; }
    h3 { font-size: 22px; font-weight: bold; margin-top: 1.2em; }
    p { margin-bottom: 1.2em; }
    
    /* CODE BLOCKS (Crucial for ML work) */
    pre { 
        background: #f0f0f0; 
        padding: 10px; 
        border-radius: 4px; 
        font-family: Menlo, monospace;
        white-space: pre-wrap; /* Preserves line breaks in code */
        overflow-x: auto;
    }
    
    /* INLINE / WORD LEVEL */
    code { 
        background: rgba(0,0,0,0.05); 
        padding: 2px 4px; 
        border-radius: 3px; 
        font-family: Menlo, monospace; 
    }
    blockquote {
        border-left: 4px solid #ccc;
        padding-left: 16px;
        font-style: italic;
        color: #666;
        margin: 1.5em 0;
    }
    
    /* LISTS */
    ul, ol {
        margin-bottom: 1.2em;
        padding-left: 2em;
    }
    li {
        margin-bottom: 0.5em;
    }
    
    /* TABLES */
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 1.5em 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f0f0f0;
        font-weight: bold;
    }
</style>
"""

def convert_md_to_html(input_file: str, output_dir: str = "output") -> str:
    """
    Convert a markdown file to Medium-ready HTML.
    
    Args:
        input_file: Path to the markdown file
        output_dir: Directory to save the HTML file (default: "output")
    
    Returns:
        Path to the generated HTML file
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # ENABLE EXTENSIONS (The "Intelligence" part)
        # - fenced_code: Handles ```
        # - tables: Handles | tables |
        # - sane_lists: Fixes mixed ordered/unordered list confusion
        html_content = markdown.markdown(text, extensions=[
            'fenced_code', 
            'tables',
            'sane_lists'
        ])

        # Wrap in the final HTML container
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Medium Export</title>
    {MEDIUM_STYLE}
</head>
<body>
    {html_content}
</body>
</html>
"""

        # Create output filename based on input filename
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_filename = f"{base_name}.html"
        output_path = os.path.join(output_dir, output_filename)
        
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        logger.info(f"✅ Converted '{input_file}' -> '{output_path}'")
        
        # Open in browser
        webbrowser.open('file://' + os.path.realpath(output_path))
        
        return output_path
        
    except Exception as e:
        logger.error(f"❌ Error converting markdown to HTML: {str(e)}")
        raise

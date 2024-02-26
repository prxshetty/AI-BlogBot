# Blog Bot with AI Paraphraser
Paraphrases the content using pegasus from API or website using BeautifulSoup.

### Dependencies
- BeautifulSoup
- requests
- urllib
- torch
- requests_html
- transformer
- Pegasus
- Python 3
  
### Functionality:
Fetching Headlines: The script fetches headlines from any category of any website and displays them with their respective indexes to select them.

Fetching Article Content: It allows users to select a headline by its index and fetches the content of the corresponding article along with  paraphrasing/summarizing it.

### How to Use:
Install the required libraries using pip:
- pip install beautifulsoup4 requests requests-html torch transformers
Run the script. It will display the headlines.
Choose the website which you want and add it to the base_url parameter. then select the category and add it to the relative_url parameter.
Choose a headline by its index, and the script will fetch and display the article content.

## Note
The paraphrased content might not always be perfect, and manual review might be necessary depending on the element you want to extract data from.
This script is for educational and demonstration purposes only. Ensure compliance with any website's terms of service when using their content.
The Pegasus model used for paraphrasing needs to be fine-tuned for better results in production scenarios.In this project i had to split the data into chunks and further divide the data into paragraphs so ensure maximium accuracy so that the AI couldn't hallucinate.

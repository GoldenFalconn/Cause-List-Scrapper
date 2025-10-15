import requests
from bs4 import BeautifulSoup
import os

# URL for Orissa High Court cause lists
url = 'https://www.orissahighcourt.nic.in/cause-list/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Create directory for saving PDFs if it doesn't exist
os.makedirs('cause_lists', exist_ok=True)

# Find all links to PDF files on the page
pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))

for link in pdf_links:
    pdf_url = link['href']
    # Convert relative URLs to absolute
    if not pdf_url.startswith('http'):
        pdf_url = 'https://www.orissahighcourt.nic.in' + pdf_url

    file_name = os.path.join('cause_lists', pdf_url.split('/')[-1])
    print(f"Downloading {file_name} ...")
    
    with requests.get(pdf_url, stream=True) as r:
        r.raise_for_status()
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

print("All PDFs downloaded.")

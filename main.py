import requests
from bs4 import BeautifulSoup

urls = ["https://www.kpi.ua/"]

for url in urls:
    # Send GET for page
    response = requests.get(url)

    # test success
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
    else:
        # Parse HTML-code with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # extract text from the tags Title, Description and all tags containing text
        title = soup.find('title').get_text()
        description = soup.find('meta', attrs={'name': 'description'})['content']
        text = ''
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text += tag.get_text() + '\n'

        # create a file with a name corresponding to the last word in the domain name
        domain_name = url.split('.')[-2:]
        filename = f"{domain_name[0]}.txt"
        filename1 = filename.replace("/", "-")
        with open(filename1, 'w', encoding='utf-8') as f:
            f.write(f"[Title]\n{title}\n\n[Description]\n{description}\n\n[Text]\n{text}")
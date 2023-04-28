import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# Initialize sets to store internal and external URLs
internal_urls = set()
external_urls = set()

# Initialize counter for the total number of URLs visited
total_urls_visited = 0

def is_valid(url):
    # Check if the URL has a valid format
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    # Function to extract all links on a given web page
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        # Join the URL if it's relative (not an absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # Remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        # Check if the URL belongs to the same domain or not
        if domain_name not in href:
            if href not in external_urls:
                print(f'"{href},"')
                external_urls.add(href)
            continue
        print(f'"{href},"')
        urls.add(href)
        internal_urls.add(href)
    return urls

def crawl(url, max_urls=30):
    # Function to crawl the website and visit all internal links
    global total_urls_visited
    total_urls_visited += 1
    print(f'"{url},"')
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

if __name__ == "__main__":
    import argparse

    # Set the starting URL and maximum number of URLs to visit
    url = 'https://www.kpi.ua/'
    max_urls =10

    # Crawl the website starting from the specified URL
    crawl(url, max_urls=max_urls)

    # Print the total number of internal and external URLs found
    print("Total Internal links:", len(internal_urls))
    print("Total External links:", len(external_urls))
    print("Total URLs:", len(external_urls) + len(internal_urls))

    domain_name = urlparse(url).netloc

   # Save internal links in a file
    with open(f"internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(f'"{internal_link}",', file=f)

    # Save external links in a file
    with open(f"external_links.txt", "w") as f:
        for external_link in external_urls:
            print(f'"{external_link}",', file=f)

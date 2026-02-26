import argparse, urllib.request
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import re
import requests
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box


def parser():
    parser = argparse.ArgumentParser(
        prog='spider',
        description='Extract images from a website recursively.'
    )
    parser.add_argument(
        '-r',
        dest='recursive_enable',
        default=False, action='store_true',
        help="Recursively downloads images from the URL.",
    )
    parser.add_argument(
        '-l',
        metavar='DEPTH', dest='level',
        type=int, default=5,
        help="Maximum depth level of the recursive download (default: 5)."
    )
    parser.add_argument(
        '-p',
        metavar='PATH', dest='path',
        type=str, default='./data/',
        help="Path where the downloaded files will be saved (default: ./data/).",
    )
    parser.add_argument(
        'URL',
        type=str,
        help="The URL to scrape images from."
    )
    return parser.parse_args()

parsed_args = parser()
print(parsed_args)

imgs_downloaded = []

DOWNLOAD_PATH = parsed_args.path
BASE_URL = parsed_args.URL
RECURSIVE_MODE = parsed_args.recursive_enable
RECURSIVE_MAX_DEPTH = parsed_args.level

MAX_WORKERS = 10
MAX_RETRIES = 3
allowed_img_types = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

console = Console()


def get_html(url) -> str :
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Error al acceder a {url}: {e}")
        return ""


def find_img_tags(url, html):
    imgs_new = []
    soup = BeautifulSoup(html, 'html.parser')
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        img_url_absolute = urljoin(url, img_url) if img_url else None
        if img_url_absolute and any(img_url_absolute.lower().endswith(ext) for ext in allowed_img_types):
            imgs_new.append(img_url_absolute)
    return imgs_new



def is_valid_content_link(url):
    def is_same_domain(url):
        return urlparse(url).netloc == urlparse(BASE_URL).netloc

    blacklist_patterns = [
        r'\.php', r'\.cgi', r'\.asp', r'\.aspx',  # Server-side scripts
        r'\?', r'\&', r'\=',                      # Query parameters (forms/searches)
        r'#',                                     # Internal page anchors
        r'mailto:', r'tel:',                      # Communication links
        r'javascript:',                           # Inline scripts
        r'/wp-admin/', r'/login', r'/register'    # Admin/System paths
    ]
    
    file_blacklist = [
        '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', 
        '.xml', '.rss', '.css', '.js', '.json'
    ]

    if not is_same_domain(url):
        return False
    if any(re.search(pattern, url, re.IGNORECASE) for pattern in blacklist_patterns):
        return False
    if any(url.lower().endswith(ext) for ext in file_blacklist):
        return False
    return True


def find_a_tags(url_base, html, urls_visited) -> set :
    next_level_urls = set()
    soup = BeautifulSoup(html, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        url_absolute = urljoin(url_base, a_tag.get('href'))
        if url_absolute and url_absolute not in urls_visited and is_valid_content_link(url_absolute):
            next_level_urls.add(url_absolute)
    return next_level_urls


def download_img(url_img) -> dict :
    def download_and_store(url, folder=DOWNLOAD_PATH) -> str:
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, url.split("/")[-1])
        if os.path.exists(filename):
            return {
                'status': "Alert",
                'filename': filename,
                'msg': "Was already downloaded"
            }
        try:
            with requests.get(url, headers=headers, stream=True) as r:
                r.raise_for_status()
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return {
                    'status': "Okey",
                    'filename': filename,
                    'msg': "Downloaded"
                }
        except Exception as e:
                return {
                    'status': "Error",
                    'filename': filename,
                    'msg': f"{e}"
                }


    if url_img in imgs_downloaded:
        return {
                    'status': "Alert",
                    'filename': url_img,
                    'msg': "Was already downloaded"
                }
    imgs_downloaded.append(url_img)
    return download_and_store(url_img)


def download_imgs(url, html, executor) -> None :
    imgs_new = find_img_tags(url, html)
    results = executor.map(download_img, imgs_new)

    # console.print(Text(f"\n---- {url} ----", style="bold magenta", no_wrap=True))

    title_panel = Panel(
        Text(f"{url}", style="bold magenta", no_wrap=True),
        style="cyan",
        box=box.SQUARE,
        expand=True
    )

    # 2. Create the Table
    table = Table(expand=True, box=box.SQUARE)
    table.add_column("Status", width=10)
    table.add_column("Filename", ratio=1)
    table.add_column("Message", ratio=1)

    colors = {
        'Okey': "cyan",
        'Alert': "yellow",
        'Error': "red"
    }

    for item in results:
        status_color = colors[item["status"]]
        table.add_row(
            f"[{status_color}]{item["status"]}[/{status_color}]",
            item["filename"],
            item['msg']
        )

    console.print(title_panel)
    console.print(table)
    console.print("")

if __name__ == '__main__':

    current_level_urls = {BASE_URL}
    urls_visited = set()

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for depth in range(RECURSIVE_MAX_DEPTH + 1):
                print(f"------- scraping DEPTH: {depth} -------")

                next_level_urls = set()

                for url in current_level_urls:
                    if url in urls_visited:
                        continue
                    urls_visited.add(url)
                    
                    html = get_html(url)
                    if not html:
                        continue

                    download_imgs(url, html, executor)

                    if RECURSIVE_MODE and depth < RECURSIVE_MAX_DEPTH:
                        next_level_urls = find_a_tags(url, html, urls_visited)
            
                current_level_urls = next_level_urls
                if not current_level_urls:
                    break

    except KeyboardInterrupt:
        print("\n[!] Interrupt detected! Shutting down safely...")
        executor.shutdown(wait=False, cancel_futures=True)
        print(f"[+] Progress saved. Total URLs visited: {len(urls_visited)}")
        print(f"[+] Check \"{DOWNLOAD_PATH}\" folder for downloaded images.")

    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")


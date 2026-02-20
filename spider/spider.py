import argparse, urllib.request, urllib.parse
from bs4 import BeautifulSoup

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


def get_html() -> str :

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    url = parsed_args.URL
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Error al acceder a {url}: {e}")
        return ""


def find_img_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        print("img_url: ", img_url)


def find_a_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    for a_tag in soup.find_all('a'):
        url = a_tag.get('href')
        if url:
            print("next_url: ", url)
        else:
            print("a:", a_tag)

parsed_args = None

if __name__ == '__main__':
    parsed_args = parser()
    print(parsed_args)
    html = get_html()
    find_img_tags(html)
    find_a_tags(html)

# from concurrent.futures import ThreadPoolExecutor
# import time

# def download_img(url_img):
#     print(f"Iniciando descarga de: {url_img}")
#     time.sleep(1)
#     return f"OK: {url_img}"

# url_lst = ["img1.png", "img2.jpg", "img3.gif"]

# with ThreadPoolExecutor(max_workers=10) as executor:
#     # .map() send each URL from the list to the function 'download_img()'
#     results = executor.map(download_img, url_lst)

# # 'results' generator with the result from each function 'dowload_img()'
# i = 0
# for r in results:
#     print("res: ", r)
#     i += 1
# print("size: ", i)
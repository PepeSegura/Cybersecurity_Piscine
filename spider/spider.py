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


def get_html(url) -> str :
    return urllib.request.urlopen(url).read().decode('utf-8', errors='replace')

def find_img_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        print("img_url: ", img_url)

def find_a_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    for a_tag in soup.find_all('a'):
        url = a_tag.get('href')
        print("next_url: ", url)

if __name__ == '__main__':
    parsed_args = parser()
    print(parsed_args)
    html = get_html(parsed_args.URL)
    find_img_tags(html)
    find_a_tags(html)

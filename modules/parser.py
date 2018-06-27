import time 
import requests
from bs4 import BeautifulSoup

def fetch_page(url=None):
    '''
    fetch_page taske a url and returns the content of the fetched page
    '''
    if url is None:
        return
    print('Requesting url: {}'.format(url))
    # pause one second to prevent being blacklisted
    # some servers black list scripts that try to access
    time.sleep(0.1)
    response = requests.get(url)
    if response and response.content is not None:
        return response.content
    return None

def parse_woman_link_url(content=None):
    if content is None:
        return None
    print('Parsing page...')
    soup = BeautifulSoup(content,'html5lib')
    # find the parent div for all categories in woman
    woman_category_div1 = soup.find('div', class_='primary-menu-sub-menu-inner')
    print()
    # print(woman_category_div1)
    # for item in woman_category_div1.select('.primary-menu-category'):
    #     print('item')
    #     print(item)

    woman_category_div = soup.find('div', class_='primary-menu-sub-menu').select('.primary-menu-category')

    if woman_category_div is None:
        print("Failed to get categories parent div")
        return None

    # start appending to categories
    start = False
    # end appending to categories
    end = False
    sub_categories = []
    for category in woman_category_div:
        heading = category.select('.sub-sub-heading')
        name = ''
        if len(heading) > 0 and heading[0].text:
            name = heading[0].text
        print('name: {}'.format(name))
        # parse only categories between 'sub-sub-heading' with text 'Shop by Product' and 'Selected'
        if 'Shop by Product' in name:
            start = True
        elif 'Selected' in name:
            # skep the rest
            return sub_categories
        if start and not end:
            print('parsing "{}"...'.format(name))
            for sub in category.select('ul li a'):
                # skip the view all link
                if 'view-all' in sub['href']:
                    continue
                url = stitch_url('http://www2.hm.com', sub['href'])
                print('URL: {}'.format(url))
                sub_categories += [{'url': url, 'name': sub.text.strip()}]
            
            # if reached here means category is found
            # return sub_categories
        else:
            print('skipping "{}"...'.format(name))
    return []

def stitch_url(base_url, path):
    '''
    stitch_url concatinates base url with with the path to get full url
    '''
    url = ''
    if path.startswith('/'):
        if base_url.endswith('/'):
            url = base_url + path[1:]
        else:
            url = base_url + path
    elif path.startswith('http'):
        # path is full url
        return path
    return url

def extract_item_count(category_url):
    '''
    extract_item_count finds the number of items in a category from the category_url page
    '''
    number_of_items = 0
    category_name = ''
    print('extracting count and last item url from {}'.format(category_url))
    if category_url is None or category_url == '':
        return None, None
    # parse the count from the category_url
    page = fetch_page(category_url)
    soup = BeautifulSoup(page,'html5lib')
    count = soup.find('span', class_='total-count')
    url = find_last_item_url(soup)
    return [count.text.strip() or 0, stitch_url('http://www2.hm.com', url)]



def find_name_in_category_url(category_url):
    parts = category_url.split('/')
    if len(parts) > 0:
        parts = parts[-1].split('.')
    else:
        return None
    # remove the extention
    name = ''
    if len(parts) > 0:
        name = parts[0]
    return name.capitalize().replace('-', ' ')

def find_last_item_url(soup=None):
    '''
    find_last_item_url finds category page's last item
    '''
    if soup is None:
        return None
    # get the page and parse
    wrapper_div = soup.find('div', class_='product-items-wrapper')
    all_items = wrapper_div.select('article h3.product-item-heading a')
    url = ''
    if len(all_items) > 0:
        last_item = all_items[-1]
        print('last item: {}'.format(last_item.text))
        if len(last_item) > 0:
            url = last_item.get('href')
    return url

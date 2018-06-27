from modules import *

if __name__=='__main__':
    url = 'http://www2.hm.com/en_asia2/index.html'
    page = fetch_page(url)
    woman_categories = parse_woman_link_url(page)
    if woman_categories == [] or woman_categories is None:
        print('Failed to parse categories links')
        exit(1)
    print('found {} sub categories in woman categories'.format(len(woman_categories)))
    lines = ''
    for category in woman_categories:
        # fetch number of items in each category
        # name = find_name_in_category_url(category)
        if category is None or type(category) is not dict:
            continue
        name = category.get('name')
        url = category.get('url')
        if name == '' or url == '':
            continue
        count, last_item_url = extract_item_count(url)
        lines += '{name},{count},{url}\n'.format(name=name, count=count, url=last_item_url)
    
    print()
    # write to file
    file = WomanFile(lines)
    file.save()
    # print(lines)
        
    
    exit(0)
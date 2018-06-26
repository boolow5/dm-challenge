from modules import *

if __name__=='__main__':
    url = 'http://www2.hm.com/en_asia2/index.html'
    page = fetch_page(url)
    woman_categories = parse_woman_link_url(page)
    print('found {} sub categories in woman categories'.format(len(woman_categories)))
    lines = ''
    for category in woman_categories:
        # fetch number of items in each category
        name = find_name_in_category_url(category)
        count = extract_item_count(category)
        lines += '{name},{count},{url}\n'.format(name=name, count=count, url=category)
    
    print()
    # write to file
    file = WomanFile(lines)
    file.save()
    # print(lines)
        
    
    print("Done!")
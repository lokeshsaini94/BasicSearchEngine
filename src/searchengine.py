# My basic search engine


# Gets html code of the page
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ''


# Finds url and the url end point
def get_next_link(s):
    start_link = s.find("<a href=")
    # Returns None if no "<a href" is found
    if start_link == -1:
        return None, 0
    url_start = s.find('"', start_link)
    url_end = s.find('"', url_start+1)
    url = s[url_start+1:url_end]
    return url, url_end


# Prints all urls
def get_all_links(page):
    links = []
    links.append(link)
    while True:
        url, endpos = get_next_link(page)
        # Prints the url recived from get_next_link till the url is not None
        if url:
            links.append(url)
            # Sets starting position of page to the end point of last url found
            page = page[endpos:]
        else:
            break
    return links


# Adds variables from list q to p except the one that already exist in list p, hence union
def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)


# Crawls links from webpages
def crawl_web(link):
    tocrawl = [link]
    crawled = []
    index = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(content))
        crawled.append(page)
    return crawled


# Index Struture: [[keyword1, [url1, url2]], [keyword2, [url1]], [keyword3, [url1, url2, url3]]]
# Adds keyword and its url to the index list.
def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    index.append([keyword, [url]])


# Returns the url of the keyword searched for
def lookup(index, word):
    for entry in index:
        if entry[0] == word:
            return entry[1]
    return "Nothing found", []


# Splits each word from the text provided and runs add_to_index procedure
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


# Makes index of all words and their links in all fetched links from the page(including index)
def get_text(index, link):
    x = 0
    all_links = get_all_links(get_page(link))
    # print len(all_links)
    while x < len(all_links):
        add_page_to_index(index, all_links[x], get_page(all_links[x]))
        x += 1


index = []  # Stores index of all words.
link = "http://www.udacity.com/cs101x/index.html"  # Link to fetch and search from

# Execution of procedures.
# print get_all_links(get_page(link))
get_text(index, link)

# Prints links where searched word is found
print lookup(index, "to")

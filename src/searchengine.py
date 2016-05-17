# My basic search engine


# Gets html code of the page
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""


# Adds variables from list q to p except the one that already exist in list p, hence union
def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)


# Finds url and the url end point
def get_next_link(s):
    start_link = s.find("<a href=")
    if start_link == -1:
        return None, 0
    url_start = s.find('"', start_link)
    url_end = s.find('"', url_start + 1)
    url = s[url_start + 1:url_end]
    return url, url_end


# Prints all urls
def get_all_links(page):
    links = []
    # links.append(link)
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


# Adds a keyword to the index list.
def add_to_index(index, keyword, url):
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]


# Splits a page in keywords and add them to the index
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


# Returns a List of URLs linked to the keyword
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    return None


# Crawls links from webpages
def crawl_web(link):
    tocrawl = [link]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}  # <key>, [list of URLs]
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


# Computing ranks for a given graph
def compute_ranks(graph):
	d = 0.8
	numloops = 10
	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0 / npages
	for i in range(0, numloops):
		newranks = {}
		for page in graph:
			newrank = (1-d)/npages
			for node in graph:
				if page in graph[node]:
					newrank = newrank + d * (ranks[node] / len(graph[node]))
			newranks[page] = newrank
		ranks = newranks
	return ranks


# Sorting in descending order
def quick_sort(pages, ranks):
	if len(pages) > 1:
		piv = ranks[pages[0]]
		i = 1
		j = 1
		for j in range(1, len(pages)):
			if ranks[pages[j]] > piv:
				pages[i], pages[j] = pages[j], pages[i]
				i += 1
		pages[i-1], pages[0] = pages[0], pages[i-1]
		quick_sort(pages[1:i], ranks)
		quick_sort(pages[i+1:len(pages)], ranks)


# Function that returns the one URL most likely to be the best site for that
# keyword. If the keyword does not appear in the index return None
def lucky_search(index, ranks, keyword):
    return_url = ''
    if ketword not in index:
        return None
    for url in index[keyword]:
        if url in ranks:
            if return_url != '':
                if ranks[url] > ranks[return_url]:
                    return_url = url
            else:
                return_url = url
    return return_url


# Function that returns the list of all URLs for that keyword. Ordered by page
# rank. If the keyword does not appear in the index return None
def ordered_search(index, ranks, keyword):
    pages = lookup(index, keyword)
    return quick_sort(pages, ranks)


# Help function that uses quick sort algorithm to order array
def quick_sort(pages, ranks):
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = ranks[pages[0]] #find pivot
        worse = []
        better = []
        for page in pages[1:]:
            if ranks[page] <= pivot:
                worse.append(page)
            else:
                better.append(page)
    return quick_sort(better, ranks) + [pages[0]] + quick_sort(worse, ranks)


# Execution of procedures.
# Link to search from
link = "http://www.udacity.com/cs101x/index.html"  # Link to fetch and search from
# link = "http://xkcd.com/353"

#Keyword to look for
keyword = "to" # raw_input()

# Crawling the page
index, graph = crawl_web(link)

# Ranking the page
ranks = compute_ranks(graph)

# Printing the results
print ordered_search(index, ranks, keyword)

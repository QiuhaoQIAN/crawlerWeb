from HTMLPage import *

class Crawler(object):
    """
    This is an iterable object, every round return a object HTMLPage
    L'instance du crawler va avoir comme principaux attributs
    """

    def __init__(self, urlOrigine, maxPages=1000,
                 pageFilter=None):
        if pageFilter is None:
            pageFilter = []
        # we just download the code of url which exist in pageFilter
        self.pageFilter = pageFilter
        self.urlOrigine = urlOrigine
        self.maxPages = maxPages

        # Each key is a URL, and the value for the key url is the list
        self.pagesToCrawl_dict = {}

        # set of the pages to be crawled
        self.pagesToCrawl = set([])

        # set of the pages already crawled
        self.pagesCrawled = set([])

        #  set of the domains already crawled
        self.domainsCrawled = set([])

    def update_pagesToCrawl(self, page):
        """
        update pagesToCrawl_dict and pagesToCrawl when the url of this page pass filtre
        """
        # check if the page from which we got URLs pass the pageFilter
        pass_filter = False
        for p in self.pageFilter:
            if p in page.url:
                pass_filter = True

        if pass_filter:
           for url in page.urls:
                # update the set if url not already crawled
                if url not in self.pagesCrawled:
                    self.pagesToCrawl.add(url)

                # update pagesToCrawl_dict
                if url in self.pagesToCrawl_dict:
                    self.pagesToCrawl_dict[url].append(page.url)
                else:
                    self.pagesToCrawl_dict[url] = [page.url]



    def __iter__(self):
        """
       :return a HTMLObject
        every round we update pagesCrawled, domainsCrawled, pagesToCrawl and pagesToCrawl_dict
        """
        page = HTMLPage(self.urlOrigine)
        self.pagesCrawled.add(self.urlOrigine)
        self.domainsCrawled.add(extract_urls(self.urlOrigine)[1])
        self.update_pagesToCrawl(page)
        yield page

        while (self.pagesToCrawl and
                       len(self.pagesCrawled) < self.maxPages):
            url = self.pagesToCrawl.pop()
            page = HTMLPage(url)
            self.pagesCrawled.add(url)
            self.domainsCrawled.add(extract_urls(url)[1])
            self.update_pagesToCrawl(page)
            yield page
        raise StopIteration


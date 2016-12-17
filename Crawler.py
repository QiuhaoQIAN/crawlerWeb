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
        self.pagesToCrawled_dict = {}

        # set of the pages to be crawled
        self.pagesToCrawled = set([])

        # set of the pages already crawled
        self.pagesCrawled = set([])

        #  set of the domains already crawled
        self.domainsCrawled = set([])

    def update_pagesToCrawled(self, page):
        """
        Prend un objet HTMLpage comme argument et trouve toutes les
        URLs presente dans la page HTML correspondante. Cette methode
        met a jour le dictionnaire pagesToCrawled_dict et
        l'ensemble pagesToCrawled. On ne met pas a jour le
        dictionnaire et le set si l'URL correspondant a l'objet
        HTMLpage n'est pas dans la liste de pages acceptees dans
        self.pageFilter.
        """
        # check if the page from which we got URLs pass the pageFilter
        pass_filter = False
        for p in self.pageFilter:
            if p in page.url:
                pass_filter = True

        if pass_filter:
            # update the list of pages to be crawled with the URLs
            for url in page.urls:
                # update the dict even if url already crawled (to get
                # comprehensif information)
                if url in self.pagesToCrawled_dict:
                    self.pagesToCrawled_dict[url].append(page.url)
                else:
                    self.pagesToCrawled_dict[url] = [page.url]

                # update the set if url not already crawled
                if url not in self.pagesCrawled:
                    self.pagesToCrawled.add(url)

    def __iter__(self):
        """
        A chaque appel de next() sur l'iterateur, on obtient un nouvel
        objet HTMLPage qui correspond a une URL qui etait dans
        l'ensemble des URLs a crawler.

        On ne donne aucune garantie sur l'ordre de parcours des URLs
        """
        page = HTMLPage(self.urlOrigine)
        self.pagesCrawled.add(self.urlOrigine)
        self.domainsCrawled.add(extract_urls(self.urlOrigine)[1])
        self.update_pagesToCrawled(page)
        yield page

        while (self.pagesToCrawled and
                       len(self.pagesCrawled) < self.maxPages):
            url = self.pagesToCrawled.pop()
            page = HTMLPage(url)
            self.pagesCrawled.add(url)
            self.domainsCrawled.add(extract_urls(url)[1])
            self.update_pagesToCrawled(page)
            yield page
        raise StopIteration


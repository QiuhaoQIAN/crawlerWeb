from HTMLPage import *

class Crawler(object):
    """
    Cette classe permet de creer l'objet qui va gerer le crawl. Cet
    objet est iterable et l'iterateur va, a chaque tour, retourner un
    nouvel objet HTMLPage.

    L'instance du crawler va avoir comme principaux attributs
      * l'ensemble des pages a crawler pages_to_be_crawled
      * l'ensemble des pages deja crawles pages_crawled
      * un dictionnaire qui a chaque URL fait correspondre la liste de
      toutes les pages qui ont reference cette URL lors du crawl
      pages_to_be_crawled_dict
    """

    def __init__(self, seed_url, max_crawled_pages=10 ** 10,
                 page_filter=None):
        """
        Constructeur du crawler

        Le constructeur prend comme arguments
        -seed_url: l'URL de la page a partir de laquelle on demarre le crawl
        -max_crawled_pages: le nombre maximum de pages que l'on va crawler
        (10**10 par defaut)
        -page_filter: la liste des pages sur lesquels le crawler
        doit rester (pas de filtre par defaut). Typiquement, une URL
        passe le filtre si n'importe lequel des elements de page_filter
        est contenu dans l'URL
        """
        if page_filter is None:
            page_filter = []
        self.page_filter = page_filter
        self.seed_url = seed_url
        self.max_crawled_pages = max_crawled_pages

        # Each key is a URL, and the value for the key url is the list
        # of pages that referenced this url. This dict is used to find
        # pages that references given URLs in order to diagnose
        # buggy Web pages.
        self.pages_to_be_crawled_dict = {}

        # set of the pages still to be crawled
        self.pages_to_be_crawled = set([])

        # set of the pages/domains already crawled
        self.pages_crawled = set([])
        self.domains_crawled = set([])

    def update_pages_to_be_crawled(self, page):
        """
        Prend un objet HTMLpage comme argument et trouve toutes les
        URLs presente dans la page HTML correspondante. Cette methode
        met a jour le dictionnaire pages_to_be_crawled_dict et
        l'ensemble pages_to_be_crawled. On ne met pas a jour le
        dictionnaire et le set si l'URL correspondant a l'objet
        HTMLpage n'est pas dans la liste de pages acceptees dans
        self.page_filter.
        """
        # check if the page from which we got URLs pass the page_filter
        pass_filter = False
        for p in self.page_filter:
            if p in page.url:
                pass_filter = True

        if pass_filter:
            # update the list of pages to be crawled with the URLs
            for url in page.urls:
                # update the dict even if url already crawled (to get
                # comprehensif information)
                if url in self.pages_to_be_crawled_dict:
                    self.pages_to_be_crawled_dict[url].append(page.url)
                else:
                    self.pages_to_be_crawled_dict[url] = [page.url]

                # update the set if url not already crawled
                if url not in self.pages_crawled:
                    self.pages_to_be_crawled.add(url)

    def __iter__(self):
        """
        A chaque appel de next() sur l'iterateur, on obtient un nouvel
        objet HTMLPage qui correspond a une URL qui etait dans
        l'ensemble des URLs a crawler.

        On ne donne aucune garantie sur l'ordre de parcours des URLs
        """
        page = HTMLPage(self.seed_url)
        self.pages_crawled.add(self.seed_url)
        self.domains_crawled.add(extract_urls(self.seed_url)[1])
        self.update_pages_to_be_crawled(page)
        yield page

        while (self.pages_to_be_crawled and
                       len(self.pages_crawled) < self.max_crawled_pages):
            url = self.pages_to_be_crawled.pop()
            page = HTMLPage(url)
            self.pages_crawled.add(url)
            self.domains_crawled.add(extract_urls(url)[1])
            self.update_pages_to_be_crawled(page)
            yield page
        raise StopIteration


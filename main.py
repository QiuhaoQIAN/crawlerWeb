#!/usr/bin/env python

from Crawler import *

def getPageMorts(url, page_filter):
    crawl = Crawler(url, page_filter=page_filter)
    dead_urls = []
    for page in crawl:
        print ("HttpCode:%d     Url: %s "%(page.codeHTTP, page.url))

        if page.codeHTTP not in range(200,300):
            dead_urls.append((page.codeHTTP, page.url))

        source_pages = {}
        for url in dead_urls:
            for source_page in crawl.pages_to_be_crawled_dict[url[1]]:
                if source_page in source_pages:
                    if url[0] in source_pages[source_page]:
                        source_pages[source_page][url[0]].append(url[1])
                    else:
                        source_pages[source_page][url[0]] = [url[1]]
                else:
                    source_pages[source_page] = {url[0]: [url[1]]}

    print "\n Crawler Complet!\n"
    with open('liensMort.txt', 'w') as dump_file:
        for source_page in source_pages:
            dump_file.write('Dans la page : \n{}\n'
                        .format(source_page))
            dump_file.write('\n')
            codeHTTP = source_pages[source_page].keys()
            codeHTTP.sort()
            for code in codeHTTP:
                dump_file.write('HTTP return code {}\n'.format(code))
                for url in source_pages[source_page][code]:
                    dump_file.write('        {}\n'.format(url))
            dump_file.write('*'*80 + '\n\n')


if __name__ == '__main__':
    seed_url = 'http://www-sop.inria.fr/members/Arnaud.Legout/'
    page_filter = ['www-sop.inria.fr/members/Arnaud.Legout']
    getPageMorts(seed_url, page_filter)
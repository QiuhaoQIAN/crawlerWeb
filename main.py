#!/usr/bin/env python

from Crawler import *

def getPageMorts(url, pageFilter):
    crawl = Crawler(url, pageFilter=pageFilter)
    urlsMort = []
    for page in crawl:
        print ("HttpCode:%d     Url: %s "%(page.codeHTTP, page.url))

        if page.codeHTTP not in range(200,300):
            urlsMort.append((page.codeHTTP, page.url))
        # a new dictionary to stock the results {url who has the dead liens: [dead liens]}
        pageParents = {}
        for url in urlsMort:
            for pageParent in crawl.pagesToCrawl_dict[url[1]]:
                if pageParent in pageParents:
                    if url[0] in pageParents[pageParent]:
                        pageParents[pageParent][url[0]].append(url[1])
                    else:
                        pageParents[pageParent][url[0]] = [url[1]]
                else:
                    pageParents[pageParent] = {url[0]: [url[1]]}

    print "\n Crawler Complet!\n"
    with open('liensMort.txt', 'w') as dump_file:
        for pageParent in pageParents:
            dump_file.write('Dans la page : \n{}\n'
                        .format(pageParent))
            dump_file.write('\n')
            codeHTTP = pageParents[pageParent].keys()
            codeHTTP.sort()
            for code in codeHTTP:
                dump_file.write('HTTP return code {}\n'.format(code))
                for url in pageParents[pageParent][code]:
                    dump_file.write('        {}\n'.format(url))
            dump_file.write('*'*80 + '\n\n')


if __name__ == '__main__':
    seed_url = 'http://www-sop.inria.fr/members/Arnaud.Legout/'
    pageFilter = ['www-sop.inria.fr/members/Arnaud.Legout']
    getPageMorts(seed_url, pageFilter)
import urllib2
from operator import itemgetter


# Extrait les domaines d'un URL
#Retourne le tuple P qui contient
#   P[0]: URL avec domain
#    P[1]: URL sans protocol
def extract_urls(url):
    protocol_http = 'http://'
    protocol_https = 'https://'
    protocol = ''
    if url.startswith(protocol_http):
        url = url.replace(protocol_http, '')
        protocol = protocol_http
    elif url.startswith(protocol_https):
        url = url.replace(protocol_https, '')
        protocol = protocol_https
    else:
        return ''
    domain = url[:url.find('/')]
    return (protocol + domain, domain)

#test the url is related to a page of HTML
def isHTMLPage(url):
    if url.endswith('/'):
        return True
    else:
        urlTokens = url.split('/')
        if '.' not in urlTokens[-1]:
            return True
        elif ('html' in urlTokens[-1].lower() or
              'htm' in urlTokens[-1].lower()):
            return True
        else:
            return False
# un class pour la page HTML
class HTMLPage(object):
    def __init__(self, url):
        """
        Constructeur de la classe.
        L'objet a 4 attributs:
        url: l'URL qui correspond a la page Web
        _html_it: un iterateur qui parcourt le code HTML, une ligne
                   a la fois
        urls: la liste de toutes les URLs contenues dans la page
        codeHTTP: le code retourne par le protocol HTTP lors de
                    l'acces a la page
                    0 signifie une erreur dans l'URL,
                    -1 signifie que le site de repond pas
                    -2 signifie une exception en accedant
                    a l'URL
        """
        self.codeHTTP = 0
        self.url = url
        self._html_it = self.pageReturn(self.url)
        self.urls = self.extract_urls_from_page()

    # Retourner un page en fonction de URL
    def pageReturn(self, url):
        # surcharge la classe Request pour faire des requetes HEAD qui
        # pemettent de collecter que l'entete de la page. C'est utile
        # lorsque la page ne contient pas de code HTML et donc pas
        # d'URL.  On peut ainsi obtenir un code HTTP sans avoir besoin
        # de telecharger toute la page.
        class HeadRequest(urllib2.Request):
            def get_method(self):
                return "HEAD"

        try:
            if isHTMLPage(url):
                page = urllib2.urlopen(url)
            else:
                page = urllib2.urlopen(HeadRequest(url))
            self.codeHTTP = page.getcode()
            return page
        except urllib2.HTTPError as e:
            self.codeHTTP = e.code
            return []

        except urllib2.URLError as e:
            self.codeHTTP = -1
            return []
        except Exception as e:
            self.codeHTTP = -2
            return []

    def extract_urls_from_page(self):
        """
        Construit la liste de toutes les URLs contenues dans le corps de
        la page HTML en parcourant l'iterateur retourne par
        pageReturn()

        On identifie une URL parce qu'elle est precedee de href= et
        dans le corps (body) de la page. Le parsing que l'on implement
        est imparfait, mais un vrai parsing intelligent demanderait
        une analyse syntaxique trop complexe pour nos besoins.

        Plus en details, notre parsing consiste a chercher dans le
        corps de la page (body):

        -les urls contenues dans le champ href (essentiellement on
         cherche le tag 'href=' et on extrait ce qui est entre
         guillemets ou apostrophes)

        -on ne garde ensuite que les urls qui commencent par http ou
         https et

             * les urls qui commencent par ./ auxquelles on ajoute
          devant (a la place du point) l'Url de la page d'origine
          (self.url) exemple : pour './ma_page.html' et self.url =
          http://mon_site.fr/rep1/ on obtient l'url
          http://mon_site.fr/rep1/ma_page.html

            * les urls qui commencent par /ma_page.html auxquelles on
           ajoute devant uniquement le hostname de la page d'origine
           (self.url) exemple : pour '/ma_page.html' et self.url =
           http://mon_site.fr/rep1/ on obtient l'url
           http://mon_site.fr/ma_page.html

        Cette methode retourne la liste des URLs contenues dans la
        page.

        """

        # parse the page to extract all URLs in href field and in the
        # body of the document
        list_urls = []
        is_body = False
        for line in self._html_it:
            # line = line.lower()
            if is_body:
                if "href=" in line.lower():
                    # extract everything between href=" and "> probably
                    # not bullet proof, but should work most of the
                    # time.
                    url_separator = line[line.lower().find('href=') + 5]
                    line = line[line.lower().find('href=') + 6:]
                    line = line[:line.lower().find(url_separator)]
                    list_urls.append(line)
            else:
                # do not end with > in order to deal with arguments
                # without complexe parsing
                if '<body' in line:
                    is_body = True

        # keep only http and https
        filtered_list_urls = [x for x in list_urls
                              if x.lower().startswith('http')
                              or x.lower().startswith('https')]

        # and reconstruct relative links ./
        filtered_list_urls.extend([self.url[:self.url.rfind('/')] + x[1:]
                                   for x in list_urls
                                   if x.startswith('./')])

        # and reconstruct relative links /
        filtered_list_urls.extend([extract_urls(self.url)[0]
                                   + x for x in list_urls
                                   if x.startswith('/')])

        # debug
        # print [x for x in list_urls if x.startswith('./')]

        return list(set(filtered_list_urls))
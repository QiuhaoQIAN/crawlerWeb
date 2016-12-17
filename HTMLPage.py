import urllib2

# Extrait les domaines d'un URL
#Retourne le tuple P qui contient
#   P[0]: URL avec domain
#    P[1]: URL sans protocol
def extract_urls(url):
    protocolHTTP = 'http://'
    protocolHTTPs = 'https://'
    protocol = ''
    if url.startswith(protocolHTTP):
        url = url.replace(protocolHTTP, '')
        protocol = protocolHTTP
    elif url.startswith(protocolHTTPs):
        url = url.replace(protocolHTTPs, '')
        protocol = protocolHTTPs
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
        # Http code 0:Url not right -1:no reponse from the site  -2: exception
        self.codeHTTP = 0
        
        # url courant
        self.url = url
        
        # the html Code of this page
        self.pageHtml = self.pageReturn(self.url)
        
        # toutes les URLs dans le page courant
        self.urls = self.getUrls()

    # Retourner un page en fonction de URL
    def pageReturn(self, url):
        # surcharge of Request, if not a HTML page, we just get the head
        # use later
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

    def getUrls(self):
        # Cette methode retourne la liste des URLs contenues dans la page.
        listUrls = []
        finalListUrls = []
        isBody = False
        for line in self.pageHtml:
            if isBody:
                if "href=" in line.lower():
                    # separator may be ' or "
                    separator = line[line.lower().find('href=') + 5]
                    line = line[line.lower().find('href=') + 6:]
                    line = line[:line.lower().find(separator)]
                    listUrls.append(line)
            else:
                # where the body begins
                if '<body' in line:
                    isBody = True

        for url in listUrls:
            if (url.lower().startswith('http') or url.lower().startswith('https')):
                finalListUrls.append(url)
            elif url.startswith('./'):
                finalListUrls.append(self.url[:self.url.rfind('/')] + url[1:])
            elif url.startswith('/'):
                finalListUrls.append(extract_urls(self.url)[0] + url[1:])

        return list(set(finalListUrls))


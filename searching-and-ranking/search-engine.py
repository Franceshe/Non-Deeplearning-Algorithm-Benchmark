class cralwer:
    #Initialize the crawler with the name of database#
    def __init__(self, dbname):
        pass

    def __del__(self):
        pass

    def dbcommit(self):
        pass

    #Auxilirary func for getting an entry id and adding#
    #it if it is not present#
    def getentryid(self, table, field, value, createnew=True):
        return None

    # Index an indivisual page
    def addtoindex(self, url, soup):
        print('Indexing %s' % url)

    # Extract the text from HTML page (NO TAG)
    def gettextonly(self, soup):
        return None

    # Seperate the text words by non-whitespace character
    def Seperatewords(self, text):
        return None

    # Return true if this url is already indexed
    def isindexed(self, url):
        return False

    # Add a link between two pages
    def addlinkref(self, urlFrom, urlTo, linkText):
        pass


    # Starting with a list of pages
    # Do a breadth first search to the given depth,
    # indexing pages as we go
    def crawl(self, pages, depth=2):
        pass

    # Create the database table
    def Createindextables(self):
        pass

    



    

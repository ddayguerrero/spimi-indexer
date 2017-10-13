from bs4 import BeautifulSoup
import os

# Reuters21578 Preprocessing
class ReutersCorpus:
    BASEPATH = "reuters21578/"
    REUTERS_FILES = ["reut2-000.sgm"]
    # REUTERS_FILES = ["reut2-000.sgm", "reut2-001.sgm", "reut2-002.sgm", "reut2-003.sgm",
    #                  "reut2-004.sgm", "reut2-005.sgm", "reut2-006.sgm", "reut2-007.sgm",
    #                  "reut2-008.sgm", "reut2-009.sgm", "reut2-010.sgm", "reut2-011.sgm",
    #                  "reut2-012.sgm", "reut2-013.sgm", "reut2-014.sgm", "reut2-015.sgm",
    #                  "reut2-016.sgm", "reut2-017.sgm", "reut2-018.sgm", "reut2-019.sgm",
    #                  "reut2-020.sgm", "reut2-021.sgm"]

    def retrieveDocuments(self):
        """ Extract text from <TITLE> and <BODY> tags of Reuters Files"""
        documents = {}
        for reuter in self.REUTERS_FILES:
            print(reuter)
            reuter_stream = open(self.BASEPATH + reuter, encoding="latin-1")
            reuter_content = reuter_stream.read()
            soup = BeautifulSoup(reuter_content, "html.parser")
            articles = soup.find_all('reuters')
            for article in articles:
                newid = article['newid']
                if not  article.title is None:
                    title = article.title.string
                if not  article.body is None:
                    body = article.body.string
                words = title + " " + body
                documents[newid] = words
        print(f"Retrieval Complete! - Total Documents: {len(documents)}")
        return documents

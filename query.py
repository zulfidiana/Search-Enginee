from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from string import punctuation
import sys, re, time

# untuk search query
class Search:
    stemmer = StemmerFactory().create_stemmer()
    stopword = StopWordRemoverFactory().create_stop_word_remover()
    dictionary = {}

# method constructor
    def __init__(self):
        filescore = open('score.txt', 'r')
        lines = filescore.readlines()

        for line in lines:
            part = line.split(' :: ')
            term = part[0]
            self.dictionary[term] = {}
            weight_terms = part[1].split()
            for weight in weight_terms:
                doc, w = weight.split(':')
                self.dictionary[term][doc] = float(w)

# method untuk mendapatkan title
    def get_title(self, text):
        return re.search('<title>(.*?)</title>', text).group(1)

# method untuk mendapatkan url
    def get_url(self, text):
        return re.search('<url>(.*?)</url>', text).group(1)

# method untuk mengambil isi artikel
    def get_content(self, tags, text):
        result = ''
        for tag in tags:
            try:
                result += re.search(f'<{tag}>(.*?)</{tag}>', text).group(1) + ' '
            except AttributeError:
                result += str(re.search(f'<{tag}>(.*?)</{tag}>', text)) + ' '
        return result

# method untuk mencari query
    def search(self, query, total):
        query = query.translate(str.maketrans('','', punctuation))
        query = self.stopword.remove(query)
        query_terms = self.stemmer.stem(query.lower()).split()
        result = {}
        article = []

        # start = time.time()

# untuk mencari dokumen berdasarkan query yg di input
        for term in query_terms:
            if term in self.dictionary.keys():
                for doc in self.dictionary[term].keys():
                    if doc not in result.keys():
                        result[doc] = float(self.dictionary[term][doc])
                    else:
                        result[doc] +=  float(self.dictionary[term][doc])

        sorted_result = sorted(result.items(), key=lambda x:x[1], reverse=True)

# untuk membaca dokumen yg sudah sebelumnya
        for doc, w in sorted_result[:total]:
            if doc.startswith('scrviva'):
                dir_path = 'Clean/VIVA/'+doc
            elif doc.startswith('kompas'):
                dir_path = 'Clean/KOMPAS/'+doc
            else:
                dir_path = 'Clean/LIPUTAN6/'+doc

            document = open(dir_path, 'r', encoding='utf-8').read()
            # article.append(document)
            article.append({
                'title': self.get_title(document),
                'url': self.get_url(document),
                'content': self.get_content(['top', 'middle', 'bottom'], document)[:200].lstrip() + '...'
            })
            # self.article[doc] = {}
            # self.article[doc]['title'] = self.get_title(document)
            # self.article[doc]['url'] = self.get_url(document)
            # self.article[doc]['content'] = self.get_content(['top', 'middle', 'bottom'], document)[:200].lstrip() + '...'
            
        # finish = time.time()
        
        return article

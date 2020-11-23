class DocumentClass(Document):
    def __init__(self, vocabulary):
        Document.__init__(self, vocabulary)
        self._number_of_docs = 0

    def Probability(self,word):
        """ returns the probabilty of the word "word" given the class "self" """
        voc_len = Document._vocabulary.len()
        SumN = 0
        for i in range(voc_len):
            SumN = DocumentClass._vocabulary.WordFreq(word)
        N = self._words_and_freq.WordFreq(word)
        erg = 1 + N
        erg /= voc_len + SumN
        return erg

    def __add__(self,other):
        """ Overloading the "+" operator. Adding two DocumentClass objects consists in adding the 
        BagOfWords of the DocumentClass objectss """
        res = DocumentClass(self._vocabulary)
        res._words_and_freq = self._words_and_freq + other._words_and_freq 
 
        return res

    def SetNumberOfDocs(self, number):
        self._number_of_docs = number
    
    def NumberOfDocuments(self):
        return self._number_of_docs
import gensim.downloader as api
import spacy
nlp = spacy.load("en_core_web_lg")

# Download a pre-trained Word2Vec model (you can choose a different one if needed)
word2vec_model = api.load("word2vec-google-news-300")


class TextPreprocessor:
    
    def __init__(self, nlp = nlp, model = word2vec_model, filepath = None, text = None):
        
        if filepath is None and text is None:
            raise Exception("Must pass in text via either a filepath to open or a text string")
        elif filepath is not None and text is not None:
            raise Exception("Both filepath and text string cannot be passed in")
        elif filepath:
            self.filepath = filepath
            self.data = self.open_file()
        elif text:
            self.data = text
            
        if not model: 
            print("Loading model")
            self.model = api.load("word2vec-google-news-300")
        else: 
            self.model = model
            
        import spacy
        
        self.sentences = self.tokenize_text(self.data)
        self.sentences_to_vectors()
    
    def open_file(self) -> str:
        
        with open(self.filepath) as f: 
            data = f.read()
            
        return data
    
    def tokenize_text(self, text:str) -> list[str]:
        from nltk.tokenize import sent_tokenize

        # Tokenizes input text string to a list of sentences.
        sentences = sent_tokenize(text) 
        
        # Takes only sentences that are not in table of contents (has '....' in the line) or are too short to be useful
        # Reducing the list and removing garbage improves performance because it reduces the matrix space of the vector comparisons
        sentences = [s.strip() for s in sentences if ('....' not in s) & (len(s) > 10) & ('___' not in s) & ('====' not in s)]
        
        return sentences
    
    def sentences_to_vectors(self):
        self.sentence_word_vectors = [self.calculate_sentence_vector(sentence) for sentence in self.sentences]
    
    def preprocess_text(self, text:str):
        '''
        
        '''

        doc = nlp(text)
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
        return tokens
    
    def calculate_sentence_vector(self, sentence:str) -> float:
        '''
        
        '''
        
        tokens = self.preprocess_text(sentence)
        vectors = [self.model[word] for word in tokens if word in self.model]

        if not vectors:
            return None  # Return None if none of the words are in the model

        # Average the word vectors to get the sentence vector
        sentence_vector = sum(vectors) / len(vectors)

        return sentence_vector

class VA:
    
    def __init__(self, filepath, model = word2vec_model): 
        self.filepath = filepath
        self.model = model
        self.process_doc()
        
    def process_doc(self):
        proc = TextPreprocessor(model = self.model, filepath = self.filepath)
        self.doc_sentences = proc.sentences
        self.doc_vec = proc.sentence_word_vectors
        
    def query(self, q):
        
        q_proc = TextPreprocessor(model = self.model, text= q)
        import numpy as np
        array1 = q_proc.sentence_word_vectors[0]
        self.cos_vectors = [self.cosine_similarity(array1, vector) for vector in self.doc_vec]
        
    def sort_results(self): 
        import pandas as pd

        data = {
            "sentences": self.doc_sentences,
            "cos_similarity": self.cos_vectors
        }
        df = pd.DataFrame(data)

        df_sort = df.sort_values('cos_similarity', ascending=False).reset_index(drop=True)

        self.top_r = df_sort.sentences[:10]
        
    def cosine_similarity(self, array1, array2):
        import numpy as np
        from numpy.linalg import norm

        try:
            # Calculate the dot product of the two arrays
            dot_product = np.dot(array1, array2)

            # Calculate the L2 norms (Euclidean norms) of both arrays
            norm_array1 = norm(array1)
            norm_array2 = norm(array2)

            # Calculate the cosine similarity
            return dot_product / (norm_array1 * norm_array2)
        except: 
            return 0.
from clir.QueryMetrics import QueryMetrics

import faiss
import ir_datasets
import numpy as np
import pickle
import spacy

class ForeignDocumentsIndex:

    def __init__(self):
        self.language = None
        self.nlp = None
        self.foreign_doc_titles = []
        self.queries = None
        self.faiss_index = None

    # ex. ForeignDocumentsIndex(nlp_language="ru_core_news_sm", neuclir_docs="neuclir/1/ru/hc4-filtered", docs_limit=50)
    @staticmethod
    def create_index(nlp_language, neuclir_docs, docs_limit=None, relevant_docs=None, language="ru"):
        fd_index = ForeignDocumentsIndex()
        fd_index.language = language

        print("Creating index...")

        # First get all the foreign-language documents and vectorize them
        # When finished we will have a list of vectors for each document and a list of titles, which will be our
        # indexes' metadata
        fd_index.nlp = spacy.load(nlp_language)
        foreign_docs = ir_datasets.load(neuclir_docs)
        foreign_doc_vectors = []
        fd_index.foreign_doc_titles = []
        fd_index.queries = foreign_docs.queries_iter()
        added_doc_ids = []

        i = 1
        if docs_limit:
            for foreign_doc in foreign_docs.docs_iter()[:docs_limit]:
                added_doc_ids.append(foreign_doc[0])
                fd_index.foreign_doc_titles.append(foreign_doc[1])
                foreign_doc_vectors.append(fd_index.nlp(foreign_doc[1] + " " + foreign_doc[2]).vector)
                if i % 100 == 0:
                    print(f"Processing document {i}/{docs_limit}")
                i += 1
        else:
            for foreign_doc in foreign_docs.docs_iter()[:docs_limit]:
                added_doc_ids.append(foreign_doc[0])
                fd_index.foreign_doc_titles.append(foreign_doc[1])
                foreign_doc_vectors.append(fd_index.nlp(foreign_doc[1] + " " + foreign_doc[2]).vector)
                if i % 100 == 0:
                    print(f"Processing document {i}/{foreign_docs.docs_count()}")
                i += 1

        # Now create an FAISS index and add the vectors to it
        fd_index.faiss_index = faiss.IndexFlat(foreign_doc_vectors[0].shape[0])
        fd_index.faiss_index.add(np.array(foreign_doc_vectors))

        # Now if we have any relevant docs that weren't in the group already added, add them
        print("Adding additional relevant docs...")
        doc_store = foreign_docs.docs_store()
        docs_to_add = []
        docs_to_add_vectors = []
        for relevant_doc in relevant_docs:
            if relevant_doc not in added_doc_ids:
                docs_to_add.append(relevant_doc)
        for d in doc_store.get_many_iter(docs_to_add):
            fd_index.foreign_doc_titles.append(d[1])
            docs_to_add_vectors.append(fd_index.nlp(d[2]).vector)
        fd_index.faiss_index.add(np.array(docs_to_add_vectors))
        print("Additional relevant docs added")

        print("FAISS index created")
        return fd_index

    # Saves the index locally so that we can load it in the future
    def save_index(self, faiss_path, metadata_path):
        faiss.write_index(self.faiss_index, faiss_path)
        pickle_dict = {
            "metadata": self.foreign_doc_titles,
            "nlp": self.nlp,
            "language": self.language
        }
        with open(metadata_path, "wb") as f:
            pickle.dump(pickle_dict, f)

    # Loads the index from a local location so that we dont have to rebuild it
    @staticmethod
    def load_index(faiss_path, metadata_path):
        fd_index = ForeignDocumentsIndex()
        fd_index.faiss_index = faiss.read_index(faiss_path)
        with open(metadata_path, "rb") as file:
            data = pickle.load(file)
        fd_index.foreign_doc_titles = data["metadata"]
        fd_index.nlp = data["nlp"]
        fd_index.language = data["language"]
        return fd_index

    # Returns the K-nearest results in the index for the query
    # Returns 2-tuple (distance, article title)
    def search_index(self, query, k=5):
        query_vector = self.nlp(query).vector
        distances, found_indexes = self.faiss_index.search(np.array([query_vector]), k)
        results = []
        for i in range(0, len(found_indexes[0])):
            found_index = found_indexes[0][i]
            distance = distances[0][i]
            results.append((distance, self.foreign_doc_titles[found_index]))
        return results

if __name__ == "__main__":

    # Create the index from scratch, comment out if we are using an existing one
    qm = QueryMetrics.create_relevance_maps("neuclir/1/ru/hc4-filtered")
    index = ForeignDocumentsIndex.create_index(nlp_language="ru_core_news_lg",
                                               neuclir_docs="neuclir/1/ru/hc4-filtered",
                                               docs_limit=10000,
                                               relevant_docs=qm.relevant_doc_ids,
                                               language="ru")
    index.save_index("../storage/ru_index", "../storage/ru_metadata")

    # Now try a query vector = вирус ("virus") and confirm results
    query = "вирус"
    print(f"Searching {query}")
    for r in index.search_index(query):
        print(r)

    # Now try another query = Плавленный сыр ("Processed cheese") and confirm results
    query = "Плавленный сыр"
    print(f"Searching {query}")
    for r in index.search_index(query):
        print(r)

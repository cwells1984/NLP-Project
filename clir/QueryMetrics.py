from clir.QueryTranslator import QueryTranslator

import ir_datasets
import pickle

class QueryMetrics:
    def __init__(self):
        self.query_titles = []
        self.relevant_doc_ids = set()
        self.ht_query_titles = []
        self.query_to_rel1_docs = {}
        self.query_to_rel3_docs = {}

    @staticmethod
    def get_doc_title(datastore, doc_id):
        try:
            test = datastore.get(doc_id)
            print(test)
        except KeyError:
            print(f"Unable to find {doc_id}")

    @staticmethod
    def create_relevance_maps(neuclir_docs):
        qm = QueryMetrics()

        foreign_docs = ir_datasets.load(neuclir_docs)
        foreign_docs_store = foreign_docs.docs_store()

        query_id_rel1_doc_ids = {}
        query_id_rel3_doc_ids = {}

        # First get a Query ID -> Query Title mapping
        query_id_to_title = {}
        for q in foreign_docs.queries_iter():
            qm.query_titles.append(q[1])
            qm.ht_query_titles.append(q[3])
            query_id_to_title[q[0]] = q[1]

        # Create maps of query ids to somewhat valuable (relevance=1) and very valuable (relevance=3) doc ids
        for qrel in foreign_docs.qrels_iter():
            query_id = qrel[0]
            doc_id = qrel[1]
            relevance = qrel[2]

            if relevance == 1:
                if query_id in query_id_rel1_doc_ids:
                    query_id_rel1_doc_ids[query_id].append(doc_id)
                    qm.relevant_doc_ids.add(doc_id)
                else:
                    query_id_rel1_doc_ids[query_id] = [doc_id]
                    qm.relevant_doc_ids.add(doc_id)

            if relevance == 3:
                if query_id in query_id_rel3_doc_ids:
                    query_id_rel3_doc_ids[query_id].append(doc_id)
                    qm.relevant_doc_ids.add(doc_id)
                else:
                    query_id_rel3_doc_ids[query_id] = [doc_id]
                    qm.relevant_doc_ids.add(doc_id)

        # Finally combine these into Query Title -> Document Titles maps
        for k in query_id_rel1_doc_ids.keys():
            doc_ids = query_id_rel1_doc_ids[k]
            query_title = query_id_to_title[k]
            title_list = [i.title for i in foreign_docs_store.get_many_iter(doc_ids)]
            qm.query_to_rel1_docs[query_title] = title_list
        for k in query_id_rel3_doc_ids.keys():
            doc_ids = query_id_rel3_doc_ids[k]
            query_title = query_id_to_title[k]
            title_list = [i.title for i in foreign_docs_store.get_many_iter(doc_ids)]
            qm.query_to_rel3_docs[query_title] = title_list

        # Now show the relevant docs
        for k in query_id_to_title.keys():
            query_title = query_id_to_title[k]
            print(query_title)
            if query_title in qm.query_to_rel3_docs:
                print(qm.query_to_rel3_docs[query_title])
            else:
                print("None")
            if query_title in qm.query_to_rel1_docs:
                print(qm.query_to_rel1_docs[query_title])
            else:
                print("None")
            print("==============================")

        return qm

    def get_query_results(self, translator, faiss_index):

        # For each of our queries:
        for i in range(0, len(self.ht_query_titles)):

            # Get the original english and hand-translated query (the input is our machine-translated query)
            query_title = self.query_titles[i]
            ht_query_title = self.ht_query_titles[i]
            mt_query_title = translator.translate(query_title)

            # Get the relevance 1 and 3 docs associated with this query
            if query_title in self.query_to_rel3_docs:
                rel3_docs = self.query_to_rel3_docs[query_title]
            else:
                rel3_docs = []
            if query_title in self.query_to_rel1_docs:
                rel1_docs = self.query_to_rel1_docs[query_title]
            else:
                rel1_docs = []

            # Now search the index
            print(f"Searching {query_title} ({ht_query_title})")
            print(f"Searching {query_title} ({mt_query_title})")
            for r in faiss_index.search_index(mt_query_title):
                if r[1] in rel3_docs:
                    print(f"R3 {r[0]} - {r[1]}")
                elif r[1] in rel1_docs:
                    print(f"R1 {r[0]} - {r[1]}")
                else:
                    print(f"R0 {r[0]} - {r[1]}")
            print("===========================")

    def save_metrics(self, query_file):
        pickle_data = {"queries": self.query_titles,
                       "ht_queries": self.ht_query_titles,
                       "relevant_doc_ids": self.relevant_doc_ids,
                       "rel1": self.query_to_rel1_docs,
                       "rel3": self.query_to_rel3_docs}
        with open(query_file, "wb") as f:
            pickle.dump(pickle_data, f)

    @staticmethod
    def load_metrics(query_file):
        qm = QueryMetrics()
        with open(query_file, "rb") as f:
            data = pickle.load(f)
            qm.query_titles = data["queries"]
            qm.relevant_doc_ids = data["relevant_doc_ids"]
            qm.ht_query_titles = data["ht_queries"]
            qm.query_to_rel1_docs = data["rel1"]
            qm.query_to_rel3_docs = data["rel3"]
        return qm

if __name__ == "__main__":

    # Create the relevance maps from scratch, comment out if we are using an existing one
    qm = QueryMetrics.create_relevance_maps("neuclir/1/ru/hc4-filtered")
    qm.save_metrics("../storage/ru_queries")

    # Load an existing index, comment out if we are building a brand-new one
    qm = QueryMetrics.load_metrics("../storage/ru_queries")

    # Now confirm some of our queries
    print(qm.query_to_rel1_docs["British royal news impacts"])
    print(qm.query_to_rel3_docs["Shipwrecks and Historical European Trade"])
    print(qm.relevant_doc_ids)

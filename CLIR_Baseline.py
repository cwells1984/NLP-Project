from clir.ForeignDocumentsIndex import ForeignDocumentsIndex
from clir.QueryMetrics import QueryMetrics
from clir.QueryTranslator import QueryTranslator

if __name__ == "__main__":
    index = ForeignDocumentsIndex.load_index("storage/ru_index_nostopwords",
                                             "storage/ru_metadata_nostopwords")
    qm = QueryMetrics.load_metrics("storage/ru_queries_nostopwords")
    translator = QueryTranslator("en", index.language)
    qm.get_query_results(translator, index, k=5)

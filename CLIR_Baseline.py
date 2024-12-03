from clir.ForeignDocumentsIndex import ForeignDocumentsIndex
from clir.QueryMetrics import QueryMetrics
from clir.QueryTranslator import QueryTranslator

if __name__ == "__main__":
    index = ForeignDocumentsIndex.load_index("storage/ru_index",
                                             "storage/ru_metadata")
    qm = QueryMetrics.load_metrics("storage/ru_queries")
    translator = QueryTranslator("en", index.language)
    qm.get_query_results(translator, index, k=5)

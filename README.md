Installation

First, install the libraries:<br>
Run `pip install requirements.txt`

To get the spacy language libraries we need for our NLP:<br>
Run `python -m spacy download ru_core_news_sm`
Run `python -m spacy download ru_core_news_lg`

First, create the Foreign language index
Run the main method of `ForeignDocumentsIndex.py` to save the index to the `storage/` directory.

Next, create the Query metrics object
Run the main method of `QueryMetrics.py` to save the object to the `storage/` directory.

Finally, you can run the main method of `CLIR_Test.py` that laods both objects and runs the machine-translated queries.

## Works Cited
NDCG Explained<br>
https://www.deepchecks.com/glossary/normalized-discounted-cumulative-gain/#:~:text=What%20is%20NDCG%3F,systems%2C%20and%20other%20ranking%20algorithms. 

SKLearn NDGC Core<br>
https://scikit-learn.org/dev/modules/generated/sklearn.metrics.ndcg_score.html

spaCy Russian language modules<br>
https://spacy.io/models/ru#ru_core_news_lg

spaCy vector similarity search example<br>
https://www.google.com/search?q=spacy+vector+text+search+python&rlz=1C1MSIM_enUS842US842&oq=spacy+vector+text+search+python&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDQ5NzRqMGo0qAIAsAIB&sourceid=chrome&ie=UTF-8

IR datasets Python API<br>
https://ir-datasets.com/python.html

IR neuCLIR datasets<br>
https://ir-datasets.com/neuclir.html

CLIR metrics<br>
https://www.google.com/search?q=cross+language+information+retrieval+metrics&rlz=1C1MSIM_enUS842US842&oq=cross+language+information+retrieval+metrics&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDYwNjBqMGoxqAIAsAIA&sourceid=chrome&ie=UTF-8

CLIR learning to rank paper<br>
https://www.cs.jhu.edu/~kevinduh/papers/sasaki18letor.pdf

JH Large-Scale CLIR Dataset<br>
https://www.cs.jhu.edu/~kevinduh/a/wikiclir2018/


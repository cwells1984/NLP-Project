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
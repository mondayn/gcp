# gcp


- [rag](https://github.com/mondayn/gcp/blob/main/rag.ipynb): I uploaded some fictious calendar data to a Google data store and then asked a Dialogflow CX agent some questions about it.  I was surprised it understood terms like "bday" as birthday.  At one point it even responded "you should buy a present several days before " their birthday.  To be able to upload tabular data and have an LLM respond with insightful information is exciting.  This reminds me of what we could do with images a few years back, called [transfer learning](https://github.com/mondayn/py/blob/master/transferLearning.ipynb), where you could submit an image to ML trained corpus and it can infer a reasonable next-step conclusion.


- cloud_run_functions: creates a cloud run function that uses python to update a blob

- nlp: Entity recognition analysis of top terms searched on google.com

- gcp_fx: reusable code for cloud storage, pubsub, bigquery
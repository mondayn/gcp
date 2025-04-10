# gcp


- [rag](https://github.com/mondayn/gcp/blob/main/rag.ipynb): I uploaded some fictious calendar data to a Google data store and then asked a Dialogflow CX agent some questions about it.  Surprisingly it understood terms like "bday" as birthday.  At one point it even responded "you should buy a present several days before " their birthday.  To upload new tabular data to an LLM and receive an insightful response is exciting!  It's similiar to what we could do a few years ago with images, called [transfer learning](https://github.com/mondayn/py/blob/master/transferLearning.ipynb), where we could submit an image to an ML trained corpus and the model responds with a good next-step.

- [cloud_run_blob](https://github.com/mondayn/gcp/blob/main/cloud_run_blob.ipynb): uses gen 2 function to update storage

- [cloud_run_postgres](https://github.com/mondayn/gcp/blob/main/cloud_run_postgres.ipynb): cloud run function that feeds pubsub message into postgres

- [dataflow](https://github.com/mondayn/gcp/blob/main/dataflow.ipynb): parse nyc taxi pubsub, stream into big query

- nlp: Entity recognition analysis of top terms searched on google.com

- gcp_fx: reusable code for cloud storage, pubsub, bigquery

- [parse_fhir](https://github.com/mondayn/gcp/blob/main/parse_fhir.ipynb): manually parse sample files from synthea.  better approach would be to load via gcp healthcare api

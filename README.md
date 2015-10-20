# Web Information Retrieval project


Scraping da http://www.beeradvocate.com/ :

.) Considerare le 250 "top beers": http://www.beeradvocate.com/lists/top/ .
.) Considerare le "top beers" per ogni us state: http://www.beeradvocate.com/lists/us/, ...
.) Per ogni birra considerata nei due punti precedenti, scaricare almeno le prime 100 recensioni ordinate per "Top Raters" http://www.beeradvocate.com/beer/profile/23222/78820/?sort=topr&start=0 .

.) Creare per ogni birra un profilo dato dall'aggregazione delle caratteristiche: "look", "smell", "taste", "feel" e "overall".

.) Effettuare clustering di tutto il dataset.
.) Effettuare ranking, prendendo in input la lista di attributi da considerare.
.) Data una birra in input e la lista di attributi da considerare, produrre in output le Top-10 e Bottom-10 birre più simili alla birra in input, considerando solo gli attributi inseriti.


Formato Dataset:


Esempio di JSON:

```json

[	
	{	
		"position" : "1",
		"name" : "Heineken",
		"brewer" : "Heineken",
		"ba_score" : "90",
		"num_rev" : "100",
		"hads" : "20",
		"avg" : "4.9",
		"pDev" : "+0.3",
		"state" : "Netherlands",
		"style" : "Lager",
		"abv" : "4.7",
		"reviews": [
			{
				"rate" : "5",
				"rDev" : "5",
				"look" : "5",
				"smell" : "5",
				"taste" : "5",
				"feel" : "5",
				"overall" : "5",
				"text" : "Sounds good.",
				"reviewer" : "me"
			},
			{
				"rate" : "1",
				"rDev" : "1",
				"look" : "1",
				"smell" : "1",
				"taste" : "1",
				"feel" : "1",
				"overall" : "1",
				"text" : "Sounds bad.",
				"reviewer": "not me"
			}
		]
	}

]
```
Guida all'uso:
- lanciare wir-downloader.py per scaricare gli html dal sito
- lanciare wir-parser.py per ottenere il dataset JSON definitivo

Per effettuare clustering, ranking e top-bottom 10:
- lanciare wir-avg.py per convertire il dataset in un formato numerico
- lanciare wir-clusterer.py per effettuare DBScan Clustering e Agglomerative Clustering
- lanciare wir-ranking.py per avere un ranking generale in base alle caratteristiche, wir-top-bottom.py per avere una classifica delle dieci birre più e meno simili ad una data birra in input

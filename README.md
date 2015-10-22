# Web Information Retrieval project

Guida all'uso degli script python:
- lanciare wir-downloader.py per scaricare gli html dal sito, specificando in input quale set di birre si vuole scaricare, la classifica "top-us" degli USA, le classifiche "top-states" dei singoli stati americani o le migliori "top-250" in assoluto. (> python wir-downloader.py [top-us|top-states|top-250] )
- lanciare wir-parser.py per ottenere il dataset JSON definitivo, specificare anche in questo caso di quale dataset si vuole il parsing in JSON (> python wir-parser.py [top-us|top-states|top-250] )

Per effettuare clustering, ranking e top-bottom 10:
- lanciare:  >wir-avg.py ["top-us"|"top-states"|"top-250"] per convertire il dataset in un formato numerico. Questo step è necessario per eseguire clusterer, ranking e top-bottom.
- lanciare:  >wir-clusterer.py ["top-us"|"top-250"] [epsilon] [minSamples] per effettuare DBScan Clustering e Agglomerative Clustering, epsilon e minSamples sono necessari per il DBScan e richiesti all'utente come input.
- lanciare:  >wir-ranking.py ["us"|sigla_stato] [caratteristiche] per avere un ranking generale in base alle caratteristiche, se non si specificano input, verrà fatto ranking sulle top-250 considerando il voto generale (overall)
- lanciare:  >wir-top-bottom.py ["us"|sigla_stato][nome_birra][caratteristiche] per avere una classifica delle dieci birre più e meno simili ad una data birra in input

Le caratteristiche selezionabili sono: "look", "smell", "taste", "feel" e "overall".


Richieste progettuali:

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
				"reviewer" : "me",
				"reviewerScore" : 100
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
				"reviewer": "not me",
				"reviewerScore" : "24"
			}
		]
	}

]
```

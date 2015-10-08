# wir-project

Direi di utilizzare http://www.beeradvocate.com/ e lavorare in questo modo:

.) Considerare le 250 "top beers": http://www.beeradvocate.com/lists/top/ .
.) Considerare le "top beers" per ogni us state: http://www.beeradvocate.com/lists/us/, ...
.) Per ogni birra considerata nei due punti precedenti, scaricare almeno le prime 100 recensioni ordinate per "Top Raters" http://www.beeradvocate.com/beer/profile/23222/78820/?sort=topr&start=0 .

.) Creare per ogni birra un profilo dato dall'aggregazione delle caratteristiche: "look", "smell", "taste", "feel" e "overall".

.) Effettuare clustering di tutto il dataset.
.) Effettuare ranking, prendendo in input la lista di attributi da considerare.
.) Data una birra in input e la lista di attributi da considerare, produrre in output le Top-10 e Bottom-10 birre più simili alla birra in input, considerando solo gli attributi inseriti.
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

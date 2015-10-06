# wir-project

Direi di utilizzare http://www.beeradvocate.com/ e lavorare in questo modo:

.) Considerare le 250 "top beers": http://www.beeradvocate.com/lists/top/ .
.) Considerare le "top beers" per ogni us state: http://www.beeradvocate.com/lists/us/, ...
.) Per ogni birra considerata nei due punti precedenti, scaricare almeno le prime 100 recensioni ordinate per "Top Raters" http://www.beeradvocate.com/beer/profile/23222/78820/?sort=topr&start=0 .

.) Creare per ogni birra un profilo dato dall'aggregazione delle caratteristiche: "look", "smell", "taste", "feel" e "overall".

.) Effettuare clustering di tutto il dataset.
.) Effettuare ranking, prendendo in input la lista di attributi da considerare.
.) Data una birra in input e la lista di attributi da considerare, produrre in output le Top-10 e Bottom-10 birre più simili alla birra in input, considerando solo gli attributi inseriti.

Beers.json:
[
	{
		position:
		nome:
		birrificio:
		ba_score:
		reviews:
		hads:
		avg:
		pDev:
		state:
		style:
		abv:
		reviews: [
			{
				rate:
				rDev:
				look:
				smell:
				taste:
				feel:
				overall:
				text:
				reviewer:
				date:
			},
			{
				...
			}
		]
	},
	{
		...
	}
]

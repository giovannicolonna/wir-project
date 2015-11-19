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

##11th point
top 10 per un gruppo di 20 persone


che vanno bene a un gruppo di persone, non a una persona sola.
si risolve in una festa - party - per tutti
ognuno ha gusti diversi, ora abbiamo sto gruppo di 20 persone quindi cardinalità = 20
prendiamo 20 profili a caso , dobbiamo fare f obiettivo = guarda questa birra fa tanto felice il 

gruppo

se invece ne abbiamo due, ci sono 3 tipi di f.ob utilizzate:
- massimizzare (la media) delle somma delle singole soddisfazioni

- problema, sensibile agli outliers. ora il minimo va tenuto in considerazione. soddisfiamo il più 

prossibile la persona meno soddisfatta

- cerca di aggiustare la metrica, considerando anche la standard deviation. cerchiamo di massimizzare 

il grado di equità all'interno (fairness) avg + 1/2*std dove 1/2 = lambda

(ELIMINAZIONE DEGLI OUTLIERS) = non generiamo persone molto insoddisfatte

- mix = sum + 0.5min 

ci fa comodo tenere outliers molto soddisfatti! 



passiamo OGNI birra sotto ognuna delle 4 funzioni obiettivo.

proviamo questo per 100 gruppi da 20 persone (scelte a caso), calcoliamo ognuna delle 4 f.o. per ogni 

gruppo e ne estraiamo le top 10.

- inviargli i dati per posta.


DUE GRUPPI DI CUI ABBIAMO CALCOLATO LE TOP 10 PER LE 4 DIVERSE F.O. discutendo i risultati di ogni 

f.o. (tenendo conto di gruppi in cui si vede la reale differenza degli algoritmi)


una slide divisa in due orizzontalmente in cui la prima parte e la seconda due gruppi con tabella
top10 con sum
top10 con min 
ecc...
(descrizione funz obiettivo non necessaria)



hashtag (parole più diffuse per città relative all'hashtag----capire la città dall'hashtag)

__author__ = 'gio'


### ESEGUE CLUSTERING PARTENDO DAL DATASET IN .TSV

## necessita l'installazione di "numpy"
## necessita l'installazione di "sklearn"
## necessita l'installazione di "scipy"

import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics


### STEP 1:
## Costruisce una matrice di float a partire da un file tsv <nomebirra><tab><arraydimedie> ottenuto dall'esecuzione di avg-us.py
## INPUT: tsv file ottenuto da avg-us.py
## OUTPUT: X, una matrice di float |beers|x|features| della classe numpy.array
##        true_labels, un array di interi della classe numpy.array che fungono da etichette iniziali del clustering
## NOTE: i nomi delle birre non vengono mantenuti nella matrice X

INPUTFILE = "top-us" #si puo' scegliere tra "top-us" o "top250"

f = open(INPUTFILE+"-vectorialized.tsv",'r')
x = []
true_labels = []  # non mi e' chiaro lo scopo, dev'essere composto da numeri che vanno da 2 a num.birre-1 per dare
# un iniziale labeling dei punti, viene assegnato a ogni punto un'etichetta compresa tra 0 e 7
i = 0
for line in csv.reader(f,delimiter='\t'):
    currentVector = []
    first = True
    for elem in line:
        if first:
            first = False
            continue  # ignoriamo il nome della birra e prendiamo solo le medie
        currentVector.append(elem)
    x.append(currentVector)
    true_labels.append(i)
    i += 1
    if i > 7:  # etichettiamo inizialmente ogni birra con un numero da 0 a 7
        i = 0
f.close()

X = np.array(x)  # convertiamo la matrice X e l'array true_labels nel formato numpy.array richiesto per DBScan
true_labels = np.array(true_labels)
print "Beer matrix:\n"
print X  # stampa matrice delle birre
print '\n\n'


## Step 2: DB SCAN clustering

## Esegue l'algoritmo di clustering DBScan. DBScan clusterizza in base alla densita' del dataset.
## Un gruppo di punti sufficientemente denso viene inserito in un cluster.
##  Ref: http://scikit-learn.org/stable/modules/clustering.html#dbscan

## ATTENZIONE: non e' detto che ogni punto venga clusterizzato, DBScan considera rumore tutto cio' che non e' abbastanza
## denso. La densita' e' definita in questo modo:

## Un CORE-SAMPLE e' un punto che ha almeno MIN_SAMPLES punti a distanza minore o uguale di EPSILON
## Un cluster viene ottenuto ricorsivamente: dato un CORE-SAMPLE, si cerca tra i suoi vicini chi a sua volta e' un CORE-SAMPLE
## e cosi' via... quando l'insieme dei core-samples e' terminato, viene colorato il cluster

## I parametri da settare sono EPSILON e MIN_SAMPLES:
## EPSILON = definisce la distanza entro cui un punto e' un vicino di un altro punto
## MIN_SAMPLES = numero minimo di punti vicini necessari per rendere un punto CORE-SAMPLE

## spero di essere stato chiaro :)

EPSILON = 0.116
MIN_SAMPLES = 6
db = DBSCAN(EPSILON,MIN_SAMPLES,metric='euclidean',p=None,random_state=None).fit(X)
labels = db.labels_

print "Initial labels:\n"
print true_labels
print "\n"
print "Label set after DBScan:\n"
print labels
print "\n"

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

## Statistiche strane:
print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(true_labels,labels))
print("Completeness: %0.3f" % metrics.completeness_score(true_labels, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(true_labels, labels))
print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(true_labels, labels))
print("Adjusted Mutual Information: %0.3f" % metrics.adjusted_mutual_info_score(true_labels, labels))
try:
    ## Attenzione, se non ci sono core-samples, quindi non ci sono clusters, qua lancia un'eccezione
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))
except:
    print("\nWARNING: DBScan has not found any clustering. Re-tune the parameters.\n")
print("\n\n")

## Step 3: Plotting
## Disegna il risultato del clustering, il codice e' della demo
## Attenzione, se DBScan clusterizza in un unico cluster (non fa clustering), genera un'eccezione in fase di disegno


# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()


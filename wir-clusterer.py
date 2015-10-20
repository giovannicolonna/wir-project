__author__ = 'gio'

import csv
import numpy as np
import logging
import sys
from collections import defaultdict
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn import metrics
from sklearn.datasets.samples_generator import make_swiss_roll

logging.basicConfig(filename='clustering.log',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y/%m/%d %H:%M',
                    filemode='w',
                    level=logging.DEBUG)

### STEP 1:
## Costruisce una matrice di float a partire da un file tsv <nomebirra><tab><arraydimedie> ottenuto dall'esecuzione di wir-avg.py
## INPUT: tsv file ottenuto da wir-avg.py
## OUTPUT: X, una matrice di float |beers|x|features| della classe numpy.array
##        true_labels, un array di interi della classe numpy.array che fungono da etichette iniziali del clustering
## NOTE: i nomi delle birre non vengono mantenuti nella matrice X

try:
    INPUTFILE = sys.argv[1]
    if not (INPUTFILE == "top-250" or INPUTFILE == "top-us"):
        print "Input format error: 'top-250' or 'top-us' is requested"
        logging.error("Input format error: 'top-250' or 'top-us' is requested")
        exit(1)
    logging.info("Dataset used: " + str(INPUTFILE))
except IndexError:
    INPUTFILE = "top-250"
    logging.info("No dataset chosen: top-250 as default")

names = []
positions = []
logging.debug("Clustering on: "+INPUTFILE+'\n')
f = open(INPUTFILE+"-vectorialized.tsv", 'r')
o = open("Clustering_output.txt", 'w')

x = []
initial_labels = []
i = 0
for line in csv.reader(f, delimiter='\t'):
    currentVector = []  # is needed for build X
    first = True
    counter = 0
    for elem in line:
        if counter == len(line)-1:
            # last iteration, take the position
            positions.append(elem)
            continue
        if first:
            first = False
            names.append(elem)
            counter += 1
            continue  # ignoring beer name, retrieving only average scores
        currentVector.append(elem)
        counter += 1

    x.append(currentVector)
    initial_labels.append(i)
    i += 1

f.close()

X = np.array(x)  # converting matrix X and true_labels array in format numpy.array required by DBScan
initial_labels = np.array(initial_labels)

logging.debug("Matrix of beers:\n"+str(X))
o.write("Beer matrix:\n")
print "Beer matrix:\n"
o.write(str(X)+"\n\n")
print X  # prints beer matrix on console
print '\n\n'

## AGGLOMERATIVE CLUSTERING

print "AGGLOMERATIVE CLUSTERING:\n"
o.write("AGGLOMERATIVE CLUSTERING:\n")
logging.info("AGGLOMERATIVE CLUSTERING:")
k = 7
ward = AgglomerativeClustering(n_clusters=k, linkage='ward').fit(X)
labelagg = ward.labels_


# plotting....
# fig = plt.figure()
# ax = p3.Axes3D(fig)
# ax.view_init(7,-80)
# for l in np.unique(labelagg):
#    ax.plot3D(X[labelagg == l, 0],X[labelagg == l,1], X[labelagg == l, 2],
#              'o', color=plt.cm.jet(np.float(l) / np.max(labelagg + 1)))
# plt.title("Plot:")
# plt.show()


clusters = defaultdict(set)
j = 0
logging.info("Clustering output:")
for elem in labelagg:
    tobeadded = (names[j], "ranked: "+positions[j])
    clusters[elem].add(tobeadded)
    j += 1
for elem in clusters:
    result = "Cluster: " + str(elem) + " " + str(sorted(clusters[elem]))
    print result
    o.write("\n"+str(result))

# DBSCAN CLUSTERING

# Esegue l'algoritmo di clustering DBScan. DBScan clusterizza in base alla densita' del dataset.
# Un gruppo di punti sufficientemente denso viene inserito in un cluster.
#  Ref: http://scikit-learn.org/stable/modules/clustering.html#dbscan

# ATTENZIONE: non e' detto che ogni punto venga clusterizzato, DBScan considera rumore tutto cio' che non e' abbastanza
# denso. La densita' e' definita in questo modo:

# Un CORE-SAMPLE e' un punto che ha almeno MIN_SAMPLES punti a distanza minore o uguale di EPSILON
# Un cluster viene ottenuto ricorsivamente: dato un CORE-SAMPLE, si cerca tra i suoi vicini chi a sua volta e' un CORE-SAMPLE
# e cosi' via... quando l'insieme dei core-samples e' terminato, viene colorato il cluster

# I parametri da settare sono EPSILON e MIN_SAMPLES:
# EPSILON = definisce la distanza entro cui un punto e' un vicino di un altro punto
# MIN_SAMPLES = numero minimo di punti vicini necessari per rendere un punto CORE-SAMPLE


logging.info("DBSCAN CLUSTERING:")
print "\n\n\n"
print "DBSCAN CLUSTERING:\n"
o.write("\n\n")
o.write("DBSCAN CLUSTERING:\n")

EPSILON = 0.06
MIN_SAMPLES = 6
logging.info("Starting DBSCAN clustering, parameters:\nEpsilon: "+str(EPSILON)+"\nMin Samples: "+str(MIN_SAMPLES))
o.write("Starting DBSCAN clustering, parameters:\nEpsilon: "+str(EPSILON)+"\nMin Samples: "+str(MIN_SAMPLES))

db = DBSCAN(EPSILON, MIN_SAMPLES, metric='euclidean', p=None, random_state=None).fit(X)
labels = db.labels_

print "Initial labels:\n"
print initial_labels
logging.info("Initial labeling: "+str(initial_labels))
o.write("Initial labeling: "+str(initial_labels)+"\n")
print "\n"
print "Label set after DBScan:\n"
print labels
o.write("\nLabel set after DBScan:\n"+str(labels)+"\n")

clusters = defaultdict(set)
j = 0
logging.info("Clustering output:")
for elem in labels:
    tobeadded = (names[j], "ranked: "+positions[j])
    clusters[elem].add(tobeadded)
    j += 1

for elem in clusters:
    if elem != -1:
        result = "Cluster: " + str(elem) + " " + str(sorted(clusters[elem]))
        o.write("\n"+result)
        print result
        logging.info(str(result))
    else:
        result = "Noise:  "+str(sorted(clusters[elem]))
        print result
        o.write("\n"+result)
        logging.info(str(result))

print
logging.info("Labeling after DBScan: \n"+str(labels))
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# Statistics:
print('Estimated number of clusters: %d' % n_clusters_)
logging.info('Estimated number of clusters: %d' % n_clusters_)
o.write("\n"+"\n"+'Estimated number of clusters: %d' % n_clusters_)

print("Homogeneity: %0.3f" % metrics.homogeneity_score(initial_labels, labels))
logging.info("Homogeneity: %0.3f" % metrics.homogeneity_score(initial_labels, labels))
o.write("\n"+"Homogeneity: %0.3f" % metrics.homogeneity_score(initial_labels, labels))

print("Completeness: %0.3f" % metrics.completeness_score(initial_labels, labels))
logging.info("Completeness: %0.3f" % metrics.completeness_score(initial_labels, labels))
o.write("\n"+"Completeness: %0.3f" % metrics.completeness_score(initial_labels, labels))

print("V-measure: %0.3f" % metrics.v_measure_score(initial_labels, labels))
logging.info("V-measure: %0.3f" % metrics.v_measure_score(initial_labels, labels))
o.write("\n"+"V-measure: %0.3f" % metrics.v_measure_score(initial_labels, labels))

print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(initial_labels, labels))
logging.info("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(initial_labels, labels))
o.write("\n"+"Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(initial_labels, labels))

print("Adjusted Mutual Information: %0.3f" % metrics.adjusted_mutual_info_score(initial_labels, labels))
logging.info("Adjusted Mutual Information: %0.3f" % metrics.adjusted_mutual_info_score(initial_labels, labels))
o.write("\n"+"Adjusted Mutual Information: %0.3f" % metrics.adjusted_mutual_info_score(initial_labels, labels))
try:
    # !!! If there are no core-samples (i.e. no clusters) an exception is thrown
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))
    logging.info("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))
    o.write("\n"+"Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))
except:
    print("\nWARNING: DBScan has not found any clustering. Re-tune the parameters.\n")
    logging.warning("DBScan has not found any clustering. Re-tune the parameters.")
    o.write("\n"+"DBScan has not found any clustering. Re-tune the parameters.\n")
print("\n\n")

# Step 3: Plotting
# Disegna il risultato del clustering, il codice e' della demo
# Attenzione, se DBScan clusterizza in un unico cluster (non fa clustering), genera un'eccezione in fase di disegno

# Black removed and is used for noise instead.
# unique_labels = set(labels)
# colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
# for k, col in zip(unique_labels, colors):
#    if k == -1:
# Black used for noise.
#        col = 'k'
#    class_member_mask = (labels == k)
#    xy = X[class_member_mask & core_samples_mask]
#    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#             markeredgecolor='k', markersize=14)
#    xy = X[class_member_mask & ~core_samples_mask]
#    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#             markeredgecolor='k', markersize=6)
# plt.title('Estimated number of clusters: %d' % n_clusters_)
# plt.show()
o.close()

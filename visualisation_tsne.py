import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

X = np.load('x_train.npy')
note = np.load('y_train.npy')

X_embedded = TSNE(n_components=2).fit_transform(X)


fig, ax = plt.subplots(figsize=(15,15))
fig.suptitle("t-SNE dimensionality reduction", fontsize=16)
for x in range(X_embedded.shape[0]):
    ax.scatter(X_embedded[x][0], X_embedded[x][1], color='blue')

for i, txt in enumerate(note):
    ax.annotate(txt, (X_embedded[i][0],X_embedded[i][1]))
fig.savefig('foo4.png')

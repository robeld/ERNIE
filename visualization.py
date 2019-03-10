import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib import colors

from ernie import QuantizedLayer, layer_check, quantize 


def compareDistributions(arr1, arr2, path=None, show_fig=True, plot_title="linear initialization", 
	arr1Title="Initial Centroids", arr2Title="Post K-means Centroids"):
	""" Graph for comparing distributions of two Numpy arrays. Used in this codebase to compare initial 
	centroid values to those after kmeans is ran. Adapted from https://matplotlib.org/gallery/statistics/hist.html
	
	Args:
		arr1 (ndarray): 1d numpy array of floats, set to initial kmeans centroids in our code.
		arr2 (ndarray): 1d numpy array of floats, set to post kmeans centroids in our code.
		path (String): path to save graph
		show_fig (bool): Flag to show figure.
		plot_title (String): title of graph. Set to init method in our code.
		arr1Title (String): title for first subplot.
		arr2Title (String): title for second subplot.
	"""
	figure, axs = plt.subplots(1, 2, tight_layout=True, sharey=True)
	figure.suptitle(plot_title, fontsize=12, y=0.03)

	N, bins, patches = axs[0].hist(arr1, bins='auto', density=True)
	axs[0].set_title(arr1Title)
	fracs = N / N.max()
	norm = colors.Normalize(fracs.min(), fracs.max())
	for tf, tp in zip(fracs, patches):
		color = plt.cm.winter(norm(tf))
		tp.set_facecolor(color)
	axs[0].yaxis.set_major_formatter(PercentFormatter(xmax=1))

	figure.subplots_adjust(hspace=0.5)

	N, bins, patches = axs[1].hist(arr2, bins='auto', density=True)
	axs[1].set_title(arr2Title)
	fracs = N / N.max()
	norm = colors.Normalize(fracs.min(), fracs.max())
	for tf, tp in zip(fracs, patches):
		color = plt.cm.winter(norm(tf))
		tp.set_facecolor(color)
	#axs[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))
	if path: 
		figure.savefig(path)
	if show_fig:
		plt.show()
def graphCDF(weights, path=None, title=None, show_fig=True, plot_title="Weights CDF Estimate"):
	"""
	Graph for graphing CDF of the values in a numpy array. Used in this codebase to graph
	CDF of weights of a layer. Adapted from https://matplotlib.org/examples/statistics/histogram_demo_cumulative.html

	Args:
		weights (ndarray): 1d numpy array of floats, set to weights of a layer in our code.
		path (String): path to save graph
		title (String): title of graph. Set to layer name in our code.
		show_fig (bool): Flag to show figure.
		plot_title (String): title of graph. Set to "Weights CDF Estimate" in our code.
	"""
	figure, ax = plt.subplots(figsize=(8, 4))
	figure.suptitle(plot_title, fontsize=12)
	num_bins = int(weights.size/10)
	ax.hist(weights, bins=num_bins, density=1, histtype='step', cumulative=True, label='weights')
	if path:
		figure.savefig(path)
	if show_fig:
		plt.show()

x = np.random.randn(500)
y = np.random.randn(500)
compareDistributions(x, y)
graphCDF(x)
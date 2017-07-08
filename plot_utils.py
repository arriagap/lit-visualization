import matplotlib.pyplot as plt
import numpy as n
from analyze import *
from parser import *

from scipy.interpolate import InterpolatedUnivariateSpline as ius
from scipy.interpolate import UnivariateSpline as us

def plot_freqs(locs, word, binsize = 100.):
    # This doesn't work to well, too shitty
    maxlocs = n.max(locs)
    bins = n.zeros(int(maxlocs / binsize) + 1)
    for i in range(len(bins)):
        curr_bin_lower = i * 100.
        curr_bin_higher = (i + 1) * 100.
        bins[i] = len([x for x in ivan_locs if x > curr_bin_lower and x < curr_bin_higher])



def plot_density(locs, binsize = 300):
    maxlocs = n.max(locs)
    denses = n.zeros(maxlocs)
    wordpos = n.arange(maxlocs)
    for i in range(0, maxlocs):
        lowerbin = i - binsize
        upperbin = i + binsize
        denses[i] = len([x for x in locs if x > lowerbin and x < upperbin])
    spl = us(wordpos, denses, s = 10)
    xx = n.linspace(0,maxlocs,  maxlocs * 3)
    plt.plot(xx, spl(xx))
#    plt.show()

def get_densities(locs, binsize = 200):
    maxlocs = n.max(locs)
    denses = []
    poses = []
    currdense = -1
    for i in range(0, maxlocs):
        lowerbin = i - binsize
        upperbin = i + binsize
        dense = len([x for x in locs if x > lowerbin and x < upperbin])
        if dense != currdense:
            denses.append(dense)
            poses.append(i)
            currdense = dense
    return poses, denses

def plot_density_lines(poses, denses, ax, **kwargs):
    maxlocs = n.max(poses)
    spl = us(poses, denses, s = 100)
    xx = n.linspace(0,maxlocs,  (maxlocs - 50) * 3)
    ax.plot(xx, spl(xx), **kwargs)
    
    

def show_colorbars(poses, denses, ax, cmap = 'Blues'):
#    norm_denses = n.array(n.array(denses) * 256. / n.max(denses), dtype = int)
    maxlocs = n.max(poses)

    xx = n.linspace(0,maxlocs,  (maxlocs - 50) * 1)
    spl = us(poses, denses, s = 100)
    yy = spl(xx)
    yim = [yy for i in range(1000)]
    yim = n.array(yim)
    ax.imshow(yim, cmap = plt.get_cmap(cmap))
#    ax.set_ylim([0,1000])



def test_text():
    f = open('ivans.txt', 'rb')
    a = f.readlines()
    a = split_text(a)
    a = remove_stopwords(a)
    word_freq, word_locs = mark_words_individual(a)
    trunc_word_freq, trunc_word_locs = get_top_words(word_freq, word_locs, numwords=100)
    ivanlocs = trunc_word_locs['IVANOVITCH'][0]
    ivanposes, ivandenses = get_densities(ivanlocs)
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex = True)
    plot_density_lines(ivanposes, ivandenses, ax1)
    show_colorbars(ivanposes, ivandenses, ax2)
#    plt.show()
    nikolocs = trunc_word_locs['NIKIFOROVITCH'][0]
    nikoposes, nikodenses = get_densities(nikolocs)
    show_colorbars(nikoposes, nikodenses, ax3, cmap = 'Reds')

    plot_density_lines(nikoposes, nikodenses, ax1, c = 'r')
    plt.show()



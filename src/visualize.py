import pandas as pd
import fastf1
from fastf1.plotting import setup_mpl
import matplotlib.pyplot as plt


def plot_one(alignedA, y_col = "Speed", label=None):
    
    plt.figure()
    plt.plot(alignedA['Distance'], alignedA[y_col], label=label)
    plt.xlabel('Distance (m)')
    plt.ylabel(y_col)
    if label:
        plt.legend()
    plt.show()


def plot_compare(alignedA, alignedB, y_col = "Speed", labelA=None, labelB=None, title=None):
    plt.figure()
    plt.plot(alignedA['Distance'], alignedA[y_col], label=labelA)
    plt.plot(alignedB['Distance'], alignedB[y_col], label=labelB)
    plt.xlabel('Distance (m)')
    plt.ylabel(y_col)
    plt.title(title)
    if labelA or labelB:
        plt.legend()
    plt.savefig(f'outputs/figures/{title}')
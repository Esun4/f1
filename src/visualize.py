import pandas as pd
import numpy as np
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


def compute_delta(alignedA, alignedB):
    if len(alignedA) != len(alignedB):
        raise ValueError("alignedA and alignedB must have the same length.")
    if not np.allclose(alignedA['Distance'].to_numpy(), alignedB['Distance'].to_numpy(), equal_nan=False):
        raise ValueError("Distance grids do not match between alignedA and alignedB.")

    dist = alignedA['Distance'].to_numpy(dtype=float)

    vA = alignedA['Speed'].to_numpy(dtype=float) / 3.6
    vB = alignedB['Speed'].to_numpy(dtype=float) / 3.6
    
    dd = np.diff(dist)

    vA_seg = (vA[:-1] + vA[1:]) / 2.0
    vB_seg = (vB[:-1] + vB[1:]) / 2.0

    eps = 1e-6
    vA_seg = np.maximum(vA_seg, eps)
    vB_seg = np.maximum(vB_seg, eps)

    dtA = dd / vA_seg
    dtB = dd / vB_seg

    
    tA = np.concatenate(([0.0], np.cumsum(dtA)))
    tB = np.concatenate(([0.0], np.cumsum(dtB)))
    delta = tA - tB

    return pd.DataFrame(
        {
            "Distance": dist,
            "tA_s": tA,
            "tB_s": tB,
            "delta_s": delta,
        }
    )

def plot_delta_curve(
    delta_df,
    labelA,
    labelB
):
    x = delta_df['Distance'].to_numpy()
    y = delta_df['delta_s'].to_numpy()

    plt.figure()
    plt.plot(x, y)
    plt.axhline(0.0, linewidth=1)
    plt.xlabel("Distance (m)")
    plt.ylabel(f"Delta (s): {labelA} - {labelB}")
    plt.title(f"Cumulative Delta vs Distance ({labelA} - {labelB})")

    plt.savefig('outputs/figures/Delta.png', dpi=200, bbox_inches="tight")
    plt.close()


def plot_compare(alignedA, alignedB, y_col=None, labelA=None, labelB=None, title=None):
    plt.figure()
    plt.plot(alignedA['Distance'], alignedA[y_col], label=labelA)
    plt.plot(alignedB['Distance'], alignedB[y_col], label=labelB)
    plt.xlabel('Distance (m)')
    plt.ylabel(y_col)
    plt.title(title)
    if labelA is not None or labelB is not None:
        plt.legend()
    plt.savefig(f'outputs/figures/{title}')
    plt.close()
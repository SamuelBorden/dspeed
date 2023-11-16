from __future__ import annotations

import numpy as np
from numba import guvectorize

from dspeed.utils import numba_defaults_kwargs as nb_kwargs


@guvectorize(
    [
        "void(float32[:], float32, float32[:])",
        "void(float64[:], float64, float64[:])",
    ],
    "(n),()->()",
    **nb_kwargs,
)
def get_wf_centroid(w_in: np.ndarray, shift: int, centroid: int) -> None:
    """Calculate waveform centroid.

    Note
    ----
    This processor calculate the centroid position when provided the convolution product with a step function.

    Parameters
    ----------
    w_in
        the input waveform.
    shift
        shift.
    centroid
        centroid position.

    JSON Configuration Example
    --------------------------

    .. code-block :: json

        "centroid": {
          "function": "get_wf_centroid",
          "module": "dspeed.processors",
          "args": ["waveform", "shift", "centroid"],
          "unit": "ADC"
        }
    """

    centroid[0] = np.nan

    if np.isnan(w_in).any() or np.isnan(shift):
        return

    if shift < 0 or shift > len(w_in) - 1:
        return

    c_a = (
        np.where(w_in[w_in.argmin() : w_in.argmax()] > 0)[0][0] + w_in.argmin() + shift
    )
    c_b = (
        np.where(w_in[w_in.argmin() : w_in.argmax()] < 0)[0][-1] + w_in.argmin() + shift
    )

    centroid[0] = round((c_a + c_b) / 2)

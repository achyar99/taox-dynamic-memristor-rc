"""
Minimal dynamic-memristor model used for reservoir computing in Zhong et al.,
Nat. Commun. 12, 408 (2021), doi:10.1038/s41467-020-20692-1.

    G[n] = r*G[n-1] + (1-r)*G0 + u(V)*(target(V) - G[n-1])
    u(V) = a|V| / (a|V| + 1),   target(V) = 1 if V > 0 else 0
    I    = G * (Kp*max(V,0)^3 + Kn*min(V,0)^3)

The state G decays back to G0 between pulses, so the device's response depends on
recent inputs (fading memory), which is what a reservoir is meant to exploit. The control runs
in the README test how much it actually contributes to spoken-digit accuracy.
"""

import matplotlib.pyplot as plt
import numpy as np

PARAMS = dict(r=0.99, G0=0.5, Kp=9.13, Kn=0.32, a=0.23)  # values published with the paper


def run(V, r, G0, Kp, Kn, a):
    """Returns the device current and internal state for an input voltage sequence V."""
    G, I, state = G0, np.zeros_like(V), np.zeros_like(V)
    for n, v in enumerate(V):
        u = a * abs(v) / (a * abs(v) + 1)
        G = r * G + (1 - r) * G0 + u * ((v > 0) - G)
        I[n], state[n] = G * (Kp * max(v, 0) ** 3 + Kn * min(v, 0) ** 3), G
    return I, state


if __name__ == "__main__":
    # a burst of three 2 V pulses, then a single pulse: the state builds up and fades away
    V = np.zeros(400)
    V[[50, 55, 60, 250]] = 2.0
    _, G = run(V, **PARAMS)
    plt.plot(G)
    plt.axhline(PARAMS["G0"], color="grey", lw=0.5, ls=":")
    plt.xlabel("Time step")
    plt.ylabel("Device state G")
    plt.title("Pulses push the state up, then it relaxes: fading memory")
    plt.show()

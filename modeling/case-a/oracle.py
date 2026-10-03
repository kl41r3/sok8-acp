#!/usr/bin/env python3
"""Case A evaluator and a declared numerical illustration, independent of an LLM."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
B = 0.15
ETA = 0.005
KAPPA = 0.01
TIE_TOL = 1e-12


def evaluate(theta: float, d: float, q: float) -> dict:
    a = min(theta + B, d)
    va = -(a - theta - B) ** 2
    vr = -q * B ** 2 - (1 - q) * (theta + B) ** 2 - ETA
    choice = "REVIEW" if vr > va + TIE_TOL else "AUTO"
    loss_auto = (a - theta) ** 2
    loss_review = KAPPA + (1 - q) * theta ** 2
    return {
        "theta": theta, "d": d, "q": q, "a_auto": a,
        "utility_auto": va, "utility_review": vr,
        "oracle_choice": choice,
        "utility_margin_review_minus_auto": vr - va,
        "user_loss_auto": loss_auto, "user_loss_review": loss_review,
        "user_loss_selected": loss_review if choice == "REVIEW" else loss_auto,
        "review_threshold_d": theta + B - math.sqrt(q * B ** 2 + (1 - q) * (theta + B) ** 2 + ETA),
    }



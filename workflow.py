"""Brightway workflow for a simple CryoPop versus standard cryotherapy comparison."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Brightway2 2.4.x still expects legacy NumPy aliases such as np.NaN, which
# were removed in NumPy 2.0+. Provide a small compatibility shim so the older
# Brightway stack can run on newer NumPy versions.
for legacy_name, target_name in (("NaN", "nan"), ("Inf", "inf"), ("Infinity", "inf")):
    if not hasattr(np, legacy_name) and hasattr(np, target_name):
        setattr(np, legacy_name, getattr(np, target_name))

from brightway2 import *
from premise_gwp import add_premise_gwp

from config import (
    CO2_USE_PER_PROCEDURE_KG,
    ELECTRICITY_EF,
    FOREGROUND_DB_NAME,
    FUNCTIONAL_UNITS,
    IMPACT_METHOD,
    MANUFACTURING_ENERGY_MJ,
    PROJECT_NAME,
    STEEL_MASS_PER_DEVICE_KG,
    STEEL_RECYCLING_CREDIT,
    TRANSPORT_DISTANCE_KM,
    TRUCK_EF,
    DELRIN_MASS_PER_DEVICE_KG,
)

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def setup_project():
    """Initialize the Brightway project and return the biosphere database."""
    projects.set_current(PROJECT_NAME)

    if "biosphere3" not in databases:
        bw2setup()

    biosphere = Database("biosphere3")
    return biosphere


def create_processes(biosphere):
    """Create the foreground activities for the two scenarios."""
    co2 = biosphere.search("carbon dioxide, fossil")[0]

    if FOREGROUND_DB_NAME in databases:
        del databases[FOREGROUND_DB_NAME]

    db = Database(FOREGROUND_DB_NAME)

    crypop_process = {
        "name": "CryoPop cryotherapy procedure",
        "unit": "procedure",
        "exchanges": [
            {"input": co2.key, "amount": STEEL_MASS_PER_DEVICE_KG * 6.15, "type": "biosphere"},
            {"input": co2.key, "amount": DELRIN_MASS_PER_DEVICE_KG * 3.40, "type": "biosphere"},
            {"input": co2.key, "amount": MANUFACTURING_ENERGY_MJ * ELECTRICITY_EF, "type": "biosphere"},
            {"input": co2.key, "amount": (STEEL_MASS_PER_DEVICE_KG + DELRIN_MASS_PER_DEVICE_KG) * TRANSPORT_DISTANCE_KM * TRUCK_EF, "type": "biosphere"},
            {"input": co2.key, "amount": CO2_USE_PER_PROCEDURE_KG, "type": "biosphere"},
            {"input": co2.key, "amount": STEEL_RECYCLING_CREDIT, "type": "biosphere"},
        ],
    }

    standard_process = {
        "name": "Standard cryotherapy procedure",
        "unit": "procedure",
        "exchanges": [
            {"input": co2.key, "amount": 2 * STEEL_MASS_PER_DEVICE_KG * 6.15, "type": "biosphere"},
            {"input": co2.key, "amount": 2 * DELRIN_MASS_PER_DEVICE_KG * 3.40, "type": "biosphere"},
            {"input": co2.key, "amount": 2 * MANUFACTURING_ENERGY_MJ * ELECTRICITY_EF, "type": "biosphere"},
            {"input": co2.key, "amount": 1.2 * (STEEL_MASS_PER_DEVICE_KG + DELRIN_MASS_PER_DEVICE_KG) * TRANSPORT_DISTANCE_KM * TRUCK_EF, "type": "biosphere"},
            {"input": co2.key, "amount": 0.2, "type": "biosphere"},
        ],
    }

    db.write({
        (FOREGROUND_DB_NAME, "CryoPop cryotherapy procedure"): crypop_process,
        (FOREGROUND_DB_NAME, "Standard cryotherapy procedure"): standard_process,
    })

    return Database(FOREGROUND_DB_NAME)


def run_comparison():
    """Run the LCA comparison and return the results."""
    biosphere = setup_project()
    db = create_processes(biosphere)

    add_premise_gwp()

    if IMPACT_METHOD not in methods:
        raise RuntimeError("The requested impact method is not available in the current Brightway setup.")

    fu_crypop = {(FOREGROUND_DB_NAME, "CryoPop cryotherapy procedure"): FUNCTIONAL_UNITS}
    fu_standard = {(FOREGROUND_DB_NAME, "Standard cryotherapy procedure"): FUNCTIONAL_UNITS}

    lca_crypop = LCA(fu_crypop, IMPACT_METHOD)
    lca_crypop.lci()
    lca_crypop.lcia()

    lca_standard = LCA(fu_standard, IMPACT_METHOD)
    lca_standard.lci()
    lca_standard.lcia()

    avoided_gwp = lca_standard.score - lca_crypop.score
    percent_savings = (avoided_gwp / lca_standard.score) * 100 if lca_standard.score else 0.0

    save_plot(lca_crypop, lca_standard)

    return {
        "crypop_score": lca_crypop.score,
        "standard_score": lca_standard.score,
        "avoided_gwp": avoided_gwp,
        "percent_savings": percent_savings,
        "method": IMPACT_METHOD,
    }


def save_plot(lca_crypop, lca_standard):
    """Save a simple bar chart comparison to the results directory."""
    labels = ["Standard cryotherapy", "CryoPop"]
    scores = [lca_standard.score, lca_crypop.score]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, scores, color=["#d62728", "#2ca02c"])
    plt.ylabel("GWP (kg CO2-eq)")
    plt.title(f"GWP comparison for {FUNCTIONAL_UNITS} procedures")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height * 1.01, f"{height:.3f}", ha="center")

    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "gwp_comparison.png")
    plt.close()


def format_results(results):
    """Return a human-readable summary string."""
    return (
        f"Impact method: {results['method']}\n"
        f"CryoPop GWP: {results['crypop_score']:.4f} kg CO2-eq\n"
        f"Standard GWP: {results['standard_score']:.4f} kg CO2-eq\n"
        f"Avoided GWP: {results['avoided_gwp']:.4f} kg CO2-eq\n"
        f"Percent savings: {results['percent_savings']:.1f}%"
    )

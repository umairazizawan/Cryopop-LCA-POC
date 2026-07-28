"""Configuration values for the CryoPop Brightway proof-of-concept.

All constants are intentionally kept in one place so that the main script can
remain simple and focus on workflow orchestration.
"""

# Core assumptions used in the simplified comparative LCA
DEVICE_LIFETIME = 500
STEEL_MASS_PER_DEVICE_KG = 0.25 / DEVICE_LIFETIME
DELRIN_MASS_PER_DEVICE_KG = 0.10 / DEVICE_LIFETIME
CO2_USE_PER_PROCEDURE_KG = 0.02
MANUFACTURING_ENERGY_MJ = 5 / DEVICE_LIFETIME
ELECTRICITY_EF = 0.07
TRANSPORT_DISTANCE_KM = 1000
TRUCK_EF = 0.0001
STEEL_RECYCLING_CREDIT = -1.5 * STEEL_MASS_PER_DEVICE_KG
FUNCTIONAL_UNITS = 1000

# Project and database names
PROJECT_NAME = "CryoPop_LCA_POC"
FOREGROUND_DB_NAME = "crypop_foreground"
IMPACT_METHOD = ("IPCC 2021", "climate change", "GWP 100a, incl. H")

# Explanations for the constants used in the model
CONSTANT_EXPLANATIONS = {
    "DEVICE_LIFETIME": "Assumed operating lifetime of the device in use cycles.",
    "STEEL_MASS_PER_DEVICE_KG": "Allocated steel mass per procedure, assuming the device is used over its lifetime.",
    "DELRIN_MASS_PER_DEVICE_KG": "Allocated Delrin mass per procedure, assuming the device is used over its lifetime.",
    "CO2_USE_PER_PROCEDURE_KG": "Estimated CO2 released during use for one procedure.",
    "MANUFACTURING_ENERGY_MJ": "Estimated manufacturing energy allocated per procedure.",
    "ELECTRICITY_EF": "Emission factor for electricity use in the manufacturing stage.",
    "TRANSPORT_DISTANCE_KM": "Assumed transport distance for the device/materials.",
    "TRUCK_EF": "Emission factor for freight transport.",
    "STEEL_RECYCLING_CREDIT": "Credit applied for recycled steel at end-of-life.",
    "FUNCTIONAL_UNITS": "Number of procedures represented by the functional unit.",
}

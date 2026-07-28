# Brightway LCA proof of concept

This repository contains a simplified Life Cycle Assesment (LCA) using Brightway2 workflow that compares a CryoPop-based cryotherapy procedure with a standard cryotherapy baseline.

The repository:
- creates a Brightway2 project and biosphere database
- builds two foreground processes
- runs a simplified LCA comparison
- saves a plot of the results in the results folder

## Repository structure

- [config.py](config.py) – model assumptions and project settings
- [workflow.py](workflow.py) – workflow logic for creating processes and running the comparison
- [main.py](main.py) – entry point for the analysis
- [requirements.txt](requirements.txt) – pinned dependency versions
- [docs/assumptions.md](docs/assumptions.md) – notes on the model assumptions

## Build Steps

1. Open PowerShell in the project folder.
2. Create and activate a fresh virtual environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Upgrade packaging tools and install the pinned dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Run the analysis:

```powershell
python main.py
```

## Compatibility

This project was verified on Windows with Python 3.13.12 and NumPy 2.5.1. Brightway2 2.4.x still uses some older NumPy aliases such as `np.NaN`, so the workflow includes a small compatibility shim to keep it working on newer NumPy releases.

In case of install errors, use a fresh virtual environment and reinstall from the pinned requirements file.

## Notes

The model is intentionally simplified and intended for educational/tutorial purposes for brightway2 package. It should not be used for formal regulatory reporting or commercial claims.

For the actual CryoPop device, refer to the official sources such as:

- https://pmc.ncbi.nlm.nih.gov/articles/PMC8666835/
- https://www.youtube.com/watch?v=yUe_uNwiEog
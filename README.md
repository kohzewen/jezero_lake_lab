# Jezero Open-Basin Lake Lab
**Authors:** Ze-Wen Koh (MIT), Shaalin Sehra (MIT)

A Jupyter lab on Python GIS techniques (rioxarray, GDAL, geopandas, pyproj). Students work with remote-sensing data to measure the Jezero crater paleolake on Mars and analyze rover data. Designed and written as Lab 4 for MIT course 12.621, *Remote Sensing: Physical Principles and Techniques*.

| File | What it is |
|---|---|
| `jezero_lake_lab.ipynb` | Jupyter notebook containing lab, with blanks to fill in (`...`, `# YOUR CODE HERE`) |
| `Remote_Sensing_Lab_4.docx` | **Answer sheet** for students to hand in |
| `environment.yml` | Conda environment for students |
| `helper_functions.py` | Plotting and interactive tools imported by the notebook (`plot_basemap`, `LineDrawer`, `PolygonEditor`, …) |
| `images/` | Figures shown in the notebook |
| `jezero_data/` | All input data (below) |

**Data files (`jezero_data/`)**

This directory needs to be installed [here](https://www.dropbox.com/scl/fo/upf0ypxnlht3icppzsai8/ABpcrHPsnDZchqHTrF55Evw?rlkey=u43bk6ga1qzpepwkuekc498do&st=cdbnfmx9&dl=0).

| File | What it is |
|---|---|
| `jezero_CTX_DEM.tif` | CTX DEM, 20 m/px (Jezero equirectangular projection, standard parallel 18.4663°N) |
| `jezero_MOLA_HRSC_DEM.tif` | MOLA–HRSC blended DEM, 200 m/px (equirectangular, standard parallel 0°) |
| `jezero_prebreach.gpkg` | Pre-breach lake polygon (level in `BreachZ_m`), Part 4 |
| `perseverance_waypoints.json` | Perseverance end-of-drive positions (NASA/JPL), Part 5 |
| `perseverance_traverse_jezero.gpkg` | Perseverance drive paths in the CTX DEM's CRS, Part 5 (converted from `perseverance_traverse.json`, NASA's original file in lon/lat) |
| `supercam_libs_moc.csv` | SuperCam rock compositions (PDS Geosciences Node), Part 5 |
| `supercam_mingsbight_spectrum.fits` | One SuperCam LIBS spectrum of the rock *Mings Bight*, sol 1494 (PDS Geosciences Node), Part 5 |


## Python Setup and Environments

### Understanding Python environments

Installing Python packages globally is like throwing every tool you own into one giant pile in your garage. Eventually, two tools won't work together: for example, one package might require an older version of a library while another requires a newer version.

A **Conda environment** is like a self-contained, isolated toolbox created specifically for a single class or project.

> **Why Conda instead of pip?** Geospatial libraries like `rasterio` rely on heavy C++ libraries in the background (like GDAL and PROJ) to read satellite imagery. Standard Python installers (`pip`) often fail on Windows and Mac because they try to compile these C++ tools from scratch. Conda downloads pre-built versions that work out of the box.

### Step 1: Download and install Miniconda

> **Already have Conda?** If you already have Anaconda, Miniconda, Miniforge or Mambaforge installed, skip this step and go to Step 2. To check, open a terminal (Anaconda Prompt on Windows) and run `conda --version`: if it prints a version number, you have Conda.

Miniconda is a lightweight, bare-bones version of Anaconda. It gives you the environment manager without cluttering your hard drive with hundreds of unused programs.

**Windows**

1. Go to the [Miniconda download page](https://www.anaconda.com/docs/getting-started/miniconda/install).
2. Download the Windows 64-bit installer.
3. Run the `.exe` file and accept the default settings. **Important:** check the option to *"Register Miniconda3 as my default Python"* if prompted.

**Mac**

1. Go to the [Miniconda download page](https://www.anaconda.com/docs/getting-started/miniconda/install).
2. Check your Mac's processor (Apple menu, top left → **About This Mac**):
   * **Apple Silicon (M1/M2/M3/M4):** download the macOS Apple M-series (arm64) installer.
   * **Intel:** download the macOS Intel x86 installer.
3. Run the downloaded `.pkg` installer and follow the standard installation steps.

### Step 2: Open your terminal / command line

Once Miniconda is installed, open the command-line program on your computer:

* **Windows:** press the Windows key, search for **Anaconda Prompt** (or **Miniconda Prompt**), and open it. (Don't use the standard Command Prompt or PowerShell unless you have set them up for Conda.)
* **Mac:** press **Cmd + Space**, search for **Terminal**, and press **Enter**.

### Step 3: Go to the lab folder

Download or clone this repository, then move into its folder (replace the path with wherever you saved it):

```bash
cd path/to/remote_sensing_mars_lab
```

### Step 4: Create the lab environment

This reads `environment.yml` and installs everything the lab needs into a new environment called `mars-gis-lab`. It only needs to be done once and can take several minutes.

```bash
conda env create -f environment.yml
```

### Step 5: Activate the environment and start Jupyter

```bash
conda activate mars-gis-lab
jupyter lab
```

A browser tab will open automatically. Click on your lab `.ipynb` file in the left sidebar to open it, or click **Python 3 (ipykernel)** under "Notebook" to create a new notebook.

### Step 6: Test your installation

In the first cell of a new notebook, paste the following code and press **Shift + Enter** to run it:

```python
import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

print("Rasterio version:", rasterio.__version__)
print("All remote sensing libraries loaded successfully!")
```

If it prints the version number without any red error messages, your environment is ready.

### Troubleshooting

**`ModuleNotFoundError: No module named 'rasterio'`**
You probably forgot to activate the environment before launching Jupyter. Close Jupyter, run `conda activate mars-gis-lab`, and start `jupyter lab` again.

**Kernel errors inside Jupyter**
In the top-right corner of JupyterLab, check that the selected kernel is **Python 3 (ipykernel)**, running from the `mars-gis-lab` environment you activated before starting Jupyter.


## Running the Lab

1. Open **Anaconda Prompt** (Windows) or **Terminal** (Mac).
2. Activate your environment:
   ```bash
   conda activate mars-gis-lab
   ```
3. Go to your lab folder:
   ```bash
   cd path/to/remote_sensing_mars_lab
   ```
4. Start Jupyter:
   ```bash
   jupyter lab
   ```


Run the notebook from the repository folder: it reads its inputs from `jezero_data/` and `images/`, and writes the files it creates to `outputs/`.

**Interactive figures are required.** Drawing profiles and polygons needs `ipympl`, which is included in `environment.yml`, and works in JupyterLab 4 / Notebook 7. Students draw their own lines and polygons (there are no defaults); the first code cell prints `interactive figures: ON` when it is working. If you install `ipympl` into an existing environment, restart Jupyter afterwards.


## Final Submission

When you are done with the lab, you only need to submit the `Remote_Sensing_Lab_4.docx` file with your answers and plots from the Jupyter Notebook filled in.

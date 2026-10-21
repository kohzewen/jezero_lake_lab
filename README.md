Jezero Open-Basin Lake Lab

Authors: Ze-Wen Koh (MIT), Shaalin Sehra (MIT)

A Jupyter lab on Python GIS techniques (rioxarray, GDAL, geopandas, pyproj). Students work with remote-sensing data to measure the Jezero crater paleolake on Mars and analyze rover data. Designed and written as Lab 4 for MIT course 12.621, Remote Sensing: Physical Principles and Techniques.

New to coding? That's fine. Follow the steps below in order and copy each command exactly. Setup takes about 20–30 minutes, so please do it before class.

Quick start (if you already use Git and Conda)
bash
git clone https://github.com/kohzewen/jezero_lake_lab.git
cd jezero_lake_lab
# download the jezero_data/ folder (link below) and put it inside jezero_lake_lab/
conda env create -f environment.yml
conda activate mars-gis-lab
jupyter lab

Everyone else, start at Step 1.

What's in this repository
File	What it is
jezero_lake_lab.ipynb	The lab itself: a Jupyter notebook with blanks to fill in (..., # YOUR CODE HERE)
Remote_Sensing_Lab_4.docx	Answer sheet that you hand in
Lab4_Intro_to_PythonBased_GIS_on_Mars.pdf	Introduction to the lab
environment.yml	List of the Python packages the lab needs (used in Step 4)
helper_functions.py	Plotting and interactive tools the notebook uses. You don't need to open it
images/	Figures shown in the notebook
outputs/	Where the notebook saves the files it makes
jezero_data/	All input data. Not included: you download it separately in Step 2
Step 1: Download the lab files

Pick one option.

Option A: Download a ZIP file (easiest, no GitHub account needed)
At the top of this page, click the green <> Code button, then Download ZIP.
Unzip it:
Mac: double-click the ZIP file in your Downloads folder.
Windows: right-click the ZIP file → Extract All… → Extract. Don't work from inside the ZIP file without extracting it first: the notebook can't save files there.
You now have a folder called jezero_lake_lab-main. Move it somewhere you'll find again, such as your Documents folder.
Option B: Clone with Git (if you have Git installed)

Open a terminal (see Step 3 if you're not sure how), go to where you want the folder, and run:

bash
git clone https://github.com/kohzewen/jezero_lake_lab.git

This makes a folder called jezero_lake_lab. If we update the lab later, get the changes by running git pull inside that folder.

Step 2: Download the data folder

The data files are too big for GitHub, so they are on Dropbox.

Open the data folder on Dropbox and click Download (you don't need a Dropbox account; close any sign-in pop-up).
Unzip it the same way as in Step 1.
Make sure the folder is named exactly jezero_data (rename it if needed), and move it inside your lab folder.

When you're done, your lab folder should look like this:

jezero_lake_lab-main/          (or jezero_lake_lab/ if you used Git)
├── jezero_lake_lab.ipynb
├── Remote_Sensing_Lab_4.docx
├── environment.yml
├── helper_functions.py
├── images/
├── outputs/
└── jezero_data/
    ├── jezero_CTX_DEM.tif
    ├── jezero_MOLA_HRSC_DEM.tif
    ├── jezero_prebreach.gpkg
    ├── perseverance_waypoints.json
    ├── perseverance_traverse_jezero.gpkg
    ├── supercam_libs_moc.csv
    └── supercam_mingsbight_spectrum.fits

Check: open jezero_data and make sure you see the .tif, .gpkg, .json, .csv and .fits files directly inside it, not another folder called jezero_data inside it.

What the data files are

File	What it is
jezero_CTX_DEM.tif	CTX elevation model, 20 m/px (Jezero equirectangular projection, standard parallel 18.4663°N)
jezero_MOLA_HRSC_DEM.tif	MOLA–HRSC blended elevation model, 200 m/px (equirectangular, standard parallel 0°)
jezero_prebreach.gpkg	Pre-breach lake polygon (level in BreachZ_m), Part 4
perseverance_waypoints.json	Perseverance end-of-drive positions (NASA/JPL), Part 5
perseverance_traverse_jezero.gpkg	Perseverance drive paths in the CTX DEM's CRS, Part 5 (converted from perseverance_traverse.json, NASA's original file in lon/lat)
supercam_libs_moc.csv	SuperCam rock compositions (PDS Geosciences Node), Part 5
supercam_mingsbight_spectrum.fits	One SuperCam LIBS spectrum of the rock Mings Bight, sol 1494 (PDS Geosciences Node), Part 5
Step 3: Install Miniconda

Already have Conda? If you have Anaconda, Miniconda, Miniforge or Mambaforge, skip to Step 4. Not sure? Open a terminal (below) and type conda --version. If it prints a version number, you have Conda.

What is this, and why? The lab needs a set of Python packages. Conda installs them into a separate "environment": a self-contained toolbox just for this class, so it can't clash with anything else on your computer. Miniconda is the small version of Conda. (Experienced users: we use Conda rather than pip because rasterio and GDAL rely on compiled C++ libraries that pip often fails to install.)

Windows

Go to the Miniconda download page and download the Windows 64-bit installer.
Run the .exe file and accept the default settings. If asked, tick "Register Miniconda3 as my default Python".

Mac

Find your Mac's chip: Apple menu (top left) → About This Mac.
Go to the Miniconda download page and download:
Apple M1/M2/M3/M4 chip: the macOS Apple Silicon (arm64) installer.
Intel chip: the macOS Intel (x86) installer.
Run the downloaded .pkg file and follow the steps.
How to open a terminal

A terminal is a window where you type commands. You'll use it to set up and to start the lab.

Windows: press the Windows key, search for Anaconda Prompt (or Miniconda Prompt) and open it. Use this, not the regular Command Prompt or PowerShell.
Mac: press Cmd + Space, type Terminal, and press Enter. If you just installed Miniconda, close and reopen Terminal first.

To run a command: type it (or paste it), then press Enter, and wait until the terminal is ready for the next one.

Step 4: Create the lab environment (once only)
In your terminal, go into your lab folder. The easiest way: type cd followed by a space, then drag the lab folder from Finder / File Explorer into the terminal window and press Enter. It should look something like this:
bash
   cd /Users/yourname/Documents/jezero_lake_lab-main

(On Windows the path looks like C:\Users\yourname\Documents\jezero_lake_lab-main.)

Create the environment:
bash
   conda env create -f environment.yml

This downloads and installs everything into an environment called mars-gis-lab. It can take 5–15 minutes. If it asks Proceed ([y]/n)?, type y and press Enter. It's finished when you see the conda activate mars-gis-lab instructions and can type again.

You only do Step 4 once.

Step 5: Start the lab (every time)

Each time you work on the lab, open a terminal and run these three commands:

bash
conda activate mars-gis-lab
cd path/to/your/lab/folder
jupyter lab

(For the cd line, use the drag-and-drop trick from Step 4.)

The start of the line in your terminal should change from (base) to (mars-gis-lab). JupyterLab then opens in your web browser. Double-click jezero_lake_lab.ipynb in the left sidebar to open the lab.

Run a cell with Shift + Enter. Run the cells in order, from the top.
Save often with Cmd + S (Mac) or Ctrl + S (Windows).
Keep the terminal window open while you work. Closing it stops Jupyter.
When you're done, save, close the browser tab, then press Ctrl + C in the terminal.

Check that it works: the first code cell in the notebook prints interactive figures: ON. The lab needs interactive figures, because you will click on maps to draw lines and polygons.

Troubleshooting

conda: command not found (Mac) or 'conda' is not recognized (Windows) Mac: close Terminal and open it again. Windows: make sure you opened Anaconda Prompt, not the regular Command Prompt. If it still fails, reinstall Miniconda (Step 3).

EnvironmentFileNotFound or environment.yml not found Your terminal isn't in the lab folder. Repeat the cd step (Step 4), then try again. Typing ls (Mac) or dir (Windows) should list environment.yml.

CondaValueError: prefix already exists You've already created the environment, so skip to Step 5.

ModuleNotFoundError: No module named 'rasterio' (or another package) Jupyter was started without activating the environment. Close Jupyter, run conda activate mars-gis-lab, then jupyter lab again.

FileNotFoundError mentioning jezero_data The data folder is missing, misnamed, or in the wrong place. Check the folder picture in Step 2.

Figures don't respond to clicks / interactive figures is not ON Make sure you started Jupyter from the mars-gis-lab environment (Step 5), then restart: close Jupyter, run jupyter lab again, and rerun the notebook from the top.

Wrong kernel In the top-right corner of the notebook, the kernel should say Python 3 (ipykernel). If Jupyter was started from mars-gis-lab, this is the right one.

Still stuck? Copy the full error message and bring it to office hours or post it on Canvas.

Final submission

When you're done, fill in your answers and plots from the notebook in Remote_Sensing_Lab_4.docx and submit that file on Canvas. That's the only file you need to hand in.

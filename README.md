# PhysiCOOL data visualizer


## Setting up

Create a conda environment with the required dependencies.


```
conda env create -f environment.yml
```

# Launching the app

Activate the environment (it's called `pc-app`)

```
conda activate pc-app
```

Copy your output folder into this directory. By default, the app will look for a folder called `output`, but you can change this by modifying the `OUTPUT_PATH` variable in the `app.py` file.

Go into the `app` folder and launch the app. 

```
cd app
python app.py
```

You will get a message with the location where your app is running. 
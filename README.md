# Tradespace Exploration System Web app

The `tradespace_webapp` branch only holds the codebase for running and deploying the web app. 
Please find all other research related material in the `master` branch.

## Installation Instructions

### Prerequisite  Softwares
Please install all software listed below. You should allow all three programs to update your PATH environment variable.
- Python 3.6 (Anaconda Python is strongly recommended by Rhodium and its dependencies. Note that earlier or later versions may not support the features of this software.)
- Git
- [J3](https://github.com/Project-Platypus/J3) (for visualization)
- Anaconda

### Run the web app locally
1. Clone this git repository
- In the command prompt, create a folder where the code repositories will be stored
- Run: `git clone https://github.com/yifz98/farmVal_Rhodium.git`
2. Create conda environment
- In the folder where the repository is cloned, run `conda env create -f tradespace_webapp.yaml`
- Activate the install conda environement by running `conda tradespace_webapp activate`
3. Install Rhodium related libraries to the 'tradespace_webapp' conda environment
- [Rhodium, PRIM, and Platypus](https://github.com/Project-Platypus/Rhodium/blob/master/INSTALL.md) (Follow instructions here)
4. Run Tradespace Exploration Tool Web App
- In the folder where the repository is cloned, `cd web_app`
- Run `flask run`
- The web app will be opend in a browser tab.

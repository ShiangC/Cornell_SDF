# *Tradespace Exploration for Software Defined Farm using RDM*

by *Shiang Chin, Yifan Zhao*

This paper has been submitted for publication in *Journal*.

> Brief description of what the paper is about (the key points).
> You can include a main paper figure here also.  
*Caption for the example figure with the main results.*

## Abstract

The Tradespace Exploration is a decision-support tool developed to find the optimal architectural design for the Software-Defined Farm using a Robust Decision Making framework. This tool can identify potential robust strategies for architectural design, analyze each strategy's vulnerability, and evaluate their attributes under deeply uncertain farming environments. Paired with this, the authors develop a browser-based application to host the trade space exploration functionalities and interfaces for user interactions and data visualizations. Inputting a JSON configuration file, users can define decision space based on specific farm situations. The interactive web interface enables the Tradespace Exploration tool to help different stakeholders with various technology familiarity levels to make key decisions in designing their digital farm systems. This paper provides a software description with an example use case, where the software workflow is demonstrated through a field experiment.

## Code implementation and references

The Tradespace Exploration tool is open-source software, including a client-side browser-based interactive application and a server-side back-end service. The Tradespace Exploration tool is designed and developed in a back-end and front-end setup due to the need for computational resources and data storage in the back-end and the need for a user-friendly interface to lower technology barriers to our various stakeholders. The server-side back-end is developed with Python as the core programming language and hosts most functionalities, including optimization, analytics, and data storage. We selected the Python Flask framework to develop the client-side web application with Javascript as a core programming language. Both the back-end service and the front-end application integrates functionalities from multiple external libraries and custom modules. 

The tool consists of 4 main modules: Decision module, Rhodium module (Hadjimichael et al, 2019), Uncertainty module, and Graphical User Interface (GUI) as seen in Figure XXX. The Decision module defines and maintains the Tradespace Architecture from the Decision Configuration file and hosts the Tradespace Enumeration and Optimization algorithms. Uncertainty module defines the uncertainty variables and models uncertain farming environments using real-time data. Rhodium module hosts functions responsible for extension and orchestration of the integrated third-party Multi-Objective Robust Decision Making (MORDM) libraries and provides key analysis of the Tradespace (Kasprzyk et al., 2019). GUI hosts the front-end interface and handles user data acquisition and visualization.


## Installation Instructions

### Prerequisite  Softwares
Please install all software listed below. You should allow all three programs to update your PATH environment variable.
- Python 3.6 (Anaconda Python is strongly recommended by Rhodium and its dependencies. Note that earlier or later versions may not support the features of this software.)
- Git
- [J3](https://github.com/Project-Platypus/J3) (for visualization)
- Anaconda

### Prerequisite  Libraries
Please install all libraries listed below to your python environment.
- [Rhodium, PRIM, and Platypus](https://github.com/Project-Platypus/Rhodium/blob/master/INSTALL.md) (Follow instructions here)
- OApackage: run `pip install oapackage`
- SKlearn (version lower than 0.22): run `pip install --upgrade scikit-learn==0.20.3`
- [J3py](https://github.com/Project-Platypus/J3Py) : Download and run `python setup.py install`

### Run the code
1. Clone this git repository
- In the command prompt, create a folder where the code repositories will be stored
- Run: `git clone https://github.com/yifz98/farmVal_Rhodium.git`
2. Create conda environment
- In the folder where the repository is cloned, run `conda env create`
4. Run Tradespace Exploration Tool Web Interface
- In the folder where the repository is cloned,
- Run `python app.py`
- Open the web page in the browser.


## Dependencies

> Depending on your project, the script might depend on several other packages
> to run. If using Python, you can use a '.yml' file specifying your dependencies.
> You can create one and place it in the repository so subsequent users take it
> and create a Python environment with all they need to replicate your results.
> This section should then describe how one can set up an environment with the
> dependencies necessary to run your code.

You'll need Python *version number* to run the code.
You can set up an environment with all dependencies using an environment manager
like [Anaconda Python distribution](https://www.anaconda.com/download/) which
provides the `conda` package manager.
Anaconda can be installed in your user directory and does not interfere with
the system Python installation.
The required dependencies are specified in the file `environment.yml`.

Run the following command in the repository folder (where `environment.yml`
is located) to create a separate environment and install all required
dependencies in it:

    conda env create

## Data
> You need to either provide or cite the data used in your analysis.
> Avoid cluttering your repository with a lot of raw data but instead archive and
> mint a DOI for your data.

Hadjimichael, A. (2020). My interesting dataset [Data set]. DataHub. https://doi.org/some-doi-number

## Reproducing the results

> Here you should include all information necessary to reproduce your results.
> Ideally, you'd set up a makefile that automates as much as possible, but make
> sure to provide clear step-by-step instructions for everything.
> The following can be used as example of replicating Python code.

Activate the conda environment:

    source activate ENVIRONMENT_NAME

or, on Windows:

    activate ENVIRONMENT_NAME

To build and test the software, produce all results and figures, follow these steps:

> Add steps here


## License

All source code is made available under a BSD 3-clause license. You can freely
use and modify the code, without warranty, so long as you provide attribution
to the authors.

The manuscript text is not open source. The authors reserve the rights to the
article content, which is currently submitted for publication in the
JOURNAL NAME.

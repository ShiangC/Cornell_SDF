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
- Python 3.9
- Git
- Anaconda


### Run the code
1. Clone this git repository
- In the command prompt, create a folder where the code repositories will be stored
- Run: `git clone https://github.com/yifz98/farmVal_Rhodium.git`
2. Create conda environment
- In the folder where the repository is cloned, run `conda env create -f environment.yml  `
3. Install related packages manually
- [Rhodium, PRIM, and Platypus](https://github.com/Project-Platypus/Rhodium/blob/master/INSTALL.md) (Follow instructions here)
- OApackage: run `python setup.py install` file in 'OApackage-2.7.11' folder.
- [J3py](https://github.com/Project-Platypus/J3Py) : run `python setup.py install` file in 'J3Py-master' folder.
4. Run Tradespace Exploration Tool Web Interface
- In the folder where the repository is cloned,
- Run `python app.py`
- Open the web page in the browser.
- Calculations and plots will be output in 'static'


## License

All source code is made available under a BSD 3-clause license. You can freely
use and modify the code, without warranty, so long as you provide attribution
to the authors.

The manuscript text is not open source. The authors reserve the rights to the
article content, which is currently submitted for publication in the
JOURNAL NAME.

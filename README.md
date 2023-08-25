# PyblioNet

PyblioNet is a software tool for the creation, visualization and analysis of bibliometric networks. It combines a Python-based data collection tool that accesses the Scopus database with a browser-based visualization and analysis tool. It allows users to create networks of publication data based on citations, co-citations, co-authorships, bibliographic coupling, and shared keywords. 


## Description
The first component is a python based data collection tool which downloads publication data from the Scopus database via [Pybliometrics](https://pybliometrics.readthedocs.io/en/stable/). Initial Scopus search is done by the user via advanced search query strings using the scopus search api. Based on this initial publication data, further information on cited and citing research are collected which e.g. allows for computing bibliographic coupling and co-citation relationships for the initial publication data (using the scopus Abstract Retrieval API and scopus Search API). The publication data is then used to create a network where each publication is represented as a node in the network. Relationships are computed based on citation analysis, co-citation analysis, co-authorship analysis, bibliographic coupling and keyword analysis.

The second component is a html / JavaScript analysis and visualisation tool building on the [VisJs](https://visjs.github.io/vis-network/docs/network/) Package. In the network each node represents a publication. Each edge represents a relation between two publications. Nodes’ positions are calculated via a force-directed or hierarchical layout algorithm. The analysis tool allows for filtering, and graphical analysis. Filtering can be done based on publication date, degree centrality or weight etc. Graphical analysis covers e.g. searching and highlighting nodes based on user input, community detection based on a louvain cluster detection method etc.

![example chart](Examples/PyblioNetV0.8.png)

## Usage

Users can use PyblioNet by executing a Python file, which requires the installation of the libraries such as Pybliometrics [Pybliometrics](https://pybliometrics.readthedocs.io/en/stable/), NetworkX [NetworkX](https://github.com/networkx/networkx), etc. Alternatively, users can run the exe file, which includes all necessary libraries. 

For the first use, users need to enter a valid Scopus API key in order to access the database via Pybliometrics ([Scopus APi key](https://dev.elsevier.com/sc_apis.html)). After that, users can start by entering Scopus advanced search query strings. PyblioNet will display how many publications were found using the search query and ask the user if they want to continue. If so, the user can continue with a standard setting, or with an advanced mode where the user can decide on the following settings: 
-	Minimum citation count: exclude search results based on their citations. (standard: 0)
-	Use cached data if possible: download publication data even if it is data cached on your computer. (default: yes)
-	Download information about citing papers: downloading information on publications citing the search results is necessary for co-citation analysis but takes additional time. (default: yes)
-	Create extra nodes for references and citing papers: creating extra nodes for references and citing papers can result in huge networks that may be too large to visualize. If the user chooses “later”, PiblioNet will ask for a minimum occurrence of extra nodes for references and citing papers. (default: yes)
-	Download abstracts: downloading abstracts for search results increases the size of the html file and takes additional time. (default: yes)
-	Minimum weight for bibliographic coupling: include bibliographic coupling links between publications only if there are at least x shared references (reduces network size). (default: 0)
-	Minimum weight for co-citation: include co-citation links between publications only if there are at least x shared citing publications (reduces network size). (default: 0)
-	Minimum weight for shared keywords: include shared keyword links between publications only if there are at least x shared keywords (reduces network size). (default: 0)
-	Create Gephi file: Creates an additional .gexf file of the network which can be opened in Gephi. (default: no)


Start the .py or .exe file. Upon first usage you will need to enter a . Afterwards, simply enter your search term and follow the instructions. PyblioNet will create a html file with the resulting network.


## Installation
Download the .py and template.html file. Make sure they are in the same directory and run the Python file. Alternatively to the python file you can download the .exe and run it.

## Support
Contact: m_mueller@uni-hohenheim.de



## License
MIT License; see [LICENSE](https://aidaho-edu.uni-hohenheim.de/gitlab/M_Mueller/pyblionet/-/blob/main/license).



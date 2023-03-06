# PyblioNet


## Name
Pyblionet

## Description
Biblionet covers two main components. The first component is a python based data collection tool which downloads publication data from the Scopus database via [Pybliometrics](https://pybliometrics.readthedocs.io/en/stable/). Initial Scopus search is done by the user via advanced search query strings using the scopus search api. Based on this initial publication data, further information on cited and citing research are collected which e.g. allows for computing bibliographic coupling and co-citation relationships for the initial publication data (using the scopus Abstract Retrieval API and scopus Search API). The publication data is then used to create a network where each publication is represented as a node in the network. Relationships are then computed based on citation analysis, co-citation analysis, co-authorship analysis, bibliographic coupling, co-word analysis and keyword analysis.

The second component is a html / JavaScript analysis and visualisation tool building on the [VisJs](https://visjs.github.io/vis-network/docs/network/) Package. In the network each node represents a publication. Each edge represents a citation relation between two publications. Nodes’ positions are calculated via a force-directed or hierarchical layout algorithm. The analysis tool allows for filtering, and graphical analysis. Filtering can be done based on publication date, degree centrality or weight etc. Graphical analysis covers e.g. searching and highlighting nodes based on user input, community detection based on a louvain cluster detection method.

## Installation
Download the .py and template.html file. Make sure they are in the same directory and run the Python file.

## Support
Contact: m_mueller@uni-hohenheim.de

## License
MIT License; see [LICENSE](https://aidaho-edu.uni-hohenheim.de/gitlab/M_Mueller/pyblionet/-/blob/main/license).



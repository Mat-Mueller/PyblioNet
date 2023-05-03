Description
============

Pyblionet covers two main components. The first component is a python based data collection tool which downloads publication data from the Scopus database via Pybliometrics. Initial Scopus search is done by the user via advanced search query strings using the scopus search api. Based on this initial publication data, further information on cited and citing research are collected which e.g. allows for computing bibliographic coupling and co-citation relationships for the initial publication data (using the scopus Abstract Retrieval API and scopus Search API). The publication data is then used to create a network where each publication is represented as a node in the network. Relationships are computed based on citation analysis, co-citation analysis, co-authorship analysis, bibliographic coupling and keyword analysis.
The second component is a html / JavaScript analysis and visualisation tool building on the VisJs Package. In the network each node represents a publication. Each edge represents a relation between two publications. Nodes’ positions are calculated via a force-directed or hierarchical layout algorithm. The analysis tool allows for filtering, and graphical analysis. Filtering can be done based on publication date, degree centrality or weight etc. Graphical analysis covers e.g. searching and highlighting nodes based on user input, community detection based on a louvain cluster detection method etc.

Installation
============
Download the .py and template.html file. Make sure they are in the same directory and run the Python file. Alternatively to the python file you can download the .exe and run it.

Usage
======
Start the .py or .exe file. Upon first usage you will need to enter a Scopus APi key. Afterwards, simply enter your search term and follow the instructions. PyblioNet will download all relevant data and create a html file with the resulting network.

Data collection tool
====================
PyblioNet downloads publication data from the Scopus database via the Pybliometrics library (see https://github.com/pybliometrics-dev/pybliometrics). Based on an initial set of publications (obtained via a Scopus advanced search query string), further information on cited and citing research is collected, allowing, for example, the determination of bibliographic coupling and co-citation relationships (using the Scopus Abstract Retrieval API and Scopus Search API). 

Web-based analysis and visualisation tool 
=========================================
The publication data obatined by the data collection tool is used to create networks of publications, where each publication is represented as a node and the relationships between nodes (e.g. shared keywords, citations, references, etc.) are visualised by links connecting the nodes. Within the tool users can:
* Filter nodes by type: e.g. show only nodes representing the main search results / show main search results + their references / show main search results + citing publications / etc.
* Filter nodes by minimum degree: exclude all nodes with a degree smaller than user-input (the degree of a node refers to the nodes' current number of links)
* Filter nodes by publication year: include only nodes with a punblication date within the set range
* Filter edges by relation: Choose the network you want to visualize. CoAuthor: publications are connected if they share one or more authors; Citation: publications are connected if one cites the other; BiblioCoupling: publications are connected if they share one or more references; CoCitation: publications are connected if they share one or more citing publications; Keywords: publications are connected if they share one or more keywords.
* Filter edges by weight: In case of bibliografic-coupling, co-citation and keyword relationships you can filter edges by minimum occurence.
* Recolor nodes: Nodes are recolored based on a Louvain community detection algorithm.
* Search for nodes: enter a search term to highlight specific nodes.
* Delete selected nodes: select nodes by clicking on them (for a selection of multiple nodes, hold Ctrl and click).
* Force-directed layout algorithm: Turn on/off the force-directed layout algorithm that places well-connected nodes in the centre of the network and less well-connected nodes at the periphery.
* Hierarchical layout: y-coordinate of nodes in the canvas is based on the year of publication, placing older publications at the top and newer ones at the bottom.
* Color by Journal: recolour nodes based on the publishing journal.

* Export: exporting the network data to a Gephi-compatible file format.

* Misc: Within PyblioNet you can manual reposition nodes, hover over nodes to get more information such as abstracts, keywords, etc., highlighting nodes and their direct peers by clicking on a node, and double-click on a node for a quick access to the publication directly from the publisher (based on the publication's DOI or, if not available, opens google scholar with the publication title as a search query).






Support
=======
Contact: m_mueller@uni-hohenheim.de

License
=======
MIT License

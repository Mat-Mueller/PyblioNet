from pybliometrics.scopus import AbstractRetrieval
import networkx as nx
from pybliometrics.scopus import ScopusSearch
from collections import Counter



## The whole package includes 3 major steps: (1) get data from scopus; (2) compute network relations and (3) copy the information into an html file containing filters etc.


##############################################################
#################### get search results ###äää################
##############################################################

# ask for user-input as scopus search-string; results ("s") are a list of papers with ID, authors, Year, etc.  no references, abstract or citing papers are included yet

answer = "n"
while answer == "n":
   searchstring = input("enter search string, e.g. TITLE-ABS-KEY ( (\"innovation diffusion\" OR \"diffusion of innovation\")  AND  (agent-based OR multi-agent ))  \n")
   if searchstring == "1":  # for quick testing
       searchstring = "TITLE-ABS-KEY ( innovation  AND diffusion  AND  agent-based  AND modelling ) AND (SRCTYPE(j) OR SRCTYPE(b) )" # AND PUBYEAR #AFT 1993
   try:
       s = ScopusSearch(searchstring, download=False)
       nr_results = (s.get_results_size())
       print("found " + str(nr_results) + " results. Do you want to proceed?")
       answer = input("y/n: ")
   except:

       print("Error when checking the search string")

#searchstring = (values[0])
# print(searchstring)
if searchstring == "1":  # for quick testing
    searchstring = "TITLE-ABS-KEY ( (\"innovation diffusion\" OR \"diffusion of innovation\")  AND  (agent-based OR multi-agent ))"  # AND PUBYEAR #AFT 1993
try:
    s = ScopusSearch(searchstring, download=False)
except:
    pass
mode_cit =  input("Do you want to download information on citing papers? This is necessary for Co-citation... \n" + "y/n: ")
extra_nodes =  input("Do you want create extra nodes for references and citing papers? \n" + "(y)es/(n)o/(a)sk later: ")
abstracts =  input("Do you want to download abstracts? \n" + "y/n: ")
#gephi = input("Do you want to export network to a Gephi? \n" + "y/n: ")

s = ScopusSearch(searchstring, download=True, verbose=True)

print("Getting main search results")


master_dict = {}  # main data dict, example for an entry here:  paperX:  {'AUTHOR-IDS': ['57360871800', '55968604500', '23003196400'], 'REFS': {'85140452566': [None, '', None, None, None, None], '85140454703': [None, 'ARIA', None, 'European scale of industrial accidents - Reference for experience feedback of technical accidents', None, None], '84946592829': ['7006694977', 'Babrauskas, Vytenis', None, 'Explosions of ammonium nitrate fertilizer in storage or transportation are preventable accidents', 'Journal of Hazardous Materials', '10.1016/j.jhazmat.2015.10.040'], '85029006306': ['7006694977; 7006694977', 'Babrauskas, Vytenis; Babrauskas, Vytenis', None, 'The West, Texas, ammonium nitrate explosion: A failure of regulation', 'Journal of Fire Sciences', '10.1177/0734904116685723'], '85091687537': [None, 'Babrauskas', None, 'The emergency response guidebook (ERG): not good enough, not safe enough', 'Fire Eng.', None], '85077371020': ['7006694977; 7006694977; 57213877899', 'Babrauskas, Vytenis; Babrauskas, Vytenis; Leggett, David', None, 'Thermal decomposition of ammonium nitrate', 'Fire and Materials', '10.1002/fam.2797'], '85115367870': [None, 'Baraer', None, 'The impact of climate events on French industrial facilities between 2010 and 2019', 'Loss Prev. Bull.', None], '85132371039': ['36652291200; 7102822591; 6602124378; 57754132800', 'Baraza, Xavier; Giménez, Jaime; Pey, Alexis; Rubiales, Miriam', None, 'Lessons learned from the Barracas accident: Ammonium nitrate explosion during road transport', 'Process Safety Progress', '10.1002/prs.12396'], '84973576945': [None, 'Bartzokas', None, 'Technological Change and Corporate Strategies in the Fertilizer Industry', None, None], '71049128094': ['57216034585; 57165511400', 'Baum; Clement', None, 'The changing structure of the fertilizer industry in the united states', 'American Journal of Agricultural Economics', '10.2307/1234991'], '85103789237': ['6701527775; 6603551183; 7203036818', 'Ale, Ben J.M.; Hartford, Des N.D.; Slater, David H.', None, 'Prevention, precaution and resilience: Are they worth the cost?', 'Safety Science', '10.1016/j.ssci.2021.105271'], '0001464557': ['7005324157; 7004427947; 15121785200', 'Brower; Oxley, Jimmie C.; Tewari, Mohan', None, 'Evidence for homolytic decomposition of ammonium nitrate at high temperature', 'Journal of Physical Chemistry®', '10.1021/j100347a033'], '85140469246': [None, 'CAS', None, 'Ammonium Nitrate Explosions: Lessons Learned', None, None], '84863904482': ['36998451500; 36952845600', 'Chaturvedi, Shalini; Dave, Pragnesh N.', None, 'Review on Thermal Decomposition of Ammonium Nitrate', 'Journal of Energetic Materials', '10.1080/07370652.2011.573523'], '85072563045': ['57211074524; 13408025900; 35489746600', 'Chen, Qiaoling; Wood, Maureen; Zhao, Jinsong', None, 'Case study of the Tianjin accident: Application of barrier and systems analysis to understand challenges to industry loss prevention in emerging economies', 'Process Safety and Environmental Protection', '10.1016/j.psep.2019.08.028'], '85113337677': ['57215024539; 57209771605; 57227968600; 57227782800', 'Cimer, Zsolt; Vass, Gyula; Kátai-Urbán, Lajos; Zsitnyányi, Attila', None, 'Application of chemical monitoring and public alarm systems to reduce public vulnerability to major accidents involving dangerous substances', 'Symmetry', '10.3390/sym13081528'], '85140486148': [None, 'Conradt', None, None, None, None], '85140443074': [None, 'CSB', None, 'FINAL REPORT: West Fertilizer Final Investigation Report', None, None], '85140470182': [None, 'Data Bridge Market Research', None, 'Global Ammonium Nitrate Market – Industry Trends and Forecast to 2027', None, None], '85140487484': [None, '', None, None, None, None], '85087908529': ['56308398600; 55431371400; 7402008246', 'Ding, Long; Ji, Jie; Khan, Faisal', None, 'A novel approach for domino effects modeling and risk analysis based on synergistic effect and accident evidence', 'Reliability Engineering and System Safety', '10.1016/j.ress.2020.107109'], '85140491015': [None, 'Dolah; Moson; Perzak', None, 'Explosion Hazards of Ammonium Nitrate Under Fire Exposure. Washington, DC: U.S. Department of the Interior', 'Bureau of Mines.', None], '85007613543': ['57192712211; 7402008246; 57192720167; 25959875100', 'El-Gheriani, Malak; Khan, Faisal; Chen, Dan; Abbassi, Rouzbeh', None, 'Major accident modelling using spare data', 'Process Safety and Environmental Protection', '10.1016/j.psep.2016.12.004'], '85064080082': ['6701768312; 57208450315; 6504258439; 34572074500; 6504391553; 7006090884; 57208450315; 7801567129; 6504258439; 6504258439; 39462122000; 39462122000; 7006090884', 'Elmqvist, Thomas; Andersson, Erik; McPhearson, Timon; Olsson, Per; Gaffney, Owen; Folke, Carl; Andersson, Erik; Frantzeskaki, Niki; McPhearson, Timon; McPhearson, Timon; Takeuchi, Kazuhiko; Takeuchi, Kazuhiko; Folke, Carl', None, 'Sustainability and resilience for transformation in the urban century', 'Nature Sustainability', '10.1038/s41893-019-0250-1'], '84886905649': [None, 'Elvers; Hawkins; Russey', None, None, "Ullmann's Encyclopedia of Industrial Chemistry", None], '84946550465': [None, 'EPA', None, 'Explosion Hazard from Ammonium Nitrate, EPA 550-F-97-002d', None, None], '85140449165': [None, 'ERA Environmental Management Solutions', None, 'OSHA HCS 2015: The Consequences of Noncompliance', None, None], '85140442333': [None, '', None, None, None, None], '85140437197': [None, 'Essig', None, None, None, None], '85140454438': [None, '', None, None, None, None], '85140453314': [None, '', None, None, None, None], '85058577081': ['55659850100; 24333140600', 'Fang, Yi-Ping; Sansavini, Giovanni', None, 'Optimum post-disruption restoration under uncertainty for enhancing critical infrastructure resilience', 'Reliability Engineering and System Safety', '10.1016/j.ress.2018.12.002'], '85140460932': [None, 'Fernandes; Kulaif', None, None, None, None], '85105321874': ['35748502300; 57194784479; 56785064300; 57223218845', 'Filho, Anastacio Pinto Goncalves; Ferreira, Adonias Magdiel Silva; Ramos, Magna Fernandes; Pinto, Anderson Rogério Albuquerque Pontes', None, 'Are we learning from disasters? Examining investigation reports from National government bodies', 'Safety Science', '10.1016/j.ssci.2021.105327'], '85140467119': [None, '', None, None, None, None], '85111463872': ['57226399403', 'Fisher, Len', None, 'To build resilience, study complex systems', 'Nature', '10.1038/d41586-021-01925-9'], '85140480554': [None, 'Future Market Insights Inc', None, 'Ammonium Nitrate Market 2018–2028: Mining Industry to Stimulate Revenue Growth', None, None], '85092599046': ['57226263190', 'Guiochon, Georges', None, 'On the catastrophic explosion of the AZF plant in Toulouse', 'Process Safety Progress', '10.1002/prs.12197'], '85047688195': ['16056319800', 'Hainer', None, 'The application of kinetics to the hazardous behavior of ammonium nitrate', 'Symposium (International) on Combustion', '10.1016/S0082-0784(55)80032-X']}, 'TITLE': ['Yue, Yue;Gai, Wenmei;Boustras,', '2023', 'Exploration of the causes of ammonium nitrate explosions: Statistics and analysis of accidents over the past 100 years', 'Safety Science', '10.1016/j.ssci.2022.105954'], 'DOI': '10.1016/j.ssci.2022.105954', 'ABSTRACT': None, 'KEYWORDS': ['ammonium nitrate', 'emergency response', 'explosions', 'information deviation', 'regulation'], 'CITS': {}}

total_refs = []  # additional list used to filter for references and citing papers
total_cits = []  # additional list used to filter for references and citing papers

# loop through found papers to get the references and citing papers
print("Getting references and citing papers")

counter = 0
print("loading information for paper: ", end=" ")

print("")
# print(s)
for paper in s.results:
    counter += 1
    print("\r", str(int((counter) / nr_results * 100)) + "%" , end=" ")
    paper_dict = {}  # create a temporary dictionary for each paper where informations are stored
    try:
        paper_dict["AUTHOR-IDS"] = paper.author_ids.split(sep=";")  # if there are author IDs for a paper x in S
    except:
        paper_dict["AUTHOR-IDS"] = ""
    try:
        ab = AbstractRetrieval(paper.eid, id_type="eid", view="REF",
                               refresh=False, startref="0")  # use different package to get references of paper.
    except:
        ab = None

    #paper_dict["CITED_BY"] = ab.citedby_count
    if abstracts != "n":
        abstract_info = AbstractRetrieval(paper.eid, id_type="eid", view="FULL",
                               refresh=False)
        paper_dict["ABSTRACT"] = abstract_info.abstract
    else:
        paper_dict["ABSTRACT"] = ""


    if ab is not None and ab.references is not None :  # if we found references
        TotalRefCount = (ab.refcount)

        #print("found: " + str(TotalRefCount) + "References")
        CheckedRefsCount = 0
        ref_dict = {}  # create a temporary second dictionary for the references, this dict will later be included in paper_dict
        paper_dict["REFS"] = {}
        CheckedRefsCount += len(ab.references)
        for reference in ab.references:  ## fill the ref_dict with a list of references, each element is again a list of the main information, e.g. authors, years, title etc
            #print(reference)

            if reference.id is not None:
                ref_dict[reference.id] = [reference.authors_auid, (reference.authors), str(reference.coverDate)[:4],
                                              (reference.title), (reference.sourcetitle), (reference.doi)]  # title
                total_refs.append(reference.id)
        while TotalRefCount > CheckedRefsCount:

            ab = AbstractRetrieval(paper.eid, id_type="eid", view="REF",
                                   refresh=False, startref=str(CheckedRefsCount + 1), refcount=0)
            CheckedRefsCount += len(ab.references)
            for reference in ab.references:  ## fill the ref_dict with a list of references, each element is again a list of the main information, e.g. authors, years, title etc
                if reference.id is not None:
                    ref_dict[reference.id] = [reference.authors_auid, (reference.authors), str(reference.coverDate)[:4],
                                                  (reference.title), (reference.sourcetitle), (reference.doi)]  # title
                    total_refs.append(reference.id)

        paper_dict["REFS"] = ref_dict

    else:
        paper_dict["REFS"] = {}


    paper_dict["TITLE"] = [str(paper.author_names)[:100], str((paper.coverDate))[:4], (paper.title),
                           (paper.publicationName), paper.doi]
    paper_dict["DOI"] = paper.doi
    paper_dict["year"] = str((paper.coverDate))[:4]
    # print(paper_dict["YEAR"])

    temp_keyword = str(paper.authkeywords).lower().split(" | ")
    paper_dict["KEYWORDS"] = temp_keyword if temp_keyword[0] != "none" else []

    ## getting  citing papers
    if mode_cit != "n":  # if user has decided to get information on the citing papers
        ##getting citing paper
        s = ScopusSearch(f"REF({str(paper.eid)})")  # use main package via a searchstring
        try:
            citing = s.results[:200000]
        except:
            citing = None
        cit_dict = {}
        if citing != None:
            for citing_paper in citing:
                total_cits.append(str(citing_paper.eid).replace("2-s2.0-", ""))
                try:
                    cit_dict[str(citing_paper.eid).replace("2-s2.0-", "")] = [citing_paper.author_ids.split(sep=";"),
                                                                              citing_paper.author_names,
                                                                              str(citing_paper.coverDate)[:4],
                                                                              (citing_paper.title),
                                                                              (citing_paper.publicationName),
                                                                              citing_paper.doi]
                except:
                    cit_dict[str(citing_paper.eid).replace("2-s2.0-", "")] = ["", citing_paper.author_names,
                                                                              str(citing_paper.coverDate)[:4],
                                                                              (citing_paper.title),
                                                                              (citing_paper.publicationName),
                                                                              citing_paper.doi]

        paper_dict["CITS"] = cit_dict
    else:
        paper_dict["CITS"] = {}

    # if counter == 10: print(paper_dict)
    master_dict[str(paper.eid).replace("2-s2.0-",
                                       "")] = paper_dict  # store all information gathered here in our main dictionary with paper ID as Key

print("done")
print("downloaded " + str(len(total_refs)) + " references and " + str(len(total_cits)) + " citing papers")
##############################################################
################## generate NetworkX network #################
##############################################################


#here you can filter to include only most frequent references and citing papers
extra_nodes_no = 0
if extra_nodes == "a":
    extra_nodes_no = input("Minimum occurence for extra nodes for references and citing papers? \"\n" + ": ")



total_refs = [item[0] for item in Counter(total_refs).most_common() if
              item[1] > int(extra_nodes_no) and item[0] not in master_dict.keys()]
total_cits = [item[0] for item in Counter(total_cits).most_common() if
              item[1] > int(extra_nodes_no) and item[0] not in master_dict.keys()]

print("make network")
print(print("will use " + str(len(total_refs)) + " references and " + str(len(total_cits)) + " citing papers"))

G = nx.DiGraph()  # create an empty networkX graph

biblio_vs_coit = []

print("create  nodes")
for node in (master_dict.keys()):
    # creating main nodes and transfer information from database

    G.add_node(node,
               myauth=master_dict[node]["AUTHOR-IDS"],
               year=master_dict[node]["year"],
               title=master_dict[node]["TITLE"],
               myrefs=master_dict[node]["REFS"].keys(),
               mycits=master_dict[node]["CITS"].keys(),
               myabstract=master_dict[node]["ABSTRACT"],
               type="main",
               color="#6495ED",
               keywords=master_dict[node]["KEYWORDS"],
               url=master_dict[node]["TITLE"][4],
               checked=[],
               #citen_by=master_dict[node]["CITED_BY"]
               )
    if extra_nodes != "n":  # if the user wants to, create nodes for the references and citing papers
        for temp_ref_id in master_dict[node]["REFS"].keys():
            if temp_ref_id in total_refs and temp_ref_id not in master_dict.keys():
                try:
                    temp_auth = (master_dict[node]["REFS"][temp_ref_id][0].split(sep=";"))
                except:
                    temp_auth = ""
                G.add_node(temp_ref_id,
                           myauth=temp_auth,
                           title=(master_dict[node]["REFS"][temp_ref_id][1:]),
                           year=(master_dict[node]["REFS"][temp_ref_id][2]),
                           type="REF",
                           color="#DE3163",
                           url=(master_dict[node]["REFS"][temp_ref_id][5]),
                           checked=[],
                           keywords = [],
                           )
                total_refs.remove(temp_ref_id)
        for temp_cit_id in master_dict[node]["CITS"].keys():
            if temp_cit_id in total_cits and temp_cit_id not in master_dict.keys():
                #print(str(master_dict[node]["CITS"][temp_cit_id][2])[:4])
                G.add_node(temp_cit_id,
                           myauth=(master_dict[node]["CITS"][temp_cit_id][0]),
                           title=(master_dict[node]["CITS"][temp_cit_id][1:]),
                           year=str(master_dict[node]["CITS"][temp_cit_id][2])[:4],
                           type="CIT",
                           color="#1a762c",
                           url=(master_dict[node]["CITS"][temp_cit_id][5]),
                           checked=[],
                           keywords=[],
                           )
                total_cits.remove(temp_cit_id)

print("create  links")
# csvFile = open("Konstantin_Innovation_diffusion.csv", "a", newline="", encoding='utf-8')  ## opens a new csv file
# csvWriter = csv.writer(csvFile)
# csvWriter.writerow(["id","Coauth", "cited", "biblio", "Cocit", "Keywords", "time", "same_journal"])


counter = 0
for node, info in G.nodes(data=True):  # foreach node
    if G.nodes[node].get(
            "type") == "main":  # if its not a reference or citing paper as we dont include information inbetween references etc.
        myauth = set(info["myauth"])  # store node's information in temporary variables to speed things up
        myrefs = (info["myrefs"])
        mycits = (info["mycits"])
        mykeys = info["keywords"]
        mytime = info["title"][1]
        myjournal = info["title"][3]
        # if counter / 100 == int(counter / 100):
        #     print(counter)
        # counter += 1
        for node_r, info2 in G.nodes(data=True):  # loop through all other nodes
            if node != node_r:
                myauth2 = set(info2["myauth"])

                # create edges. edges also have information on the nature of the relationship

                ## cited
                if node_r in myrefs:  # if second node is in my list of references
                    G.add_edge(node, node_r, cited=True)
                if node_r in mycits:  # if second node is in my list of citing papers
                    G.add_edge(node_r, node, cited=True)


                ## same authors
                if len(list(myauth.intersection(
                        myauth2))) > 0:  # if the intersection between list of authors of A and B is bigger 0
                    G.add_edge(node_r, node, coauth=True)  # create edge


                if G.nodes[node_r].get("type") == "main":  # for the fun stuff use again temporary variables
                    myrefs2 = (info2["myrefs"])
                    mycits2 = (info2["mycits"])
                    mykeys2 = info2["keywords"]
                    mytime2 = info2["title"][1]
                    myjournal2 = info2["title"][3]
                    ##biblio_vs_coit.append([ len(list(myauth.intersection(myauth2))), 1 if node_r in myrefs or node_r in mycits else 0 ,  len(list(set(myrefs).intersection(set(myrefs2)))), len(list(set(mycits).intersection(set(mycits2)))), len(list(set(mykeys).intersection(set(mykeys2)))), (int(mytime) - int(mytime2)), 1 if myjournal == myjournal2 else 0])
                    # csvWriter.writerow([str(node) + "and" + str(node_r) ,len(list(myauth.intersection(myauth2))), 1 if node_r in myrefs or node_r in mycits else 0 ,  len(list(set(myrefs).intersection(set(myrefs2)))), len(list(set(mycits).intersection(set(mycits2)))), len(list(set(mykeys).intersection(set(mykeys2)))), (int(mytime) - int(mytime2)), 1 if myjournal == myjournal2 else 0])

                    ## same reference

                    temp = len([x for x in myrefs if x in myrefs2])  # len(list(set(myrefs).intersection(set(myrefs2))))
                    if temp > 0:
                        G.add_edge(node_r, node, BiblioCoup=True, Biblio_strength=temp)
                    # Co-citation
                    temp = len([x for x in mycits if x in mycits2])  # len(list(set(mycits).intersection(set(mycits2))))
                    if temp > 0:
                        G.add_edge(node_r, node, CoCit=True,
                                   cocit_strength=temp)
                    # Keywords
                    temp = len([x for x in mykeys if x in mykeys2])  # len(list(set(mykeys).intersection(set(mykeys2))))
                    if temp > 0:
                        G.add_edge(node_r, node, KeyWord=True,
                                   keyword_strength=temp)
print(G)





# if gephi == "y":
#     G2 = G
#     for node, info in G2.nodes(data=True):
#         del G2.nodes[node]["myauth"]
#         if G.nodes[node].get("type") == "main":
#             del G.nodes[node]["myrefs"]
#             del G2.nodes[node]["mycits"]
#         del G2.nodes[node]["checked"]
#         del G2.nodes[node]["keywords"]
#         G2.nodes[node]["title"] = G2.nodes[node].get("title")[0]
#
#     filename_gephi = input("Filename? \n"   )
#     print(filename_gephi)
#     nx.write_gexf(G2, filename_gephi)


###### overwrite the list of nodes and edges in our template html by transforming our information from the NetworkX network to lists

list_node_dict = []  # temporary variables used to store information
list_edge_dict = []  # temporary variables used to store information
for node, info in G.nodes(data=True):
    node_dict = {}
    del G.nodes[node]["myauth"]
    if G.nodes[node].get("type") == "main":
        del G.nodes[node]["myrefs"]
    node_dict["color"] = G.nodes[node].get("color")
    node_dict["color2"] = G.nodes[node].get("color2") if G.nodes[node].get(
        "color2") is not None else "#d3d3d3"  # ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
    if G.nodes[node].get("type") == "main":
        node_dict["cited_by"] = len(G.nodes[node].get("mycits"))
        node_dict["shape"] = "dot"
    if G.nodes[node].get("year") != None:
        node_dict["level"] = G.nodes[node].get("year")
    else:
        node_dict["level"] = "0000"

    node_dict["id"] = node
    node_dict["keywords"] = G.nodes[node].get("keywords")
    node_dict["size"] = 10
    if G.nodes[node].get("type") == "REF":
        #node_dict["size"] = 5 + G.degree[node]
        node_dict["shape"] = "triangle"
    if G.nodes[node].get("type") == "CIT":
        node_dict["shape"] = "star"
        #node_dict["size"] = 5 + G.degree[node]
    node_dict["journal"] = str(G.nodes[node].get("title")[3])
    node_dict["title"] = " \n ".join([str(x)[:200] for x in G.nodes[node].get("title") if (x) != None]) + \
                         "\n Keywords: " + '\n'.join(
        str(G.nodes[node].get("keywords"))[i:i + 100] for i in range(0, len(str(G.nodes[node].get("keywords"))), 100)) + \
                         "\n Abstract: " + '\n'.join(str(G.nodes[node].get("myabstract"))[i:i + 100] for i in
                                                           range(0, len(str(G.nodes[node].get("myabstract"))), 100)) + "\n DOI: " + str(G.nodes[node].get("url"))
    #node_dict["label"] = " ".join([str(x)[:20] for x in G.nodes[node].get("title")[:2] if (x) != None])
    node_dict["type"] = G.nodes[node].get("type")
    node_dict["label"] = " ".join([str(x)[:20] for x in G.nodes[node].get("title")[:2] if (x) != None])
    if str((G.nodes[node].get("url"))) != "None":
        node_dict["url"] = "https://doi.org/" + str(G.nodes[node].get("url"))
    else:
        node_dict["url"] = "https://scholar.google.de/scholar?q=" + str(G.nodes[node].get("title")) + "\""
    #node_dict["degree"] = G.degree[node]
    list_node_dict.append(node_dict)

list_edge_dict = []
for edge, edge2, info in G.edges(data=True):
    edge_dict = {}
    edge_dict["from"] = edge
    edge_dict["to"] = edge2
    if G.edges[edge, edge2].get("cited") == True:
        edge_dict["cited"] = "true"
    if G.edges[edge, edge2].get("BiblioCoup") == True:
        edge_dict["BiblioCoup"] = "true"
    if G.edges[edge, edge2].get("coauth") == True:
        edge_dict["coauth"] = "true"
    if G.edges[edge, edge2].get("CoCit") == True:
        edge_dict["CoCit"] = "true"
    if G.edges[edge, edge2].get("KeyWord") == True:
        edge_dict["KeyWord"] = "true"
    try:
        if G.edges[edge, edge2].get("Biblio_strength") >= 0:
            edge_dict["Biblio_strength"] = G.edges[edge, edge2].get("Biblio_strength")
    except:
        edge_dict["Biblio_strength"] = 0

    try:
        if G.edges[edge, edge2].get("cocit_strength") >= 0:
            edge_dict["cocit_strength"] = G.edges[edge, edge2].get("cocit_strength")
    except:
        edge_dict["cocit_strength"] = 0
    try:
        if G.edges[edge, edge2].get("keyword_strength") >= 0:
            edge_dict["keyword_strength"] = G.edges[edge, edge2].get("keyword_strength")
    except:
        edge_dict["KeyWord_strength"] = 0

    list_edge_dict.append(edge_dict)

node_list = "nodes = new vis.DataSet(" + str(list_node_dict) + ")"
edge_list = "edges = new vis.DataSet(" + str(list_edge_dict) + ")"

file = open("PyblioNet_templateV0.7.html", "r", encoding="utf-8")
replacement = ""
for line in file:
    line = line.strip()
    changes = line
    if "YourSearchTerm" in line:
        changes = str(searchstring)
    if "edges = new vis.DataSet([{" in line:
        changes = edge_list
    if "nodes = new vis.DataSet([{" in line:
        changes = node_list
    replacement = replacement + changes + "\n"

file.close()
# opening the file in write mode
fout = open(searchstring.replace(" ", "").replace("\"", "").replace("*", "")[:60] + "_final.html", "w",
            encoding="utf-8")
fout.write(replacement)
fout.close()




#
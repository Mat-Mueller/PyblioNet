from pybliometrics.scopus import AbstractRetrieval
import networkx as nx
from pybliometrics.scopus import ScopusSearch
from collections import Counter
from tqdm import tqdm
import webbrowser
import textwrap
from itertools import combinations



## The whole package includes 3 major steps: (1) get data from scopus; (2) compute network relations and (3) copy the information into an html file containing filters etc.


##############################################################
#################### get search results ###äää################
##############################################################


# ask for user-input as scopus search-string; results ("s") are a list of papers with ID, authors, Year, etc.  no references, abstract or citing papers are included yet

answer = "n"
while answer == "n":
   searchstring = input("enter search string, e.g. TITLE-ABS-KEY ( (\"innovation diffusion\" OR \"diffusion of innovation\")  AND  (agent-based OR multi-agent ))  \n")
   if searchstring == "1":  # for quick testing
       searchstring = "TITLE-ABS-KEY((\"innovation diffusion\" OR \"diffusion of innovation\")  AND  (agent-based OR multi-agent OR \"agent based\" ))"
   try:
       s = ScopusSearch(searchstring, download=False)
       nr_results = (s.get_results_size())
       print("found " + str(nr_results) + " results. Do you want to proceed?")
       answer = input("(y)es/(a)dvanced/(n)o: ")
   except Exception as e:
       print("An unexpected error occurred:", e)



if answer == "a":
    min_cit = input("Minimum citation count: \n")
    refresh = input("Use cached data if possible:  \n" + "y/n: ")
    mode_cit =  input("Do you want to download information on citing papers? This is necessary for Co-citation... \n" + "y/n: ")
    extra_nodes =  input("Do you want create extra nodes for references and citing papers? \n" + "(y)es/(n)o/(a)sk later: ")
    abstracts =  input("Do you want to download abstracts? \n" + "y/n: ")
    min_weight_biblio = (input("Minimum weight for bibliographic coupling? \n"))
    min_weight_cocit = (input("Minimum weight for co-citation? \n"))
    min_weight_key = (input("Minimum weight for shared keywords? \n"))
    if not (min_weight_biblio).isnumeric():
        min_weight_biblio = 0
    else:
        min_weight_biblio = int(min_weight_biblio)
    if not (min_weight_cocit).isnumeric():
        min_weight_cocit = 0
    else:
        min_weight_cocit = int(min_weight_cocit)
    if not (min_weight_key).isnumeric():
        min_weight_key = 0
    else:
        min_weight_key = int(min_weight_key)
    if refresh == "n":
        refresh = True
    else:
        refresh = False

else:
    min_cit = "0"
    mode_cit =  ""
    extra_nodes = ""
    abstracts =  ""
    min_weight_biblio = 0
    min_weight_cocit = 0
    min_weight_key = 0
    refresh = False
#gephi = input("Do you want to export network to a Gephi? \n" + "y/n: ")

s = ScopusSearch(searchstring, download=True, verbose=True, refresh=refresh)

print("Getting main search results")

master_dict = {}  # main data dict, example for an entry here:  paperX:  {'AUTHOR-IDS': ['57360871800', '55968604500', '23003196400'], 'REFS': {'85140452566': [None, '', None, None, None, None], '85140454703': [None, 'ARIA', None, 'European scale of industrial accidents - Reference for experience feedback of technical accidents', None, None], '84946592829': ['7006694977', 'Babrauskas, Vytenis', None, 'Explosions of ammonium nitrate fertilizer in storage or transportation are preventable accidents', 'Journal of Hazardous Materials', '10.1016/j.jhazmat.2015.10.040'], '85029006306': ['7006694977; 7006694977', 'Babrauskas, Vytenis; Babrauskas, Vytenis', None, 'The West, Texas, ammonium nitrate explosion: A failure of regulation', 'Journal of Fire Sciences', '10.1177/0734904116685723'], '85091687537': [None, 'Babrauskas', None, 'The emergency response guidebook (ERG): not good enough, not safe enough', 'Fire Eng.', None], '85077371020': ['7006694977; 7006694977; 57213877899', 'Babrauskas, Vytenis; Babrauskas, Vytenis; Leggett, David', None, 'Thermal decomposition of ammonium nitrate', 'Fire and Materials', '10.1002/fam.2797'], '85115367870': [None, 'Baraer', None, 'The impact of climate events on French industrial facilities between 2010 and 2019', 'Loss Prev. Bull.', None], '85132371039': ['36652291200; 7102822591; 6602124378; 57754132800', 'Baraza, Xavier; Giménez, Jaime; Pey, Alexis; Rubiales, Miriam', None, 'Lessons learned from the Barracas accident: Ammonium nitrate explosion during road transport', 'Process Safety Progress', '10.1002/prs.12396'], '84973576945': [None, 'Bartzokas', None, 'Technological Change and Corporate Strategies in the Fertilizer Industry', None, None], '71049128094': ['57216034585; 57165511400', 'Baum; Clement', None, 'The changing structure of the fertilizer industry in the united states', 'American Journal of Agricultural Economics', '10.2307/1234991'], '85103789237': ['6701527775; 6603551183; 7203036818', 'Ale, Ben J.M.; Hartford, Des N.D.; Slater, David H.', None, 'Prevention, precaution and resilience: Are they worth the cost?', 'Safety Science', '10.1016/j.ssci.2021.105271'], '0001464557': ['7005324157; 7004427947; 15121785200', 'Brower; Oxley, Jimmie C.; Tewari, Mohan', None, 'Evidence for homolytic decomposition of ammonium nitrate at high temperature', 'Journal of Physical Chemistry®', '10.1021/j100347a033'], '85140469246': [None, 'CAS', None, 'Ammonium Nitrate Explosions: Lessons Learned', None, None], '84863904482': ['36998451500; 36952845600', 'Chaturvedi, Shalini; Dave, Pragnesh N.', None, 'Review on Thermal Decomposition of Ammonium Nitrate', 'Journal of Energetic Materials', '10.1080/07370652.2011.573523'], '85072563045': ['57211074524; 13408025900; 35489746600', 'Chen, Qiaoling; Wood, Maureen; Zhao, Jinsong', None, 'Case study of the Tianjin accident: Application of barrier and systems analysis to understand challenges to industry loss prevention in emerging economies', 'Process Safety and Environmental Protection', '10.1016/j.psep.2019.08.028'], '85113337677': ['57215024539; 57209771605; 57227968600; 57227782800', 'Cimer, Zsolt; Vass, Gyula; Kátai-Urbán, Lajos; Zsitnyányi, Attila', None, 'Application of chemical monitoring and public alarm systems to reduce public vulnerability to major accidents involving dangerous substances', 'Symmetry', '10.3390/sym13081528'], '85140486148': [None, 'Conradt', None, None, None, None], '85140443074': [None, 'CSB', None, 'FINAL REPORT: West Fertilizer Final Investigation Report', None, None], '85140470182': [None, 'Data Bridge Market Research', None, 'Global Ammonium Nitrate Market – Industry Trends and Forecast to 2027', None, None], '85140487484': [None, '', None, None, None, None], '85087908529': ['56308398600; 55431371400; 7402008246', 'Ding, Long; Ji, Jie; Khan, Faisal', None, 'A novel approach for domino effects modeling and risk analysis based on synergistic effect and accident evidence', 'Reliability Engineering and System Safety', '10.1016/j.ress.2020.107109'], '85140491015': [None, 'Dolah; Moson; Perzak', None, 'Explosion Hazards of Ammonium Nitrate Under Fire Exposure. Washington, DC: U.S. Department of the Interior', 'Bureau of Mines.', None], '85007613543': ['57192712211; 7402008246; 57192720167; 25959875100', 'El-Gheriani, Malak; Khan, Faisal; Chen, Dan; Abbassi, Rouzbeh', None, 'Major accident modelling using spare data', 'Process Safety and Environmental Protection', '10.1016/j.psep.2016.12.004'], '85064080082': ['6701768312; 57208450315; 6504258439; 34572074500; 6504391553; 7006090884; 57208450315; 7801567129; 6504258439; 6504258439; 39462122000; 39462122000; 7006090884', 'Elmqvist, Thomas; Andersson, Erik; McPhearson, Timon; Olsson, Per; Gaffney, Owen; Folke, Carl; Andersson, Erik; Frantzeskaki, Niki; McPhearson, Timon; McPhearson, Timon; Takeuchi, Kazuhiko; Takeuchi, Kazuhiko; Folke, Carl', None, 'Sustainability and resilience for transformation in the urban century', 'Nature Sustainability', '10.1038/s41893-019-0250-1'], '84886905649': [None, 'Elvers; Hawkins; Russey', None, None, "Ullmann's Encyclopedia of Industrial Chemistry", None], '84946550465': [None, 'EPA', None, 'Explosion Hazard from Ammonium Nitrate, EPA 550-F-97-002d', None, None], '85140449165': [None, 'ERA Environmental Management Solutions', None, 'OSHA HCS 2015: The Consequences of Noncompliance', None, None], '85140442333': [None, '', None, None, None, None], '85140437197': [None, 'Essig', None, None, None, None], '85140454438': [None, '', None, None, None, None], '85140453314': [None, '', None, None, None, None], '85058577081': ['55659850100; 24333140600', 'Fang, Yi-Ping; Sansavini, Giovanni', None, 'Optimum post-disruption restoration under uncertainty for enhancing critical infrastructure resilience', 'Reliability Engineering and System Safety', '10.1016/j.ress.2018.12.002'], '85140460932': [None, 'Fernandes; Kulaif', None, None, None, None], '85105321874': ['35748502300; 57194784479; 56785064300; 57223218845', 'Filho, Anastacio Pinto Goncalves; Ferreira, Adonias Magdiel Silva; Ramos, Magna Fernandes; Pinto, Anderson Rogério Albuquerque Pontes', None, 'Are we learning from disasters? Examining investigation reports from National government bodies', 'Safety Science', '10.1016/j.ssci.2021.105327'], '85140467119': [None, '', None, None, None, None], '85111463872': ['57226399403', 'Fisher, Len', None, 'To build resilience, study complex systems', 'Nature', '10.1038/d41586-021-01925-9'], '85140480554': [None, 'Future Market Insights Inc', None, 'Ammonium Nitrate Market 2018–2028: Mining Industry to Stimulate Revenue Growth', None, None], '85092599046': ['57226263190', 'Guiochon, Georges', None, 'On the catastrophic explosion of the AZF plant in Toulouse', 'Process Safety Progress', '10.1002/prs.12197'], '85047688195': ['16056319800', 'Hainer', None, 'The application of kinetics to the hazardous behavior of ammonium nitrate', 'Symposium (International) on Combustion', '10.1016/S0082-0784(55)80032-X']}, 'TITLE': ['Yue, Yue;Gai, Wenmei;Boustras,', '2023', 'Exploration of the causes of ammonium nitrate explosions: Statistics and analysis of accidents over the past 100 years', 'Safety Science', '10.1016/j.ssci.2022.105954'], 'DOI': '10.1016/j.ssci.2022.105954', 'ABSTRACT': None, 'KEYWORDS': ['ammonium nitrate', 'emergency response', 'explosions', 'information deviation', 'regulation'], 'CITS': {}}

# loop through found papers to get the references and citing papers, we will use dicts and not Pandas etc. to minimize the final .exe file
print("Getting references and citing papers")
print("loading information for paper: ", end=" ")
print("")

skipped = 0

for paper in tqdm(s.results):

    if min_cit.isnumeric() == False or int(min_cit) <= paper.citedby_count:
        paper_dict = {}  # create a temporary dictionary for each paper where informations are stored
        try:
            paper_dict["AUTHOR-IDS"] = paper.author_ids.split(sep=";")  # if there are author IDs for a paper x in S
        except:
            paper_dict["AUTHOR-IDS"] = ""
        try:
            ab = AbstractRetrieval(paper.eid, id_type="eid", view="REF",
                                   refresh=refresh, startref="0")  # use different package to get references of paper.
        except:
            ab = None

        if abstracts != "n":
            try:
                abstract_info = AbstractRetrieval(paper.eid, id_type="eid", view="FULL",
                                   refresh=refresh)
                paper_dict["ABSTRACT"] = abstract_info.abstract
            except:
                paper_dict["ABSTRACT"] = ""
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
                if reference.id is not None:
                    ref_dict[reference.id] = [reference.authors_auid, ((reference.authors)), str(reference.coverDate)[:4],
                                                  (reference.title), (reference.sourcetitle), (reference.doi)]  # title
            while TotalRefCount > CheckedRefsCount:

                ab = AbstractRetrieval(paper.eid, id_type="eid", view="REF",
                                       refresh=refresh, startref=str(CheckedRefsCount + 1), refcount=0)
                CheckedRefsCount += len(ab.references)
                for reference in ab.references:  ## fill the ref_dict with a list of references, each element is again a list of the main information, e.g. authors, years, title etc
                    if reference.id is not None:
                        ref_dict[reference.id] = [reference.authors_auid, ((reference.authors)), str(reference.coverDate)[:4],
                                                      (reference.title), (reference.sourcetitle), (reference.doi)]  # title
            paper_dict["REFS"] = ref_dict
        else:
            paper_dict["REFS"] = {}
        try:
            paper_dict["authorNames"] = (paper.author_names.split(sep=";"))
        except:
            paper_dict["authorNames"] = ["NA"]

        paper_dict["TITLE"] = [str(paper.author_names)[:100], str((paper.coverDate))[:4], (paper.title),
                               (paper.publicationName), paper.doi]
        paper_dict["DOI"] = paper.doi
        paper_dict["year"] = str((paper.coverDate))[:4]
        paper_dict["cite_count"] = paper.citedby_count
        temp_keyword = str(paper.authkeywords).lower().split(" | ")
        paper_dict["KEYWORDS"] = temp_keyword if temp_keyword[0] != "none" else []

        ## getting  citing papers
        if mode_cit != "n":  # if user has decided to get information on the citing papers
            ##getting citing paper
            s = ScopusSearch(f"REF({str(paper.eid)})", refresh=refresh)  # use main package via a searchstring
            try:
                citing = s.results[:200000]
            except:
                citing = None
            cit_dict = {}
            if citing != None:
                for citing_paper in citing:

                    try:
                        cit_dict[str(citing_paper.eid).replace("2-s2.0-", "")] = [citing_paper.author_ids.split(sep=";"),
                                                                                  (citing_paper.author_names),
                                                                                  str(citing_paper.coverDate)[:4],
                                                                                  (citing_paper.title),
                                                                                  (citing_paper.publicationName),
                                                                                  citing_paper.doi]
                    except:
                        cit_dict[str(citing_paper.eid).replace("2-s2.0-", "")] = ["", (citing_paper.author_names),
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
    else:
        skipped += 1



print("done. skipped " + str(skipped) + " papers")

total_cits = (([item for sublist in ([[x for x in (paper["CITS"])] for paper in master_dict.values()]) for item in sublist]))
total_refs = (([item for sublist in ([[x for x in (paper["REFS"])] for paper in master_dict.values()]) for item in sublist]))





print("downloaded " + str(len(total_refs)) + " references and " + str(len(total_cits)) + " citing papers")

##############################################################
################## generate NetworkX network #################
##############################################################

#here you can filter to include only most frequent references and citing papers
extra_nodes_no = 0
if extra_nodes == "a":
    extra_nodes_no = input("Minimum occurrence for extra nodes for references and citing papers? \"\n" + ": ")




total_refs = [item[0] for item in Counter(total_refs).most_common() if
              item[1] > int(extra_nodes_no) and item[0] not in master_dict.keys()]
total_cits = [item[0] for item in Counter(total_cits).most_common() if
              item[1] > int(extra_nodes_no) and item[0] not in master_dict.keys()]

print("make network")
print(print("will use " + str(len(total_refs)) + " references and " + str(len(total_cits)) + " citing papers"))

G = nx.DiGraph()  # create an empty networkX graph

Author_paper_dict = {} # helper dict store author -> paper combinations which allows for a quick computation of authorship networks

print("create nodes")
for node in (master_dict.keys()):
    # creating main nodes

    for id in master_dict[node]["AUTHOR-IDS"]:
        if id in Author_paper_dict:
            Author_paper_dict[id].append(node)
        else:
            Author_paper_dict[id] = [node]


    G.add_node(node,
               type="main",
               myauth=master_dict[node]["AUTHOR-IDS"],
               year=master_dict[node]["year"],
               title=master_dict[node]["TITLE"],
               myrefs=master_dict[node]["REFS"].keys(),
               mycits=master_dict[node]["CITS"].keys(),
               myabstract=master_dict[node]["ABSTRACT"],

               color="#6495ED",
               keywords=master_dict[node]["KEYWORDS"],
               url=master_dict[node]["TITLE"][4],
               cite_count=master_dict[node]["cite_count"],
               authorNames= master_dict[node]["authorNames"]
               )
    if extra_nodes != "n":  # if the user wants to, create nodes for the references and citing papers
        for temp_ref_id in master_dict[node]["REFS"].keys():
            if temp_ref_id in total_refs and temp_ref_id not in master_dict.keys():




                try:
                    temp_auth = (master_dict[node]["REFS"][temp_ref_id][0].split(sep="; "))
                except:
                    temp_auth = ""
                #print((master_dict[node]["REFS"][temp_ref_id][1]))

                for id in temp_auth:

                    if id in Author_paper_dict:
                        Author_paper_dict[id].append(temp_ref_id)
                    else:
                        Author_paper_dict[id] = [temp_ref_id]
                G.add_node(temp_ref_id,
                           type="REF",
                           myauth=temp_auth,
                           title=(master_dict[node]["REFS"][temp_ref_id][1:]),
                           year=(master_dict[node]["REFS"][temp_ref_id][2]),

                           color="#DE3163",
                           url=(master_dict[node]["REFS"][temp_ref_id][5]),
                           keywords = [],
                           myabstract="",
                           authorNames=str(master_dict[node]["REFS"][temp_ref_id][1]).split(sep=";")
                           )
                total_refs.remove(temp_ref_id)
        for temp_cit_id in master_dict[node]["CITS"].keys():
            if temp_cit_id in total_cits and temp_cit_id not in master_dict.keys():

                for id in (master_dict[node]["CITS"][temp_cit_id][0]):

                    if id in Author_paper_dict:
                        Author_paper_dict[id].append(temp_cit_id)
                    else:
                        Author_paper_dict[id] = [temp_cit_id]

                G.add_node(temp_cit_id,
                           type="CIT",
                           myauth=(master_dict[node]["CITS"][temp_cit_id][0]),
                           title=(master_dict[node]["CITS"][temp_cit_id][1:]),
                           year=str(master_dict[node]["CITS"][temp_cit_id][2])[:4],

                           color="#1a762c",
                           url=(master_dict[node]["CITS"][temp_cit_id][5]),
                           keywords=[],
                           myabstract="",
                           authorNames=str(master_dict[node]["CITS"][temp_cit_id][1]).split(sep=";"),
                           )
                total_cits.remove(temp_cit_id)


print("create links")



def compute_links():

    list_of_nodes = G.nodes(data=False)


    # citations
    for node, info in  G.nodes(data=True):
        if info["type"] == "main":
            for other_node in [other_node for other_node in info["myrefs"] if other_node in list_of_nodes]:
                G.add_edge(node, other_node, cited="true")
            for other_node in [other_node for other_node in info["mycits"] if other_node in list_of_nodes]:
                G.add_edge(other_node, node, cited="true")


    # shared authorship
    # for node1, node2, in (combinations([(node[0], node[1]) for node in G.nodes(data="myauth")], 2)):
    #
    #     if [x for x in node1[1] if x in node2[1]] != []:
    #         G.add_edge(node1[0], node2[0], coauth="true")  # create edge

    for author in Author_paper_dict:
        if len(Author_paper_dict[author]) > 1:
            for myPaper1, myPaper2 in combinations(Author_paper_dict[author], 2):
                G.add_edge(myPaper1, myPaper2, coauth="true")




    #bibliographic coupling, co-citation, shared keywords, only possible for main nodes
    for node1, node2, in (combinations([node for node in G.nodes(data=True) if node[1]["type"] == "main"], 2)):
                        ## same reference
            temp = len([x for x in (node1[1]["myrefs"]) if x in (node2[1]["myrefs"])])
            if temp > min_weight_biblio:
                G.add_edge(node2[0], node1[0], BiblioCoup="true", Biblio_strength=temp)
            # Co-citation
            temp = len([x for x in (node1[1]["mycits"]) if x in (node2[1]["mycits"])])
            if temp > min_weight_cocit:
                G.add_edge(node2[0], node1[0], CoCit="true",
                           cocit_strength=temp)
            # Keywords
            temp = len([x for x in node1[1]["keywords"] if x in node2[1]["keywords"]])
            if temp > min_weight_key:
                G.add_edge(node2[0], node1[0], KeyWord="true",
                           keyword_strength=temp)




import time


compute_links()



print(G)

#gephi
if answer == "a" and input("Create Gephi file?: \n" + "y/n: ") == "y":
    G2 = G
    for node, info in G2.nodes(data=True):
        del G2.nodes[node]["myauth"]
        if G2.nodes[node].get("type") == "main":
            del G2.nodes[node]["myrefs"]
            del G2.nodes[node]["mycits"]
        G2.nodes[node]["label"] = " ".join([str(x)[:20] for x in G.nodes[node].get("title")[:2] if (x) != None])
        G2.nodes[node]["title"] = str(G2.nodes[node].get("title"))
    for node in G2.nodes:
        for attrib in G2.nodes[node]:
            if (G2.nodes[node][attrib]) == None:
                (G2.nodes[node][attrib]) = "None"
            if type(G2.nodes[node][attrib]) == list:
                (G2.nodes[node][attrib]) = "None"

    filename_gephi = input("Filename? \n"   )
    print(filename_gephi)
    nx.write_gexf(G2, filename_gephi)
#

###### overwrite the list of nodes and edges in our template html by transforming our information from the NetworkX network to lists

list_node_dict = []  # temporary variables used to store information
list_edge_dict = []  # temporary variables used to store information



for node, info in G.nodes(data=True):
    node_dict = {}
    node_dict["color"] = info["color"]
    node_dict["myauth"] = info["myauth"]
    #node_dict["authorNames"] = info["authorNames"]
    #node_dict["myauthName"] = info["myauth"]
    if info["type"] == "main":
        node_dict["shape"] = "dot"
        node_dict["cite_count"] = info["cite_count"]
    if G.nodes[node].get("year") != None:
        node_dict["level"] = info["year"]
    else:
        node_dict["level"] = "0000"

    node_dict["id"] = node
    node_dict["keywords"] = info["keywords"]
    node_dict["size"] = 10
    if info["type"] == "REF":
        #node_dict["size"] = 5 + G.degree[node]
        node_dict["shape"] = "triangle"
        node_dict["cite_count"] = 0
    if info["type"] == "CIT":
        node_dict["shape"] = "star"
        node_dict["cite_count"] = 0
        #node_dict["size"] = 5 + G.degree[node]
    node_dict["journal"] = str(info["title"][3])
    node_dict["title"] = textwrap.fill(str(info["title"][0]) + " (" + str(info["title"][1])  + "). " + str(info["title"][2]) + ". " + str(info["title"][3]) + ". Keywords: " + ", ".join(info["keywords"]), 100) + "\n" + "\n"
    #[i:i + 100] for i in range(0, len(str(info["keywords"]))
    node_dict["title"] += textwrap.fill("Abstract: " + str(info["myabstract"]) + " DOI: " + str(info["url"]), 100)
                                        # node_dict["title"] = " \n ".join([str(x)[:200] for x in info["title"] if (x) != None]) + \
    #                      "\n Keywords: " + '\n'.join(
    #     str(info["keywords"])[i:i + 100] for i in range(0, len(str(info["keywords"])), 100)) + \
    #                      "\n Abstract: " + '\n'.join(str(info["myabstract"])[i:i + 100] for i in
    #                                                        range(0, len(str(info["myabstract"])), 100)) + "\n DOI: " + str(info["url"])
    #node_dict["label"] = " ".join([str(x)[:20] for x in G.nodes[node].get("title")[:2] if (x) != None])
    node_dict["type"] = info["type"]
    node_dict["value"] = 1
    #print(str(info["authorNames"]))
    tempauthors = ([(x.split(sep=",")[0]) for x in info["authorNames"]])#[x.split(",") for x in info["authorNames"]])#" ".join([str(x)[:20] for x in info["title"][:2] if (x) != None])
    if len(tempauthors) < 3:
            node_dict["label"] = ", ".join(tempauthors) + " (" + info["title"][1] + ") "
    else:
        node_dict["label"] = (tempauthors[0]) + " et al. (" + info["title"][1] + ") "
    #print(node_dict["label"])
    if str((info["url"])) != "None":
        node_dict["url"] =  "https://doi.org/" + str(G.nodes[node].get("url"))
    else:
        node_dict["url"] = "https://scholar.google.de/scholar?q=" + str(info["title"]) + "\""
    #node_dict["degree"] = G.degree[node]
    list_node_dict.append(node_dict)


list_edge_dict = []
for edge, edge2, info in G.edges(data=True):
    edge_dict = {}
    edge_dict["from"] = edge
    edge_dict["to"] = edge2
    for key in info.keys():
        edge_dict[key] = info[key]
    list_edge_dict.append(edge_dict)

node_list = "nodes = new vis.DataSet(" + str(list_node_dict) + ")"
edge_list = "edges = new vis.DataSet(" + str(list_edge_dict) + ")"

file = open("PyblioNet_templateV0.9.html", "r", encoding="utf-8")
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

if input("done, open html file now?  \n" + "(y)es/(n)o:") != "n":
    webbrowser.open(searchstring.replace(" ", "").replace("\"", "").replace("*", "")[:60] + "_final.html")
#
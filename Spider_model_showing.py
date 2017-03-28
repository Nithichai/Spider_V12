import networkx  # Library use save website in graph
from nodebox.graphics.physics import Graph  # Library use to draw graph
import json  # Library used to change json string to dict
from urlparse import urlparse  # Set website format


class SpiderModelShowing:
    def __init__(self):
        print "start : init : SpiderModelShowing"
        self.json_dict = {}                     # data from json
        self.all_graph = networkx.DiGraph()     # graph that save all website
        self.show_graph = Graph()               # graph to draw
        self.dict_netloc_used = {}              # dict to save number of netloc is used
        self.dict_website_found = {}            # dict to save number of word is found (website)
        self.dict_netloc_found = {}             # dict to save number of word is found (netloc)
        self.list_rank = []                     # list that save netloc, number of used, word found and rank it
        print "complete : init : SpiderModelShowing"

    def change_json_to_dict(self, json_str):
        print "complete : change_json_to_dict : SpiderModelShowing"
        self.json_dict = json.loads(json_str)  # change json string to dict

    def reset_data(self):
        print "start : reset_data : SpiderModelShowing"
        self.all_graph = networkx.DiGraph()  # graph that save all website
        self.show_graph = Graph()  # graph to draw
        self.dict_netloc_used = {}  # dict to save number of netloc is used
        self.dict_website_found = {}  # dict to save number of word is found (website)
        self.dict_netloc_found = {}  # dict to save number of word is found (netloc)
        self.list_rank = []  # list that save netloc, number of used, word found and rank it
        print "complete : reset_data : SpiderModelShowing"

    # method is used to set some value into graph
    def set_into_graph(self, root_website):
        print "start : set_into_graph : SpiderModelShowing"
        for netloc_uni in self.json_dict[root_website]:     # use netloc in json_dict
            netloc = netloc_uni.encode('utf-8')             # change unicode to string
            for website_uni in self.json_dict[root_website][netloc]:  # use website in json_dict
                website = website_uni.encode('utf-8')       # change unicode to string
                self.all_graph.add_node(website)  # add website into graph)
                if self.get_netloc(website) != "":  # netloc has word
                    self.show_graph.add_node(self.get_netloc(website))  # add netloc in draw graph
                # use child website
                for child_website_uni in self.json_dict[root_website][netloc][website]["website"]:
                    child_website = child_website_uni.encode('utf-8')
                    self.all_graph.add_node(child_website)  # add child website into graph
                    self.all_graph.add_edge(child_website, website)  # add edge website to child-website
                    # add netloc of child website into draw graph
                    if self.get_netloc(child_website) != "":  # netloc has word
                        self.show_graph.add_node(self.get_netloc(child_website))
                    # detect netloc of website and child-website is not same
                    if self.get_netloc(website) != self.get_netloc(child_website):
                        # all netloc has word
                        if self.get_netloc(website) != "" and self.get_netloc(child_website) != "":
                            # add edge website to child-website to draw graph
                            self.show_graph.add_edge(self.get_netloc(website),
                                                     self.get_netloc(child_website))
        print "complete : set_into_graph : SpiderModelShowing"

    # method is used to set number of this website is used
    def set_n_used(self, root_website):
        print "start : set_n_used : SpiderModelShowing"
        for netloc in self.json_dict[root_website]:         # use netloc in json_dict
            netloc = netloc.encode('utf-8')                 # change unicode to string
            if netloc not in self.dict_netloc_used:         # netloc not in dict used
                self.dict_netloc_used[netloc] = 0           # set netloc in dict and set 0
            for website in self.json_dict[root_website][netloc]:  # get website in dict
                website = website.encode('utf-8')                 # change unicode to string
                # get child website in list
                for child_website in self.json_dict[root_website][netloc][website]["website"]:
                    child_website = child_website.encode('utf-8')
                    # child's netloc not in dict used
                    if self.get_netloc(child_website) not in self.dict_netloc_used:
                        self.dict_netloc_used[self.get_netloc(child_website)] = 0   # set netloc in dict and set 0
                    # child's netloc and website's netloc is not same
                    if self.get_netloc(child_website) != netloc:
                        self.dict_netloc_used[self.get_netloc(child_website)] += 1  # add value in used dict
        print "complete : set_n_used : SpiderModelShowing"

    # method is used to set number of word that find in content (netloc)
    def set_n_word_netloc(self, root_website, word):
        print "start : set_n_word_netloc : SpiderModelShowing"
        for netloc in self.json_dict[root_website]:     # use netloc in json_dict
            netloc = netloc.encode('utf-8')             # change unicode to string
            if netloc not in self.dict_netloc_found:    # netloc not in dict n_word
                self.dict_netloc_found[netloc] = 0      # set netloc in dict and set 0
            for website in self.json_dict[root_website][netloc]:  # get website in dict
                website = website.encode('utf-8')  # change unicode to string
                # get content in json dict
                content = self.json_dict[root_website][netloc][website]["content"].encode('utf-8')
                self.dict_netloc_found[netloc] += content.lower().count(word.lower())  # count word in that content
                for child_website in self.json_dict[root_website][netloc][website]["website"]:
                    child_website = child_website.encode('utf-8')
                    # child's netloc not in dict used
                    if self.get_netloc(child_website) not in self.dict_netloc_found:
                        self.dict_netloc_found[self.get_netloc(child_website)] = 0  # set netloc in dict and set 0
        print "complete : set_n_word_netloc : SpiderModelShowing"

    # method is used to set number of word that find in content (website)
    def set_n_word_website(self, root_website, word):
        print "start : set_n_word_website : SpiderModelShowing"
        for netloc in self.json_dict[root_website]:  # use netloc in json_dict
            netloc = str(netloc)  # change unicode to string]
            for website in self.json_dict[root_website][netloc]:  # get website in dict
                website = str(website)  # change unicode to string
                if website not in self.dict_website_found:  # website not in dict
                    self.dict_website_found[website] = 0    # get website in dict and set 0
                content = self.json_dict[root_website][netloc][website]["content"]  # get content in json dict
                self.dict_website_found[website] += content.lower().count(word.lower())  # count word in that content
        print "complete : set_n_word_website : SpiderModelShowing"

    # method that get netloc from website (website)
    @staticmethod
    def get_netloc(website):
        # print "complete : get_netloc : SpiderModelShowing"
        return urlparse(website).netloc  # return netloc

    # method that return dict of number of used (netloc)
    def get_dict_netloc_used(self):
        # print "complete : get_dict_netloc_used : SpiderModelShowing"
        return self.dict_netloc_used

    # method that return dict of number of found (netloc)
    def get_dict_netloc_found(self):
        # print "complete : get_dict_netloc_found : SpiderModelShowing"
        return self.dict_netloc_found

    # method that return dict of number of found (network)
    def get_dict_website_found(self):
        # print "complete : get_dict_website_found : SpiderModelShowing"
        return self.dict_website_found

    # method that return show graph value
    def get_show_graph(self):
        # print "complete : get_show_graph : SpiderModelShowing"
        return self.show_graph

    # method that return all graph
    def get_all_graph(self):
        # print "complete : get_all_graph : SpiderModelShowing"
        return self.all_graph

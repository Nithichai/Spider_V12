from Spider_model_saving import SpiderModelSaving       # use Spider_model_saving
from Spider_model_showing import SpiderModelShowing     # use Spider_model_showing
from Spider_model_indexing import SpiderModelIndexing
from Spider_model_ranking import SpiderModelRanking


class SpiderModel:
    def __init__(self):
        print "start : init : SpiderModel"
        self.saving = SpiderModelSaving()           # use saving model
        self.showing = SpiderModelShowing()         # use showing model
        self.indexing = SpiderModelIndexing()       # use indexing model
        self.ranking = SpiderModelRanking()

        self.root_website = ""                      # root website
        self.index_website = ""                     # index website
        self.word = ""                              # word that found

        self.content_dict = {}                      # dict of content
        self.website_dict = {}                      # dict of website
        print "complete : init : SpiderModel"

    def reset_data(self):
        print "start : reset_data : SpiderModel"
        self.content_dict = {}  # dict of content
        self.website_dict = {}  # dict of website.
        print "complete : reset_data : SpiderModel"

    def save_data_from_html(self):
        print "start : save_data_from_html : SpiderModel"
        html_code = self.saving.get_html_code(self.index_website)  # get html code
        data_str = self.saving.get_htmlcode_to_datastr(html_code)  # get data string
        # save content into dict (all content)
        self.content_dict[self.index_website] = self.saving.get_content_from_datastr(data_str) + \
                                                self.saving.get_weblink_from_datastr(data_str)
        # save website into dict
        self.website_dict[self.index_website] = self.saving.get_website_from_datastr(self.root_website, data_str)
        print "complete : save_data_from_html : SpiderModel"

    def save_data_to_json(self):
        print "start : save_data_to_json : SpiderModel"
        # set dict of json
        json_string = self.saving.get_json_string(self.root_website, self.website_dict, self.content_dict)
        # set file name
        json_file_name = self.saving.get_netloc(self.root_website).replace(".", "_") + ".json"
        json_file = open(json_file_name, "w+")  # start to write file
        json_file.write(json_string)  # write json in file
        json_file.close()  # stop to use file
        print "complete : save_data_to_json : SpiderModel"

    def set_data_to_show(self):
        print "start : set_data_to_show : SpiderModel"
        # get file name
        json_file_name = self.saving.get_netloc(self.root_website).replace(".", "_") + ".json"
        json_file = open(json_file_name, "r+")  # open to read file
        self.showing.change_json_to_dict(json_file.read())  # set json string to dict
        self.showing.reset_data()                           # Reset data
        self.showing.set_into_graph(self.root_website)  # set data to graph
        self.showing.set_n_used(self.root_website)  # set number of used in dict
        self.showing.set_n_word_netloc(self.root_website, self.word)  # set number of word in dict (netloc)
        self.showing.set_n_word_website(self.root_website, self.word)  # set number of word in dict (website)
        json_file.close()
        print "complete : set_data_to_show : SpiderModel"

    def make_indexing(self):
        print "start : make_indexing : SpiderModel"
        self.indexing.set_avoid_word()
        self.indexing.set_n_used()
        self.indexing.indexing()
        self.indexing.save_to_json_file()
        print "complete : make_indexing : SpiderModel"

    def get_ranking_dict(self):
        print "start : get_ranking_dict : SpiderModel"
        self.ranking.ranking()
        print "complete : get_ranking_dict : SpiderModel"
        return self.ranking.get_ranking_dict()

    # method send data for graph
    def graph_data_pack(self):
        # print "complete : graph_data_pack : SpiderModel"
        return self.showing.get_dict_netloc_used(), self.showing.get_dict_netloc_found()

    # method send data for field
    def field_data_pack(self):
        # print "complete : field_data_pack : SpiderModel"
        return self.showing.get_dict_website_found()  # return word found dict (website)

    # method return root website
    def get_root_website(self):
        # print "complete : get_root_website : SpiderModel"
        return self.root_website

    # method return index website
    def get_index_website(self):
        # print "complete : get_index_website : SpiderModel"
        return self.index_website

    def get_content_dict(self):
        # print "complete : get_content_dict : SpiderModel"
        return self.content_dict

    def get_website_dict(self):
        # print "complete : get_website_dict : SpiderModel"
        return self.website_dict

    # method set root website
    def set_root_website(self, root_website):
        # print "complete : set_root_website : SpiderModel"
        self.root_website = root_website

    # method set index website
    def set_index_website(self, index_website):
        # print "complete : set_index_website : SpiderModel"
        self.index_website = index_website

    # method set word
    def set_word(self, word):
        # print "complete : set_word : SpiderModel"
        self.word = word

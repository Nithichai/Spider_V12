from Spider_Model import SpiderModel
from Spider_View import SpiderView
import thread
import json
import os


class SpiderControl:
    def __init__(self):
        print "start : init : SpiderControl"
        self.spider_model = SpiderModel()                   # set model
        self.spider_view = SpiderView(self.spider_model)    # set view
        self.list_website = []                              # save child-website list
        self.update_spider_state = False                    # state search spider
        self.deep = 0                                       # deep of spider reaching
        self.total_deep = 0
        self.pause = True
        self.has_deep_thread = False
        self.count_deep_thread = 0
        if "deep_save.json" not in os.listdir(os.getcwd()):
            file_saving = open("deep_save.json", "w+")
            file_saving.write(json.dumps({}))
            file_saving.close()
        print "complete : init : SpiderControl"

    # method that thread of searching website
    def start_search_website_thread(self):
        print "start : start_search_website_thread : SpiderControl"
        if not self.has_deep_thread:
            thread.start_new_thread(self.start_deep_website, ())
        print "complete : start_search_website_thread : SpiderControl"

    # method that searching website
    def start_deep_website(self):
        print "start : start_search_website : SpiderControl"
        self.spider_view.set_update_state(False)                                    # set update text = updating
        self.spider_model.set_root_website(self.spider_view.get_root_website())     # set root website
        self.spider_model.set_index_website(self.spider_view.get_root_website())    # set index website
        self.spider_model.set_word(self.spider_view.get_word())                     # set word
        self.total_deep = self.spider_view.get_deep()
        self.pause = False
        file_deep = open("deep_save.json", "r+")
        json_deep = json.loads(file_deep.read())
        file_deep.close()
        root_website = self.spider_model.get_root_website()
        if root_website in json_deep:
            n_deep_save = int(json_deep[root_website].items()[0][0])
            if n_deep_save < self.total_deep:
                self.list_website = json_deep[root_website][unicode(n_deep_save)]
                self.deep = self.total_deep - n_deep_save
                self.spider_model.set_index_website(self.list_website[0][0].encode("utf-8"))
            else:
                self.deep = self.total_deep
                self.list_website = []
                self.list_website.append([root_website])  # set root website in child website
        else:
            self.deep = self.total_deep
            self.list_website = []
            self.list_website.append([root_website])    # set root website in child website

        self.spider_model.reset_data()
        self.deep_into_website(self.deep)
        self.spider_view.set_update_state(True)
        self.pause = True
        print "complete : start_search_website : SpiderControl"

    def deep_into_website(self, n_deep):
        print "start : deep_into_website : SpiderControl"
        list_web_in_hop = []    # set child website in that deep
        if n_deep == 0:         # deep of reaching is end
            self.deep_save()
            return              # exit
        for web in self.list_website[0]:    # get website in first of child website list
            if self.pause:
                if len(self.list_website) > 1:
                    self.list_website[1] = list(set(self.list_website[1]) | set(list_web_in_hop))
                elif len(self.list_website) == 1:
                    self.list_website.append(list_web_in_hop)
                self.total_deep = self.total_deep - n_deep
                self.deep_save()
                return
            web = web.encode("utf-8")
            # set index website
            index_website = self.spider_model.saving.website_formatter(self.spider_model.get_index_website(), web)
            self.spider_model.set_index_website(index_website)
            if self.spider_model.get_index_website() == "":     # website no word
                continue                                        # next loop
            self.spider_model.save_data_from_html()             # get data from html
            # get child website in that website
            for web_inside in self.spider_model.get_website_dict()[self.spider_model.get_index_website()]:
                if web_inside == "":                            # website no word
                    continue                                    # next loop
                list_web_in_hop.append(web_inside)              # save child website in list
            self.spider_model.save_data_to_json()               # save data to json file
            self.list_website[0].pop(0)
        self.list_website.append(list_web_in_hop)               # save child website in that deep in list of all child
        self.list_website.pop(0)                                # delete deep that is reached
        swap_deep = self.total_deep
        self.total_deep = self.total_deep - n_deep + 1
        self.deep_save()
        self.total_deep = swap_deep
        self.deep_into_website(n_deep - 1)                      # go deeper
        print "complete : deep_into_website : SpiderControl : Deep = " + str(n_deep)

    def pause_deep(self):
        self.pause = True

    def deep_save(self):
        file_saving = open("deep_save.json", "r+")
        dict_deep = json.loads(file_saving.read())
        root_website = self.spider_model.get_root_website()
        dict_deep[root_website] = {self.total_deep: self.list_website}
        file_saving.close()
        file_saving = open("deep_save.json", "w+")
        file_saving.write(json.dumps(dict_deep))
        file_saving.close()

    def start_to_show(self):
        print "complete : search_website : SpiderControl"
        self.spider_model.set_root_website(self.spider_view.get_root_website())
        self.spider_model.set_word(self.spider_view.get_word())
        self.spider_model.set_data_to_show()
        print "complete : search_website : SpiderControl"

    def start_to_indexing(self):
        print "start : start_to_indexing : SpiderControl"
        self.spider_model.make_indexing()
        print "complete : start_to_indexing : SpiderControl"

    def start_to_searching(self):
        print "start : start_to_searching : SpiderControl"
        self.spider_view.show_search()
        print "complete : start_to_searching : SpiderControl"

from Spider_Model import SpiderModel        # use save data
from Spider_View import SpiderView          # use GUI and sho graph
import thread                               # use thread of program
import json                                 # use for json
import os                                   # use for specific file


class SpiderControl:
    def __init__(self):
        print "start : init : SpiderControl"
        self.spider_model = SpiderModel()                   # set model
        self.spider_view = SpiderView(self.spider_model)    # set view
        self.list_website = []                              # save child-website list
        self.update_spider_state = False                    # state search spider
        self.deep = 0                                       # range of deep for spider reaching
        self.total_deep = 0                                 # deep of spider reach
        self.pause = True                                   # pause to deep website
        self.has_deep_thread = False                        # use thread of deep website
        if "deep_save.json" not in os.listdir(os.getcwd()):     # not found deep_save.json
            file_saving = open("deep_save.json", "w+")          # open file
            file_saving.write(json.dumps({}))                   # save json
            file_saving.close()                                 # close file
        print "complete : init : SpiderControl"

    # method that thread of searching website
    def start_search_website_thread(self):
        print "start : start_search_website_thread : SpiderControl"
        if not self.has_deep_thread:                                # detect not use thread
            thread.start_new_thread(self.start_deep_website, ())    # start thread
            self.has_deep_thread = True                             # set thread is used
        print "complete : start_search_website_thread : SpiderControl"

    # method that deeping website
    def start_deep_website(self):
        print "start : start_search_website : SpiderControl"
        self.spider_view.set_update_state(False)                                    # set update text = updating
        self.spider_model.set_root_website(self.spider_view.get_root_website())     # set root website
        self.spider_model.set_index_website(self.spider_view.get_root_website())    # set index website
        self.spider_model.set_word(self.spider_view.get_word())                     # set word
        self.total_deep = self.spider_view.get_deep()                               # get total_deep from GUI
        self.pause = False                                                          # not pause
        file_deep = open("deep_save.json", "r+")                                    # open file
        json_deep = json.loads(file_deep.read())                                    # get dict from file
        file_deep.close()                                                           # close file
        root_website = self.spider_model.get_root_website()                         # get root website from dict
        if root_website in json_deep:                                               # detect root website in dict
            n_deep_save = int(json_deep[root_website].items()[0][0])                # get number of deep from save

            # detect deep from save less than deep from GUI
            if n_deep_save < self.total_deep:
                self.list_website = json_deep[root_website][unicode(n_deep_save)]   # get list website from save

                # calculate deep from GUI - from save
                self.deep = self.total_deep - n_deep_save

                # set index website for find
                self.spider_model.set_index_website(self.list_website[0][0].encode("utf-8"))
            else:
                self.deep = self.total_deep                 # set deep is deep from GUI
                self.list_website = []                      # reset list of website
                self.list_website.append([root_website])    # set root website in child website
        else:
            self.deep = self.total_deep                 # set deep is deep from GUI
            self.list_website = []                      # reset list of website
            self.list_website.append([root_website])    # set root website in child website

        self.spider_model.reset_data()                  # reset data
        self.deep_into_website(self.deep)               # deep into website
        self.spider_view.set_update_state(True)         # set update text = updated
        self.pause = True                               # set pause
        print "complete : start_search_website : SpiderControl"

    # method used to deep into website at multi-deep
    def deep_into_website(self, n_deep):
        print "start : deep_into_website : SpiderControl"
        list_web_in_hop = []                    # set child website in that deep
        if n_deep == 0:                         # deep of reaching is end
            self.deep_save()                    # save website is not deep
            self.has_deep_thread = False        # set thread is not used
            return
        for web in self.list_website[0]:        # get website in first of child website list
            if self.pause:                      # detect deeping is pause
                if len(self.list_website) > 1:  # detect website in next deep is reach

                    # merge website from save website and website is found
                    self.list_website[1] = list(set(self.list_website[1]) | set(list_web_in_hop))
                elif len(self.list_website) == 1:               # detect website in next deeo is not reach
                    self.list_website.append(list_web_in_hop)   # add list into list for save
                self.total_deep = self.total_deep - n_deep      # calculate deep from GUI - deep in this
                self.deep_save()                                # save website is not deep
                self.has_deep_thread = False                    # set thread is not used
                return
            web = web.encode("utf-8")                           # set website type to string

            # set index website
            index_website = self.spider_model.saving.website_formatter(self.spider_model.get_index_website(), web)
            self.spider_model.set_index_website(index_website)  # set index website for gather
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
        swap_deep = self.total_deep                             # get real total deep
        self.total_deep = self.total_deep - n_deep + 1          # set deep to save
        self.deep_save()                                        # save website is not deep
        self.total_deep = swap_deep                             # get real total deep
        self.deep_into_website(n_deep - 1)                      # go deeper
        print "complete : deep_into_website : SpiderControl : Deep = " + str(n_deep)

    # set pause of deep
    def pause_deep(self):
        self.pause = True

    # save max deep and list of website that is not reach
    def deep_save(self):
        file_saving = open("deep_save.json", "r+")              # open file to read
        dict_deep = json.loads(file_saving.read())              # load json to dict
        root_website = self.spider_model.get_root_website()     # get root website
        dict_deep[root_website] = {self.total_deep: self.list_website}      # save dict for deep and website list
        file_saving.close()                                     # close file
        file_saving = open("deep_save.json", "w+")              # open file to write
        file_saving.write(json.dumps(dict_deep))                # write json to file
        file_saving.close()                                     # close file

    # set root website, word from GUI and show graph
    def start_to_show(self):
        print "complete : search_website : SpiderControl"
        self.spider_model.set_root_website(self.spider_view.get_root_website())
        self.spider_model.set_word(self.spider_view.get_word())
        self.spider_model.set_data_to_show()
        print "complete : search_website : SpiderControl"

    # start indexing
    def start_to_indexing(self):
        print "start : start_to_indexing : SpiderControl"
        self.spider_model.make_indexing()
        print "complete : start_to_indexing : SpiderControl"

    # start searching
    def start_to_searching(self):
        print "start : start_to_searching : SpiderControl"
        self.spider_view.show_search()
        print "complete : start_to_searching : SpiderControl"

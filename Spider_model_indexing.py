from urlparse import urlparse   # Set website format
import os                       # check list file
import json                     # Read json string to dict
import re                       # Sub or split string


class SpiderModelIndexing:
    def __init__(self):
        print "start : init : SpiderModelIndexing"
        self.avoid_word = {}        # dict that save avoid word
        self.word = {}              # dict that save word from text file
        self.content = {}           # dict that save content from json file
        self.indexing_dict = {}     # dict that make word library
        self.dict_n_ref = {}        # dict that save number of website is reference
        self.dict_n_word = {}       # dict that save number of word in website
        self.avoid_file = ["indexing.json", "deep_save.json"]

    # save avoid word from text file into dict
    def set_avoid_word(self):
        print "start : set_avoid_word : SpiderModelIndexing"
        avoid_word_file = open("avoid_word.txt", "r+")      # open file
        for word in avoid_word_file:                        # get word from avoid word file
            word = word.strip()                             # delete space
            self.avoid_word[word] = {}                      # set word in list
        avoid_word_file.close()                             # close file
        print "complete : set_avoid_word : SpiderModelIndexing"

    def indexing(self):
        print "start : indexing : SpiderModelIndexing"
        if "indexing" not in os.listdir(os.getcwd()):
            self.indexing_dict = {}
        else:
            file_indexing = open("indexing.json", "r+")
            self.indexing_dict = json.loads(file_indexing.read())
        for file_name in os.listdir(os.getcwd()):                # get file in current file
            surname_file = file_name[file_name.find(".") + 1:]                 # get surname of file
            if surname_file == "json" and file_name not in self.avoid_file:         # detect python name
                read_file = open(file_name, "r+")           # read file
                json_dict = json.loads(read_file.read())    # set json dict
                for root_website in json_dict:              # get root website
                    root_website = str(root_website.decode('utf-8'))                # get root website in string
                    for netloc in json_dict[root_website]:                          # netloc list
                        netloc = str(netloc.decode('utf-8'))                        # get netloc string
                        for website in json_dict[root_website][netloc]:             # get website list
                            website = str(website.decode('utf-8'))  # get website string
                            content = json_dict[root_website][netloc][website]["content"]  # get content
                            content = content.encode('utf-8').lower()               # encode and lower
                            list_word = content.split()                             # list of word in content
                            for word in list_word:                                  # loop word in list
                                # detect word
                                word = re.sub(r'[\W\d]', "", word)                  # remove non-word and non-digit
                                if word != "" and word != "\s" and word not in self.avoid_word:
                                    if word.decode("utf-8") not in self.indexing_dict:              # word not in dict
                                        self.indexing_dict[word] = {}               # make it to dict
                                    n_ref = self.dict_n_ref[website]                # get n_ref
                                    # get number of word in website into dict
                                    n_word = content.count(word)
                                    self.dict_n_word[website] = n_word
                                    self.indexing_dict[word][website] = {"used": n_ref, "word": n_word}
                read_file.close()                                                   # close file
        print "complete : indexing : SpiderModelIndexing"

    def set_n_used(self):
        print "start : set_n_used : SpiderModelIndexing"
        self.dict_n_ref = {}                                                # reset dict of n_ref
        for file_name in os.listdir(os.getcwd()):                           # get file in current file
            surname_file = file_name[file_name.find(".") + 1:]              # get surname of file
            if surname_file == "json" and file_name not in self.avoid_file: # detect python name
                read_file = open(file_name, "r+")                           # read file
                json_dict = json.loads(read_file.read())                    # set json dict
                for root_website in json_dict:                              # get root website
                    root_website = str(root_website.decode('utf-8'))        # change type of string
                    for netloc in json_dict[root_website]:                  # use netloc in json_dict
                        netloc = netloc.encode('utf-8').decode('utf-8')     # change unicode to string
                        for website in json_dict[root_website][netloc]:     # get website in dict
                            website = website.encode('utf-8')               # change unicode to string
                            if website not in self.dict_n_ref:              # detect website in dict
                                self.dict_n_ref[website] = 0                # set website in dict and set 0

                            # get child website in list
                            for child_website in json_dict[root_website][netloc][website]["website"]:
                                child_website = child_website.encode('utf-8')

                                # child website not in dict used
                                if child_website not in self.dict_n_ref:
                                    self.dict_n_ref[child_website] = 0      # set website in dict and set 0

                                # child's netloc and website's netloc is not same
                                child_netloc = self.get_netloc(child_website)

                                # detect child netloc not same website netloc
                                if child_netloc != netloc:
                                    self.dict_n_ref[child_website] += 1     # add value in used dict
                read_file.close()                                           # close file
        print "complete : set_n_used : SpiderModelIndexing"

    # save in indexing into string
    def save_to_json_file(self):
        print "start : save_to_json_file : SpiderModelIndexing"
        json_str = json.dumps(self.indexing_dict)           # change dict to string json
        json_file = open("indexing.json", "w+")             # open file to write
        json_file.write(json_str)                           # write in file
        json_file.close()                                   # close file
        print "complete : save_to_json_file : SpiderModelIndexing"
        return json_str

    # method that get netloc from website (website)
    @staticmethod
    def get_netloc(website):
        # print "complete : get_netloc : SpiderModelIndexing"
        return urlparse(website).netloc  # return netloc

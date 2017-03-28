import operator
import json


class SpiderModelRanking:
    def __init__(self):
        self.ranking_dict = {}

    def ranking(self):
        print "start : ranking : SpiderModelRanking"
        file_json = open("indexing.json", "r+")         # open file
        indexing_dict = json.loads(file_json.read())    # get dict from json file
        file_json.close()                               # close file
        for word in indexing_dict:                      # get word from list
            # sort data
            indexing_dict[word] = sorted(indexing_dict[word].items(), key=operator.itemgetter(1), reverse=True)
        self.ranking_dict = indexing_dict               # set dict
        print "complete : ranking : SpiderModelRanking"
        return self.ranking_dict

    # return dict that sorted
    def get_ranking_dict(self):
        return self.ranking_dict

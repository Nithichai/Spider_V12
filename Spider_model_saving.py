import urllib       # Library for get HTML code
import html2text    # Library for change HTML code to text
import re           # Set format or replace word
import json         # Save json format
from urlparse import urlparse   # Set website format


class SpiderModelSaving:
    def __init__(self):
        print "start : init : SpiderModelSaving"
        self.html2text = html2text.HTML2Text()   # set html2text
        self.html2text.ignore_links = False      # care link
        self.html2text.ignore_images = True      # don't care image
        self.html2text.ignore_tables = True      # don't care table
        print "complete : init : SpiderModelSaving"

    # Method to get HTML code (website)
    @staticmethod
    def get_html_code(website):
        print "start : get_html_code : SpiderModelSaving"
        try:
            response = urllib.urlopen(website)      # use urllib for this website
            html_code = response.read()             # get html code
            response.close()                        # stop use urllib
            print "complete : get_html_code : SpiderModelSaving"
            return html_code                        # return html code
        except IOError:                             # Detect error
            print "IOError : get_html_code : SpiderModelSaving"
            return ""                               # return no word

    # Method to get content, website from html (html2text object, html code)
    def get_htmlcode_to_datastr(self, html_code):
        print "start : get_htmlcode_to_datastr : SpiderModelSaving"
        if html_code == "":     # detect no word
            print "no word : get_htmlcode_to_datastr : SpiderModelSaving"
            return ""           # exit this method
        try:
            # Set data from html code
            data_from_html = self.html2text.handle(html_code.decode("utf-8")).encode("utf-8")
            data_str = re.sub("[\n\t\s*]", " ", data_from_html)    # make string
            print "complete : get_htmlcode_to_datastr : SpiderModelSaving"
            return data_str                         # Delete all space for data and return
        except UnicodeDecodeError:                  # Detect UnicodeDecodeError
            print "UnicodeDecodeError : get_htmlcode_to_datastr : SpiderModelSaving"
            return ""                               # retrun no word
        except UnicodeEncodeError:                  # Detect UnicodeDecodeError
            print "UnicodeEncodeError : get_htmlcode_to_datastr : SpiderModelSaving"
            return ""                               # retrun no word

    # Method to get content from datastring (data string)
    @staticmethod
    def get_content_from_datastr(datastr):
        print "start : get_content_from_datastr : SpiderModelSaving"
        if len(datastr) == 0:                                                # detect no word
            print "no word : get_content_from_datastr : SpiderModelSaving"
            return ""
        data_del_website = re.sub(r'\((.*?)\)', "", datastr)                 # delete word in (website)
        data_del_web_content = re.sub(r'\[(.*?)\]', "", data_del_website)    # delete word in [content_weblink]
        if data_del_web_content.strip() != "":                               # detect data has word
            print "complete : get_content_from_datastr : SpiderModelSaving"
            return data_del_web_content.strip()                              # strip space and return content
        return ""

    # Method to get website from datastring (data string)
    def get_website_from_datastr(self, root_website, datastr):
        print "start : get_website_from_datastr : SpiderModelSaving"
        if datastr == "":                                                    # not detect word
            print "no word : get_website_from_datastr : SpiderModelSaving"
            return ""
        list_website = []                                                    # list that save website
        website_list = re.findall(r'\((.*?)\)', datastr)                     # split website(in ()) to list
        for web in website_list:
            web_del_website = re.sub("\"(.*?)\"", "", web).strip()           # delete word in ()
            web_del_website_format = self.website_formatter(root_website, web_del_website)    # Set format to website
            if web_del_website_format != "":    # detect website
                list_website.append(web_del_website_format)                  # add in list
        print "complete : get_website_from_datastr : SpiderModelSaving"
        return list_website                                                  # return list

    @staticmethod
    # Method to get content is linked from datastring (data string)
    def get_weblink_from_datastr(datastr):
        print "start : get_weblink_from_datastr : SpiderModelSaving"
        if datastr == "":                                           # not detect word
            print "no word : get_weblink_from_datastr : SpiderModelSaving"
            return ""                                               # return no word
        all_content = ""                                            # Save all content in this
        data_del_web = re.sub(r'\((.*?)\)', " ", datastr)           # data delete word in () or website
        content_list = re.findall(r'\[(.*?)\]', data_del_web)       # list word in [] or content that is linked
        for content in content_list:                                # get content in list
            if content.strip() != "":                               # detect content
                all_content += content.strip() + " "                # save all content in one
        print "complete : get_weblink_from_datastr : SpiderModelSaving"
        return all_content

    @staticmethod
    # Method that set website format (scheme, netloc and path)
    def website_formatter(main_website, website):
        # print "start : website_formatter : SpiderModelSaving"

        # Detect word that start "./" or "//"
        if len(website) > 0 and (website.find("./") == 0 or website.find("//") == 0):
            website = website.replace(website[0:2], "/")        # Change to "/"
        if len(website) > 0 and website[0] == "/":              # Detect word that start "/" (Found link only)

            # Set main website that is added link in last and strip "/" in last
            website_format = ('{uri.scheme}://{uri.netloc}'
                              .format(uri=urlparse(main_website)).strip("/") + website).strip("/")
            # print "complete : website_formatter : SpiderModelSaving"
            return website_format                                    # return website is formatted
        elif len(website) > 0:                                       # Detect website
            parsed_uri = urlparse(website)                           # Get website par
            if parsed_uri.scheme == "" or parsed_uri.netloc == "":   # Detect website has not scheme or netloc
                print "no word : website_formatter : SpiderModelSaving"
                return ""                                            # return no word
            # print "complete : website_formatter : SpiderModelSaving"

            # Set website format that has scheme, netloc, path only and return it
            return ('{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri)).strip("/")
        else:           # not detect anything
            # print "no word : website_formatter : SpiderModelSaving"
            return ""   # return no word

    # Method that set json string to text file (root website, dict of website, dict of content)
    def get_json_string(self, root_website, website_dict, content_dict):
        print "start : get_json_string : Spider_model_saving"
        root_netloc = self.get_netloc(root_website)                         # get netloc of root website
        dict_to_save = {root_website: {root_netloc: {root_website: {}}}}    # dict that save to json file
        for website in content_dict:                                        # get website in content dict.
            website_netloc = self.get_netloc(website)                       # get netloc of website
            if website_netloc not in dict_to_save[root_website]:  # detect this netloc not in dict
                dict_to_save[root_website][website_netloc] = {website: {}}  # set netloc in dict
            dict_to_save[root_website][website_netloc][website] = {         # set content and child-website in dict
                "content": content_dict.get(website),                       # content
                "website": website_dict.get(website)                        # list of child-website
            }
        print "complete : get_json_string : SpiderModelSaving"
        return json.dumps(dict_to_save)                                     # set dict to json string and return

    # method that get netloc from website (website)
    @staticmethod
    def get_netloc(website):
        # print "complete : get_netloc : SpiderModelSaving"
        return urlparse(website).netloc     # return netloc

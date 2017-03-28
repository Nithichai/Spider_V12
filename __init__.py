from Spider_Control import SpiderControl
from nodebox.graphics import *  # Library for draw canvas


def website_update(button):
    spider.start_search_website_thread()


def show_graph(button):
    spider.start_to_show()


def indexing(button):
    spider.start_to_indexing()


def searching_word(button):
    spider.start_to_searching()


def pause_deep(button):
    spider.pause_deep()


def draw(my_canvas):
    spider.spider_view.draw_graph(my_canvas)


spider = SpiderControl()
spider.spider_view.set_website_update(website_update)
spider.spider_view.set_show_output(show_graph)
spider.spider_view.set_indexing(indexing)
spider.spider_view.set_go(searching_word)
spider.spider_view.set_pause(pause_deep)
spider.spider_view.set_gui(canvas)
canvas.run(draw)


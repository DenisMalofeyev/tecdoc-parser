# -*- coding: utf-8 -*-

def get_from_xpath(sel, xpath_str, n=0):
    return sel.xpath(xpath_str).extract()[n]

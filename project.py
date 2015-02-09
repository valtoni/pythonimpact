# -*- coding: utf-8 -*-
'''
Created on 09/02/2015
@author: Valtoni Boaventura (valtoni@gmail.com)
'''

class Project:
  def __init__(self, urlroot, url):
    self.url = url
    self.rawdir = url.replace(urlroot, "")
    self.name = ""
    
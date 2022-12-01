'''Contains Structure of each class object'''

from anytree import NodeMixin
class Location(NodeMixin):
     def __init__(self, Hex_val, x1=0, y1=0, x2=0,y2=0,parent=None, children=None):
         self.Hex_val = Hex_val
         self.x1 = x1
         self.y1 = y1
         self.parent=parent
         if children:
             self.children = children

     def __str__(self):
       return "Location " + str(self.Hex_val) + ": Bottom Right = {}, Top Left =  {}".format(self.x1, self.y1)
import sys
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from lxml import etree
import xmldiff
import glob
from io import StringIO
from xmldiff import main
from xmldiff import formatting
import csv


print(sys.version)
print(sys.executable)
formatter=formatting.XMLFormatter(normalize=formatting.WS_NONE,pretty_print=True)


#nsmap['gbd']=""
def greet():
    
    tree1=[]
    for filename in glob.iglob("/Users/sachin/Documents/*.xml"):
        tree1.append((filename))
    
    print(tree1)
    x1=etree.parse("/Users/sachin/Documents/first.xml")
    x2=etree.parse("/Users/sachin/Documents/file2.xml")

    print(x1)
    print(x2)

    root1=x1.getroot()
    root2=x2.getroot()

    print(root1)
    print(root2)    
    
    result = xmldiff.main.diff_trees(root1, root2)

# convert the XPath expressions to full tag paths
    

    diff = etree.diff(x1, x2)

# Print the tag paths for the differences
    for action, elem in diff:
        if action == 'add':
            print("Element added:", elem.tag, elem.getroottree().getpath(elem))
        elif action == 'delete':
            print("Element deleted:", elem.tag, elem.getroottree().getpath(elem))
        elif action == 'change':
            print("Element changed:", elem.tag, elem.getroottree().getpath(elem))


    converted_result = []
    for change in result:
        node_path = change.node
        node = root1.xpath(node_path)[0]

        path = [node.tag]
        parent = node.getparent()
        while parent is not None:
            path.insert(0, parent.tag)
            parent = parent.getparent()

        full_path = "/".join(path)
        
        
    print(converted_result)


        
    
    
    #print(root.attrib)
    
    #print(ET.tostring(root))
    with open(tree1[0],"r") as f1,open(tree1[1],"r") as f2:
        result=main.diff_files(f1,f2)
    #print(result)
   
    with open('output.csv','w',newline='') as file:
        writer=csv.writer(file)
        writer.writerows(result)
    
    return result


print(greet())




from timeit import default_timer as timer
from lxml import etree
import re
import io

def compare_xml_trees(left_tree, right_tree):
    left_root = left_tree.getroot()
    right_root = right_tree.getroot()

    left_elements = [left_root]
   
    right_elements = [right_root]
    
    output=[]
    while left_elements or right_elements:
        if not left_elements:
            output.append(("Element added:", right_elements[0].tag, right_tree.getelementpath(right_elements[0]),"Missing",right_element[0].tag))
            right_elements.pop(0)
        elif not right_elements:
            output.append( ("Element deleted:", left_elements[0].tag, left_tree.getelementpath(left_elements[0]),"Missing",left_element[0].tag))
            left_elements.pop(0)
        else:
            left_element = left_elements.pop(0)
            right_element = right_elements.pop(0)
            if left_element.tag != right_element.tag:
                output.append( ("Element changed:", left_element.tag, left_tree.getelementpath(left_element),left_element.tag,right_element.tag))
            elif left_element.text != right_element.text:
                output.append(("Text changed:", left_element.tag, left_tree.getelementpath(left_element),left_element.text,right_element.text))
            else:
                left_attrib = left_element.attrib
                right_attrib = right_element.attrib
                if left_attrib != right_attrib:
                    output.append(("Attribute changed:", left_element.tag, left_tree.getelementpath(left_element),left_element.attrib,right_element.attrib))
                left_elements = left_element.getchildren() + left_elements
                right_elements = right_element.getchildren() + right_elements

    for i, text in enumerate(output):
        output[i] = (text[0], text[1].replace("{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}", ""), text[2].replace("{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}", ""),text[3],text[4])

    print(output)


# Load the two XML files


start=timer()

# Parse XML from file 1
with open("first.xml", "r") as f:
    xml_string1 = f.read()
with open("file2.xml", "r") as f:
    xml_string2 = f.read()

# Use regular expression to extract CDATA content
cdata_pattern = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)
xml_content1 = cdata_pattern.search(xml_string1)
xml_content2 = cdata_pattern.search(xml_string2)

# If CDATA content is found, extract it and parse as XML
if xml_content1:
    xml_string1 = xml_content1.group(1)
    root1 = etree.parse(io.StringIO(xml_string1))
if xml_content2:
    xml_string2 = xml_content2.group(1)
    root2 = etree.parse(io.StringIO(xml_string2))



x1 = (root1)
x2 = (root2)

# Find the differencesc
compare_xml_trees(x1, x2)
end=timer()

print(end-start)
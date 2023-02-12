from lxml import etree

def compare_xml_trees(left_tree, right_tree):
    left_root = left_tree.getroot()
    right_root = right_tree.getroot()

    left_elements = [left_root]
   
    right_elements = [right_root]
    
    output=[]
    while left_elements or right_elements:
        if not left_elements:
            output.append(("Element added:", right_elements[0].tag, right_tree.getelementpath(right_elements[0])))
            right_elements.pop(0)
        elif not right_elements:
            output.append( ("Element deleted:", left_elements[0].tag, left_tree.getelementpath(left_elements[0])))
            left_elements.pop(0)
        else:
            left_element = left_elements.pop(0)
            right_element = right_elements.pop(0)
            if left_element.tag != right_element.tag:
                output.append( ("Element changed:", left_element.tag, left_tree.getelementpath(left_element)))
            elif left_element.text != right_element.text:
                output.append(("Text changed:", left_element.tag, left_tree.getelementpath(left_element),left_element.text,right_element.text))
            else:
                left_attrib = left_element.attrib
                right_attrib = right_element.attrib
                if left_attrib != right_attrib:
                    output.append(("Attribute changed:", left_element.tag, left_tree.getelementpath(left_element)))
                left_elements = left_element.getchildren() + left_elements
                right_elements = right_element.getchildren() + right_elements

    for i, text in enumerate(output):
        output[i] = (text[0], text[1].replace("{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}", ""), text[2].replace("{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}", ""),text[3],text[4])

    print(output)


# Load the two XML files



x1=etree.parse("/Users/sachin/Documents/first.xml")
x2=etree.parse("/Users/sachin/Documents/file2.xml")

# Find the differences
compare_xml_trees(x1, x2)
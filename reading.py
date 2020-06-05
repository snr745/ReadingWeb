from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import xml.etree.ElementTree as ET
from pathlib import Path
import os.path as OsPath
from datetime import date
from xml.dom import minidom

myFile=Path("C:\Learning\WebReading1\GoldRates.xml")
#if OsPath.is
tree=""
root1=""
GoldrateElement=""
carat_24_parsed=False

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def CreateorGetXmlFile():
    global root1
    global tree
    try:
        tree=ET.parse("C:\Learning\WebReading1\GoldRates.xml")
        print("try Block")
        root1 = tree.getroot()
    except FileNotFoundError:
        rt=ET.Element("Root")
        tree=ET.ElementTree(rt)
        tree.write("C:\Learning\WebReading1\GoldRates.xml")
        tree=ET.parse("C:\Learning\WebReading1\GoldRates.xml")
        root1=tree.getroot()




def Handle22Carat(table1):
    global GoldrateElement
    row=table1.find("i")
    print("22 Carat Value:"+row.parent.text)
    print(type(root1))
    print(type(str(date.today())))
    GoldrateElement=ET.SubElement(root1,'GoldRates')
    GoldrateElement.set("Date",str(date.today()))
    goldRate=ET.SubElement(GoldrateElement,"GoldRate")
    goldRate.set("Carat","22")
    goldRate.text=row.parent.text.replace("₹","")
    #GoldrateElement.append(goldrate)
    #root1.append(GoldrateElement)



def Handle24Carat(table1):
    global carat_24_parsed
    row=table1.find("i")
    carat_24_parsed= not carat_24_parsed
    print("24 Carat Value:"+row.parent.text)
    goldRate=ET.SubElement(GoldrateElement,"GoldRate")
    goldRate.set("Carat","24")
    goldRate.text=row.parent.text.replace("₹","")
    #tree.toprettyxml()
    tree=ET.ElementTree(ET.fromstring(prettify(root1)))
    print(str(prettify(root1)))
    tree.write("C:\Learning\WebReading1\GoldRates.xml")
   


link = "https://www.goodreturns.in/gold-rates/chennai.html"
f = urlopen(link)
myfile = f.read()
with open("C:\Learning\WebReading1\log.txt","w+") as text_file:
    print(myfile,file=text_file)
CreateorGetXmlFile()
soup =BS(myfile,'html.parser')
table=soup.find("div",class_ = "gold_silver_table")
for div in soup.find_all("div",class_ = "gold_silver_table"):
    table=div.find("table").text
    if "22 Carat Gold" in table:
        Handle22Carat(div.find("table"))
    else:
        if  carat_24_parsed == False:
            Handle24Carat(div.find("table"))
        print("yes 24")
tree.write("C:\Learning\WebReading1\GoldRates.xml")

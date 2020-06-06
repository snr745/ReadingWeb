from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import xml.etree.ElementTree as ET
from pathlib import Path
import os.path as OsPath
from datetime import *
from xml.dom import minidom
import logging

logging.basicConfig(handlers=[logging.FileHandler('Applog.txt', 'w', 'utf-8')],level=logging.DEBUG)
tree=""
root1=""
GoldrateElement=""
carat_24_parsed=False
GoldRates_Updated=True

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
        tree=ET.parse("GoldRates.xml")
        root1 = tree.getroot()
        logging.info("Successfully Parsed the File"+"GoldRates.xml")
    except FileNotFoundError:
        rt=ET.Element("Root")
        tree=ET.ElementTree(rt)
        tree.write("GoldRates.xml")
        tree=ET.parse("GoldRates.xml")
        root1=tree.getroot()
        logging.info("Successfully Created the File"+"GoldRates.xml")




def Handle22Carat(table1):
    global GoldrateElement
    global GoldRates_Updated
    row=table1.find("i")
    logging.info("22 Carat Value:"+row.parent.text)
    today_Date=str(date.today())
    xpath1=".//*[@Date='"+today_Date+"']"
    existingGoldrates=root1.findall(xpath1)
    if not existingGoldrates:
        GoldRates_Updated=False
        GoldrateElement=ET.SubElement(root1,'GoldRates')
        GoldrateElement.set("Date",str(date.today()))
        goldRate=ET.SubElement(GoldrateElement,"GoldRate")
        goldRate.set("Carat","22")
        goldRate.text=row.parent.text.replace("₹","")

    



def Handle24Carat(table1):
    global carat_24_parsed
    row=table1.find("i")
    carat_24_parsed= not carat_24_parsed
    logging.info("24 Carat Value:"+row.parent.text)
    if not GoldRates_Updated:
        goldRate=ET.SubElement(GoldrateElement,"GoldRate")
        goldRate.set("Carat","24")
        goldRate.text=row.parent.text.replace("₹","")
        tree=ET.ElementTree(ET.fromstring(prettify(root1)))
        tree.write("GoldRates.xml")
        logging.info("Successfully Written Xml File")

    
def loadUrl():
    link = "https://www.goodreturns.in/gold-rates/chennai.html"
    f = urlopen(link)
    myfile = f.read()
    with open("logFile.txt","w+") as text_file:
        print(myfile,file=text_file)
    return myfile

def ParseFileContents(myfile):
    soup =BS(myfile,'html.parser')
    table=soup.find("div",class_ = "gold_silver_table")
    for div in soup.find_all("div",class_ = "gold_silver_table"):
        table=div.find("table").text
        if "22 Carat Gold" in table:
            Handle22Carat(div.find("table"))
        else:
            if  carat_24_parsed == False:
                Handle24Carat(div.find("table"))
            
def main():
    logging.info("Apllication Starting At:::::"+str(datetime.now()))
    fileData= loadUrl()
    CreateorGetXmlFile()
    ParseFileContents(fileData)


if __name__ == "__main__":
    main()
import xml.etree.ElementTree as ET
import sys
import xlsxwriter
import re
rules_list = list()
fname=sys.argv[1]
xml = ET.parse(fname)
root1 = xml.getroot()
root = root1.find('.knowledgeBase/kbaSet')


def getDataRecursive(element):
    data = list()

    # get attributes of element, necessary for all elements
    for key in element.attrib.keys():
        data.append(element.tag + '.' + key + ' ' + element.attrib.get(key))

    # only end-of-line elements have important text, at least in this example
    if len(element) == 0:
        if element.text is not None:
            data.append(element.tag + ' ' + element.text)

    # otherwise, go deeper and add to the current tag
    else:
        for el in element:
            within = getDataRecursive(el)

            for data_point in within:
                data.append(element.tag + '.' + data_point)

    return data

for x in getDataRecursive(root):
    rules_list.append(x)
fw=open(fname.replace(".xml",".txt"),"w")
fw.write("\n_____________")
for values in rules_list:
    #print(values)
    fw.write("\n"+values)
fw.write("\n_____________")
fw.close()

rules_list=list()
fw=open(fname.replace(".xml",".txt"),"a")
xml = ET.parse(fname)
root=xml.getroot()
for x in getDataRecursive(root):
    if "rule" in x:
        rules_list.append(x)

for values in rules_list: 
    if("targets" in values):
        fw.write("\n###")
        #print("#########")
        fw.write(values)
        #print(values)
    if("userData" in values):
        #print(values)
        fw.write(values)
fw.close()


rw=0
workbook = xlsxwriter.Workbook(fname.replace(".xml","").upper()+"_Geneos_Parsed.xlsx")
worksheet = workbook.add_worksheet("KB in Geneos")
worksheet.write(rw,0,'KB Target')
worksheet.write(rw,1,'KB URL')
kb_str=""
fw=open(fname.replace(".xml",".txt"),"r")
kb_str_1=""
kb_str_2=""
for each_item in fw.readlines():
    #print(each_item)
    if("kbaSet.kba.label" in each_item):
        kb_str_1 ="KB Label :"+each_item.replace("\n","")
    if("kbaSet.kba.urlElements.urlElement.literal" in each_item):
        kb_str_2=kb_str_1+",""KB URL :"+each_item.replace("\n","")
        kb_str_1=""
        
    #print(kb_str_2)
    if(len(kb_str_2)>0):
        fnl=kb_str_2.split(",")
        rw += 1
        worksheet.write(rw,0,fnl[0])
        worksheet.write(rw,1,fnl[1])
    kb_str_2=""
fw.close()
rw=0
worksheet2 = workbook.add_worksheet("Emails in Geneos")
worksheet2.write(rw,0,'EMAIL Target')
worksheet2.write(rw,1,'Emails')
regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
flg=0
fw=open(fname.replace(".xml",".txt"),"r")
for each_item in fw.readlines():
    if("###" in each_item):
        flg=1
    
    if(flg):
        #print(each_item)
        if(re.search(regex,each_item)):
            res=re.search(regex, each_item)
            str_eml=each_item[each_item.find("["):each_item.rfind("]")]+" : "+each_item[res.start():each_item.rfind(".com")]+".com"
            ##print(str_eml)
            if(re.search(regex,str_eml)):
                str_tgt=each_item[each_item.find("["):each_item.rfind("]")]
                str_emlval=each_item[res.start():each_item.rfind(".com")]+".com"
                if(len(str_emlval)>0):
                    rw += 1
                    worksheet2.write(rw,0,str_tgt)
                    worksheet2.write(rw,1,str_emlval)
                str_emlval=""
                str_tgt=""
fw.close()
workbook.close()

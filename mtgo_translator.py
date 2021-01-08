import lxml.etree
import glob
import json
import progressbar

#language code used by scryfall: https://scryfall.com/docs/api/languages
language="es"
#work path containing the mtgo CardDataSource folder
path=r'd:\\mtgo\\'
#load file with the card names
card_names = lxml.etree.parse(path+r'CardDataSource\CARDNAME_STRING.xml')
#load file with the card text
oracle_text = lxml.etree.parse(path+r'CardDataSource\REAL_ORACLETEXT_STRING.xml')
#list all set files
set_files = glob.glob(path + r'CardDataSource\client_*.xml')
#load scryfall all cards json donwloaded from https://scryfall.com/docs/api/bulk-data
json_file=open(path+"all-cards-20201223101905.json", encoding='utf-8')
cards=json.load(json_file)

#loop over each set
for set_file in set_files:
    count=0
    card_set = lxml.etree.parse(set_file)
    #get set code from the game file
    set_code = card_set.getroot().attrib['id']
    print(set_code)
    bar = progressbar.ProgressBar(max_value=len(card_set.xpath('./DigitalObject')))
    #loop over each card in the set
    for card_id in card_set.xpath('./DigitalObject'):
            count+=1
            bar.update(count)
            #find the mtgo id from the file
            mtgo_id=int(card_id.attrib['DigitalObjectCatalogID'].split("_")[1])
            #loop over the elemnts of the xml section of the card to find the id for the card name and the card text
            for element in card_id.iter():
                if element.tag == 'CARDNAME_STRING':
                    name_id=element.attrib['id']
                if element.tag == 'REAL_ORACLETEXT_STRING':
                    text_id=element.attrib['id']
            found=False
            #first loop to locate the card in english
            for card_info in cards:
                #check if the card matches the mtgo id
                if 'mtgo_id' in card_info.keys():
                    #due to issues with cards with several faces we skip them in this version of the script
                    if 'card_faces' in card_info.keys():
                        continue
                    #check if the card id and the set matches
                    if card_info['mtgo_id']==mtgo_id and card_info['set'] == set_code.lower():
                        #as the collector number and the set matches for all languages we use it to find the json entry for our language
                        card_es=card_info['collector_number']
                        #second loop looking for the card in the specified language
                        for card_meta in cards:
                            if card_meta['collector_number'] == card_es and card_meta['set']==set_code.lower() and card_meta['lang'] == language:
                                #if the cards is found update the entry in the output xml
                                found=True
                                card_name=card_names.xpath("./CARDNAME_STRING_ITEM[@id='"+name_id+"']")[0]
                                card_text=oracle_text.xpath("./REAL_ORACLETEXT_STRING_ITEM[@id='"+text_id+"']")[0]
                                card_name.text = card_meta['printed_name']
                                lxml.etree.ElementTree(card_names.getroot()).write(path+r'CARDNAME_STRING.xml', pretty_print=True)
                                if 'printed_text' in card_meta.keys():
                                    card_text.text = card_meta['printed_text']
                                    lxml.etree.ElementTree(oracle_text.getroot()).write(path+r'REAL_ORACLETEXT_STRING.xml', pretty_print=True)
                if found:
                    #if the card was not found stop the loop to avoid innecesary work
                    break

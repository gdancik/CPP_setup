import pubmed_parser as pp
pubmed_dict = pp.parse_medline_xml('pubmedsample18n0001.xml')
for item in pubmed_dict:
    print(item['title'] + item['abstract'] + item['journal'] + 
          item['author'] + item['pubdate'] + '\n')
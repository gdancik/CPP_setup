import pubmed_parser as pp
pubmed_dict = pp.parse_medline_xml('pubmedsample18n0001.xml')
for item in pubmed_dict:
    print(item['title'] + '\n' + item['abstract'] + '\n' + item['journal'] + '\n' +
          item['author'] + '\n' + item['pubdate'] + '\n')
import re
from bs4 import BeautifulSoup
import extraction_text_manip

'''The purpose of this python file is to help you build the code needed to extract articles from websites'''


url="http://www.livemint.com/Companies/fghWAFAu1k7JYKnUU31g4I/Nestle-asks-Bombay-HC-for-time-to-reply-to-Maharashtra-FDA-a.html"
website=extraction_text_manip.extract_website(url)

html=extraction_text_manip.get_html(url)

#We must set the following:
article_headline=""
article_alt_headline_list=[]
article_text=""

article_soup=BeautifulSoup(html)
with open("G:/article.html", 'w') as art_file:
	art_file.write(article_soup.prettify().encode('ascii','ignore'))





					#start of website-specific code
					#input: article_soup
website_base_url="livemint.com" 

headline_list=article_soup.find("h1", {"class":"sty_head_38"})
article_headline=""
for i in headline_list:
	article_headline+=extraction_text_manip.properly_encode(str(i))
article_headline=extraction_text_manip.properly_format(article_headline)

article_alt_headline_list=[]
alt_headline_list=article_soup.find("div", {"class":"sty_sml_summary_18"})
article_alt_headline=""
for i in alt_headline_list:
	article_alt_headline+=extraction_text_manip.properly_encode(str(i))
article_alt_headline=extraction_text_manip.properly_format(article_alt_headline)
article_alt_headline_list.append(article_alt_headline)


date_list=article_soup.findAll("div", {'class':"sty_posted_txt"})
article_dateline=""
for i in date_list:
	article_dateline+=extraction_text_manip.properly_encode(str(i))
# print article_dateline
article_dateline=extraction_text_manip.remove_HTML_tags(article_dateline)
article_dateline_list=article_dateline.split(":")
for i in range(0, len(article_dateline_list)):
	article_dateline_list[i]=article_dateline_list[i].strip()
article_date_and_time=article_dateline_list[1]
article_locality=""



text_list= article_soup.findAll("div", {'class':"text"})
article_text=(str(text_list[0]))
# article_text=""
# for i in text_list:
# 	article_text+=extraction_text_manip.properly_encode(str(i))
article_text = extraction_text_manip.remove_HTML(article_text, "strong", 'class="read_more"')
article_text = extraction_text_manip.remove_HTML_tags(article_text)
article_text = extraction_text_manip.properly_encode(article_text)
article_text = extraction_text_manip.properly_format(article_text)


					# end of website-specific code
					# output: article_headline, article_alt_headline_list, article_text, etc. saved in an ArticleObject

# print "\n\nDATELINE:\t"+article_date_and_time
print "\n\nHEADLINE:\t"+article_headline
for article_alt_headline in article_alt_headline_list:
	print "\n\nALT HEADLINE:\t"+article_alt_headline
print "\n\n"+article_text



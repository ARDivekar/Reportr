#Article Extraction test case


import db_setup
import extract




conn=db_setup.init_db()


website_code_dict={
"livemint.com" :

'''
					#start of website-specific code
					#input: article_soup, from function def soup_recepie(url)
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
					# output: article_headline, article_alt_headline_list, article_text
''',

"timesofindia.indiatimes.com" :
''' 
					#start of website-specific code
					#input: article_soup, from function def soup_recepie(url)
website_base_url="timesofindia.indiatimes.com" 
website_addendum=["/business/india-business/"] 
#website_base_url+website_addendum[i] = base for extracting

headline_list=article_soup.select("span.arttle h1") #find("div", {"class":"title"})
article_headline=""
for i in headline_list:
	article_headline+=extraction_text_manip.properly_encode(extraction_text_manip.remove_HTML_tags(str(i)))
article_headline=extraction_text_manip.properly_format(article_headline)


article_alt_headline_list=[]

date_list=article_soup.findAll("span", {'class':"byline"})
article_dateline=""
for i in date_list:
	article_dateline+=extraction_text_manip.properly_encode(str(i))
# print article_dateline
article_dateline=extraction_text_manip.remove_HTML_tags(article_dateline)
article_dateline_list=article_dateline.split("|")
for i in range(0, len(article_dateline_list)):
	article_dateline_list[i]=article_dateline_list[i].strip()
article_date_and_time=article_dateline_list[1]
article_locality=""




text_list= article_soup.findAll("div", {'class':"Normal"})
article_text=str(text_list[0])
# article_text=""
# for i in text_list:
# 	article_text+=extraction_text_manip.properly_encode(str(i))
article_text = extraction_text_manip.remove_HTML(article_text, "div", 'class="fpublish"')
article_text = extraction_text_manip.remove_HTML_tags(article_text)
article_text = extraction_text_manip.properly_encode(article_text)
article_text = extraction_text_manip.properly_format(article_text)


					# end of website-specific code
					# output: article_headline, article_alt_headline_list, article_text
''',

"financialexpress.com":

'''
					#start of website-specific code
					#input: article_soup, from function def soup_recepie(url)
website_base_url="financialexpress.com" 
website_addendum=["/article/companies/", "/article/industry/"] 
#website_base_url+website_addendum[i] = base for extracting

headline_list=article_soup.select("div.title h1") #find("div", {"class":"title"})
article_headline=""
for i in headline_list:
	article_headline+=extraction_text_manip.properly_encode(extraction_text_manip.remove_HTML_tags(str(i)))
article_headline=extraction_text_manip.properly_format(article_headline)


article_alt_headline_list=[]
alt_headline_list=article_soup.find("h2", {"class":"synopsis"})
article_alt_headline=""
for i in alt_headline_list:
	article_alt_headline+=extraction_text_manip.properly_encode(str(i))
article_alt_headline=extraction_text_manip.properly_format(article_alt_headline)
article_alt_headline_list.append(article_alt_headline)


date_list=article_soup.select("div.dateline")
article_dateline=""
for i in date_list:
	article_dateline+=extraction_text_manip.properly_encode(str(i))

article_dateline=extraction_text_manip.remove_HTML(str=article_dateline, tag="span", attributes="")
article_dateline=extraction_text_manip.remove_HTML(str=article_dateline, tag="a", attributes="")
article_dateline=extraction_text_manip.remove_HTML_tags(str=article_dateline)
article_dateline_list=article_dateline.split("|")
for i in range(0, len(article_dateline_list)):
	article_dateline_list[i]=article_dateline_list[i].strip()
article_dateline_list=extraction_text_manip.remove_empty_from_list(article_dateline_list)
article_date_and_time=article_dateline_list[0]


text_list= article_soup.findAll("div", {'class':"main-story"})
# article_text=extraction_text_manip.properly_encode(str(text_list[0]))
article_text=""
for i in text_list:
	article_text+=extraction_text_manip.properly_encode(str(i))
article_text = extraction_text_manip.remove_HTML(article_text, "div", 'class="fpublish"')
article_text = extraction_text_manip.remove_HTML_tags(article_text)
article_text = extraction_text_manip.properly_encode(article_text)
article_text = extraction_text_manip.properly_format(article_text)


					# end of website-specific code
					# output: article_headline, article_alt_headline_list, article_text

''',




"business-standard.com" :
'''
					#start of website-specific code
					#input: article_soup, from function def soup_recepie(url)
# s=misc_functions.Stopwatch()
# s.start()
website_base_url="business-standard.com" 
website_addendum=["/article/companies/", "/article/industry/"] 
#website_base_url+website_addendum[i] = base for extracting

headline_list=article_soup.find("h1", {"itemprop":"headline"})
article_headline=""
for i in headline_list:
	article_headline+=extraction_text_manip.properly_encode(str(i))
article_headline=extraction_text_manip.properly_format(article_headline)
# print "\tTime needed to extract headline: "+str(s.lap())+" seconds."


article_alt_headline_list=[]
alt_headline_list=article_soup.find("h3", {"itemprop":"alternativeHeadline"})
article_alt_headline=""
for i in alt_headline_list:
	article_alt_headline+=extraction_text_manip.properly_encode(str(i))
article_alt_headline=extraction_text_manip.properly_format(article_alt_headline)
# print "\tTime needed to extract alt-headline: "+str(s.lap())+" seconds."
article_alt_headline_list.append(article_alt_headline)



text_list= article_soup.findAll("div", {'class':"colL_MktColumn2"})
article_text=str(text_list[0])
# article_text=""
# for i in text_list:
# 	article_text+=extraction_text_manip.properly_encode(str(i))
article_text = extraction_text_manip.remove_HTML(article_text, "strong", 'class="read_more"')
article_text = extraction_text_manip.remove_HTML_tags(article_text)
article_text = extraction_text_manip.properly_encode(article_text)
article_text = extraction_text_manip.properly_format(article_text)

# print "\tTime needed to extract article text: "+str(s.lap())+" seconds."
					# end of website-specific code
					# output: article_headline, article_alt_headline_list, article_text

'''
}

try:
	db_setup.website_regex_insert(conn, website_code_dict)
except Exception:
	print "Duplicate entry."



site_list=['financialexpress.com/article/', 'business-standard.com/article', 'livemint.com/companies', 'timesofindia.indiatimes.com/business/india-business/ ']

extract.build_giant_profile(topic='Indigo', site_list=site_list, root_filepath="./test example/", number_of_months=3, articles_per_month=15)






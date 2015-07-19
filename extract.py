# -*- coding: utf-8 -*-
import re
import time
from bs4 import BeautifulSoup
import article_manip
import google_manip
import os
import random
import db_setup
import datetime
import extraction_text_manip

conn = db_setup.get_conn()
	


def build_giant_profile(topic, root_filepath, site_list=None, number_of_months=12, articles_per_month=20, end_date=None, start_date=None):	
	#eg: start_date=2456074, end_date=2456554
	if end_date==None:
		now=datetime.datetime.now()
		end_date=extraction_text_manip.to_julian_date(now.year, now.month, now.day)
	if start_date==None:
		start_date=end_date-number_of_months*30 #assume for simplicity each month has the same numeber of days
	

	articleObjs=[]
	article_urls_list=[]
	
	root_filepath=extraction_text_manip.make_folder_path(root_filepath)
	base_filepath = extraction_text_manip.make_folder_path(root_filepath+topic)
	if not os.path.exists(base_filepath):
		os.makedirs(base_filepath)
	total_repeat_count=0
	total_url_count=0


	

	for i in range(0,number_of_months):

		if end_date-i*30 <= start_date:
			print "DONE"
			exit(0)

		daterange_from=max(start_date,end_date-(i+1)*30) #to make __sure__ it does not go beyond the start date
		daterange_to=end_date-i*30
		directory_name = "%s-%s"%(daterange_from,daterange_to)
		folderpath = base_filepath+directory_name
		print "\n>>> Current directory: %s"%folderpath
		if not os.path.exists(folderpath):
			os.makedirs(folderpath)

		some_text=None
		if len(articleObjs)>0:
			some_text=articleObjs[random.randrange(0,len(articleObjs))].article_text

		query=extraction_text_manip.make_google_search_query(topic_list=[topic], site_list=site_list, daterange_from=daterange_from, daterange_to=daterange_to)	
		print '>>> Google search Query: \n%s'%query
		print ">>> Getting search results..."
		results= google_manip.google_search_results(search_query=query, number_of_results=articles_per_month, random_text=some_text)
		counter=1

		print ">>> Number of results found: %s"%len(results)
		if len(results)>0:
			print ">>> Results : \n"+ str([(res.url) for res in results])
		else: 
			print "It seems your IP is getting blocked by Google. Wait some time (at least half an hour) before trying again, or switch to a different internet connection."
			exit(0)
		print "\n\n"
		url_count=1
		repeat_count=1
		for res in results:
			existing_files = [ f for f in os.listdir(folderpath) if os.path.isfile(folderpath+"/"+f) ]
			for existing_file_name in existing_files:
				with open(folderpath+"/"+existing_file_name) as existing_file:
					existing_url=re.findall('(?<=__URL__:).*?(?=\\n)', existing_file.read(), re.I)
					existing_url=existing_url[0]
					article_urls_list.append(existing_url)

			article_urls_list=list(set(article_urls_list))

			if res.url not in article_urls_list:
				print "\n\n%s. %s"%(url_count,res.url)
				# time.sleep(1)
				htmlObj= article_manip.HTML_page_Obj(res.url)
				if htmlObj.url!= None:
					art=article_manip.ArticleObject(HTML_page_Obj=htmlObj, conn=conn)
					print ">>> Writing article to file..."
					if art.write_to_file(folderpath):
						print ">>> Write to file status: SUCCESS!"
						articleObjs.append(art)
					else: print ">>> Write to file status: unsuccessful."
				article_urls_list.append(res.url)
				url_count+=1
				total_url_count+=1
			else: 
				repeat_count+=1
				total_repeat_count+=1

		if len(articleObjs)!=0:
			for x in range(0,random.randrange(1,3)):
				some_text=""
				while some_text == "" or some_text is None:
					some_text=articleObjs[random.randrange(0,len(articleObjs))].article_text
				google_manip.google_search_redirect(some_text)
	print "\n\n>>> Number of urls found: %s"%len(article_urls_list)
	print ">>> Total number of repeat urls: %s out of %s"%(total_repeat_count, total_repeat_count+total_url_count)
	print ">>> Number of articles obtained in this session: %s"%len(articleObjs)







# exec(webextcode[text_manip.extract_website(url)])

# print "\n\nDATELINE:\t"+article_date_and_time
# print "\n\nHEADLINE:\t"+article_headline
# for article_alt_headline in article_alt_headline_list:
# 	print "\n\nALT HEADLINE:\t"+article_alt_headline
# print "\n\n"+article_text

# print "\n\n\n\n\tTotal time taken: "+str(s.stop())+" seconds."






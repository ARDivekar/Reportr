import urllib2
import re
from bs4 import BeautifulSoup
import pickle
import extraction_text_manip
import simpleMySQL
import os

class HTML_page_Obj: #uses urllib2
	
	'''	
	class members (usable after constuctor):
		url : the page url
		short_url : a shortened url (if possible to shorten)
		html : the html of the webpage
		charset : the charset used to encode the HTML
		headers : a dictionary of the other miscellaneous headers which might or might not be present.
	
	class functions:
		__init__ : the constructor that sets all the above variables

		all_hyperlinks : returns a dictionary of all hyperlinks in the html code

		html_prettify : prettifies the html by using BeautifulSoup.prettify()

		get_response_object : internal method, not meant for external use

	'''

	def __init__(self, page_url):
		response=None
		self.url=None
		try: 
			response=self.get_response_object(page_url)
		except Exception:
			try:
				# time.sleep(1)
				response=self.get_response_object(page_url)
			except Exception:
				try:
					# time.sleep(5)
					response=self.get_response_object(page_url)
				except Exception:
					print "\nTried 3 times. Cannot access url: %s. \nHence, cannot make HTML_page_Obj\n"%page_url
		if response != None:

			self.url=page_url
			try:
				self.short_url=response.headers.getparam('Link')
			except Exception:
				self.short_url=""
			self.charset = response.headers.getparam('charset')
			self.headers={'charset':self.charset}
			for i in response.headers:
				self.headers[i]=response.headers[i].split(';')[0]

			self.html = response.read()  #the actual html
		

	def all_hyperlinks(self):
		article_soup=BeautifulSoup(self.html)
		self.link_dict={}
		for link_tag in article_soup.find_all('a'):
			self.link_dict[link_tag.contents[0].strip()]=link_tag.get('href')
			# this makes a dict of the form {'article_headline':'article_hyperlink'}
		return self.link_dict	

	def html_prettify(self):
		html_soup= BeautifulSoup(self.html)
		self.html=html_soup.prettify(encoding=self.charset)
		return html_soup

	def get_response_object(self, page_url):
		if 'http://'  in page_url.lower():
			response =urllib2.urlopen(page_url)
		elif 'https://' in page_url.lower():
			response=urllib2.urlopen('https://'+page_url.split("https://")[-1])
		else:
			response =urllib2.urlopen('http://'+page_url)
		return response







class ArticleObject:
	'''
	class members (usable after constructor):
		article_url : the url of the article
		article_headline : the headline of the article
		article_alt_headline_list : a list of all the alternate headlines of the article
		article_text : the text of the article


	class functions:
		__init__ (self, HTML_page_Obj, conn) : the constructor, used to initialize the above member variables.

		make_from_file (self, article_file_path) : converts the article.txt made by write_to_file() back into an Article Object. 
		
		write_to_file : creates a file to dump the article url, headlines and text into. The name of this file is the article_headline, formatted so that it can be used at a filename.

		article_supersplit : constucts a properly_format()'ed, split of the article. It is structured as:
				a list of paragraphs,
					where each paragraph is a list of sentences,
						where each sentence is a list of words, punctuations as seperate words. Note: the sentences are split naively on the periods.

	'''

	def __init__ (self,conn, HTML_page_Obj=None, article_file_path=None):
		if HTML_page_Obj==None and article_file_path!=None:
			make_from_file(article_file_path)
		elif HTML_page_Obj!=None and article_file_path==None:
			self.article_url=HTML_page_Obj.url
			website_base_url=extraction_text_manip.extract_website(self.article_url)
			print "\n Making article found on %s"%website_base_url
			self.article_headline=""
			self.article_alt_headline_list=[]
			self.article_text=""
			article_soup=HTML_page_Obj.html_prettify()
			table = simpleMySQL.verified_select(conn=conn, select_query="select * from website_regex where base_url='%s' order by date_of_addition desc;" %website_base_url)

			if table is not None:
				for i in range(0,len(table)):
					try_code=table[i][1]
					# print try_code
					try:
						exec(try_code)
					except Exception:
						print "Something went wrong while executing that code. Trying next code..."
					else:
						self.article_headline=article_headline.strip()
						self.article_alt_headline_list=article_alt_headline_list
						self.article_text=article_text.strip()
						return
				print "None of the extraction codes for %s have worked on this article. Please re-check them."%website_base_url

				


	def make_from_file(self, article_file_path): #makes the article object from an article.txt file made by write_to_file
		try:
			with open(article_file_path) as article_text_file:
				text=article_text_file.read()
				self.article_url=re.findall('(?<=__URL__:).*(?=\n)', text)[0]
				self.article_headline=re.findall('(?<=__HEADLINE__:).*(?=\n)', text)[0]
				self.article_alt_headline_list=re.findall('(?<=__ALT HEADLINE__:).*(?=\n)', text)
				self.article_text=re.findall('(?<=__ARTICLE TEXT__:)((.|\n)+)', text)[0][0]
				
		except Exception:
			print "ERROR: unable to make file from %s. Possibly no such file.\n"%article_file_path

	def write_to_file(self, folderpath):
		#filename is the article headline

		if self.article_headline=="" or self.article_text=="":
			print "ERORR: Unable to make .txt file for article."
			return False
		else: 
			article_headline=self.article_headline
			article_headline=extraction_text_manip.make_filename(article_headline)

			file_path=extraction_text_manip.make_file_path(folderpath=folderpath, filename=article_headline, extension=".txt")

			with open(file_path, "w+") as article_file:
				article_file.write("__URL__:"+self.article_url+"\n\n\n")
				article_file.write("__HEADLINE__:"+article_headline+"\n\n\n")
				for article_alt_headline in self.article_alt_headline_list:
					article_file.write("__ALT HEADLINE__:"+article_alt_headline+"\n\n\n")
				article_file.write("__ARTICLE TEXT__:")
				for line in self.article_text:
					article_file.write(line)
			return True


	def article_supersplit(self, article=None):
		if article==None:
			article=self.article_text

		article=extraction_text_manip.properly_format(article)
		'''	
		This function splits a "properly_format"ed article, 
		and returns the variable 'text'.

		'text' is structured as:
			a list of paragraphs,
				where each paragraph is a list of sentences,
					where each sentence is a list of words, punctuations as seperate words.
		'''
		text=article.split("\n") #get paragraphs
		text = extraction_text_manip.remove_empty_from_list(text)
		for i in range(0,len(text)):
			text[i]=text[i].split(". ") #get sentences
			text[i]=remove_empty_from_list(text[i])
			for j in range(0,len(text[i])):
				try:
					# print "\ntrying NLTK"
					text[i][j]=nltk.word_tokenize(text[i][j])
					# print "\nNLTK success"
				except Exception:
					# print "\n\nNLTK failed. Going for backup..."
					text[i][j]=text[i][j].split(" ") #get words
					text[i][j]+="."
					for k in range(0,len(text[i][j])):
						text[i][j][k]=re.sub(",", "", text[i][j][k])
						text[i][j][k]=re.sub(";", "", text[i][j][k])
						text[i][j][k]=re.sub("\(", "", text[i][j][k])
						text[i][j][k]=re.sub("\)", "", text[i][j][k])
						text[i][j][k]=re.sub("\[", "", text[i][j][k])
						text[i][j][k]=re.sub("\]", "", text[i][j][k])
						text[i][j][k]=re.sub("\{", "", text[i][j][k])
						text[i][j][k]=re.sub("\}", "", text[i][j][k])

					if text[i][-1][-2][-1] == ".":
						# print text[i][-1]
						text[i][-1][-2]=re.sub(".*", text[i][-1][-2][:-1], text[i][-1][-2])
					# print "\nreplaced: %s\n\n\n"%text[i][-1]
				finally:
					text[i][j]=remove_empty_from_list(text[i][j])

		return text
	








def make_article_objs_pickle(company_name):

	root_filepath="F:\Workspaces\Python\Stock Price Application\Articles/"
	base_filepath = root_filepath+company_name
	only_folders=[base_filepath+"/"+direct for direct in os.listdir(base_filepath) if os.path.isdir(base_filepath+"/"+direct)]

	all_articles=[]
	num=1
	for dir_path in only_folders:
		articles_list=os.listdir(dir_path)
		for i in range(0, len(articles_list)):
			art_file_name=articles_list[i]
			# lines = [line.rstrip('\n') for line in open(filepath+"/"+art_file_name, "r")]
			with open(dir_path+"/"+art_file_name, "r") as article_file:
				all_articles.append(article_file.read())



	article_objs=[]
	for i in range(0,len(all_articles)):
		article_objs.append(Article(all_articles[i]))
	print len(article_objs)
	with open(base_filepath+"/"+company_name+"_article_objs.pickle", 'wb') as handle:
			pickle.dump(article_objs, handle)


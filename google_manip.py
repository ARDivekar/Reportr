import random
import re
from xgoogle.search import GoogleSearch, SearchError
import time


def google_search_redirect(random_text=None): #throws Google off the scent
	
	if random_text==None:  #give some default random text
		random_text='''
		What is GIS?. Crab Snack Upgrade Linux Mint 17 to 17.1. Samsung Galaxy Sales vs iPhone Sales. Chrome Extensions Manifest Converted From Userscript. Moto G Lollipop India. Crazy Christmas Tree angels. Ideas for Office decoraton. Meet my cat he's lovely. why are Windows 8.1 Apps Not Responding Once Open?. Neville Southall. Food Bike. Marquesas AND history of surfing. What is Seeding in Torrents X14EL38. Quora how many times do i have to say naive. site:reddit.com try again not responding .stackoverflow binary search tree. stackoverflow linux. stackoverflow random function python. How to make. google summmer of code. Maple Syrup & buttered Popcorn. clock on my laptop. Motorcycle pedals on a harley. wikipedia something the beatles. core two duo is the best?. Google translate porugese. Google translate Spanish. Google translate French. Google translate geman. vallaha. price car on road mumbai. price car on road florida. price car on road los angeles. 
			site:apple.com new iphone
			site:microsoft.com windows release.
			site:google.com new savant
			GRE test scores
			site:google.com "GRE"
			site:flipkart.com "tablets"
			site:flipkart.com lenovo
			site:flipkart.com clothes men fashion
			site:nytimes.com new horizon
			site:bing.com help manual

		'''



	print "\n\n\n\t>>>Google Redirect...."
	try:
		search_query=extraction_text_manip.article_supersplit(random_text)
		search_query=search_query[random.randrange(0, len(search_query))]
		search_query=search_query[random.randrange(0, len(search_query))]
		search_query=extraction_text_manip.remove_empty_from_list(search_query)
		search_query=search_query[:random.randrange(3,4+len(search_query)%6)]
		search_query=' '.join(search_query)
	except Exception: 
		search_query=random_text[:10]
	# search_query=re.sub("\.","",search_query)
	search_query=re.sub(",","",search_query)
	search_query=re.sub("`","",search_query)
	google_search_results(search_query=search_query, number_of_results=5)



def google_search_results(search_query, wait=40, number_of_results=10, encode=True, max_fail_count=5, current_fail_count=1, random_text=None):
	''' DO NOT MESS WITH THIS IT IS PERFECT FOR NOW'''
	# gets AT LEAST number_of_results results
	# don't query too fast or Google will block your IP temporarily 
	# for this purpose, I have added the variable max_result_size
	# if your IP does get blocked, try later in the day or wait a day or two


	try:
		max_result_size=10 #don't change it from this: the standard of 10 seems the least suspicious to google
		gs = GoogleSearch(search_query, random_agent=True) # does not actually search
		gs.results_per_page = max_result_size
		
		gs.page=0
		times_tried=0
		results=[]
		prev=0
		# print "getting results:"	
		while len(results) < number_of_results:
			prev=len(results)
			times_tried+=1
			time.sleep(random.uniform(0.5*wait, 1.5*wait))
			results+=gs.get_results() # Actual search and extraction of results.
			print "\rtimes_tried: %s\tlen(results): %s\tpage_number: %s"%(times_tried, len(results), gs.page),
		print "\n"

		# We now have a list of SearchResult objects, called 'results'.
		# A SearchResult object has three attributes -- "title", "desc", and "url".
		# They are Unicode strings, so do a proper encoding before outputting them. (done below)
		if encode:
			for i in range (0, len(results)):
				results[i].title=results[i].title.encode("utf8", "ignore")
				results[i].desc=results[i].desc.encode("utf8", "ignore")
				results[i].url=results[i].url
		# random.shuffle(results)

	except SearchError, e:
		print "Google Try #%s: Search failed on this url:\t%s" %(current_fail_count,e)
		google_search_redirect(random_text)
		if current_fail_count!=max_fail_count:
			return google_search_results(search_query, wait=wait, number_of_results=wait, encode=encode, max_fail_count=max_fail_count, current_fail_count=current_fail_count+1)
	return results

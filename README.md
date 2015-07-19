# Text-Extraction
Primary contributor: Abhishek Divekar



<h2>System requirements: </h2>
  - Python (for safety, use v. 2.7 or above, though others may work)
  - External Python libraries:
      - xgoogle
      - BeautifulSoup
      - MySQLdb (also requires a MySQL instance on your computer)
      - (optional) NLTK 
  - Internal Python libraries:
    - re
    - random
      - time
      - urllib2
      - sys
      - os
      - datetime
      - pickle 
      - unicodedata (for formatting purposes)


<br>
<h2>Statement of Purpose (and the motivation behind the code):</h2>

The aim of this project was to make it easier to extract and store a large number of high-quality text articles from a list of websites - majorly online newspapers and blogs. The main idea was to create an extraction-code for each website: a 10-20 line script which could be applied to basically any webpage on the domain, to get the text of the article in that webpage. These extraction-codes are usually some mesh of Python regular expressions and HTML-parsing code (BeautifulSoup, XHTML etc). 
<br><br>
I noticed that a lot of the extraction codes for different websites looked very similar, and it was easy to build them from one another. It took me just a few hours to hack together the extraction codes for quite a few websites.
The reason is fairly obvious; articles on websites all follow the same structure: headline, sub-headline/s, body, date-time, etc. This format got me thinking if there was a better way to handle all the data that comes with an HTML page, and to abstract it into its neccessary parts. Thus the project grew to include the ArticleObject class, which stored all of the relevant features of an article and allowed them to be manipulated more fluidly with different functions. 
<br><br>
Another thing that I found tiresome during development was finding articles...after I had found a few, it was both difficult and time-consuming to find more. I found that this was particularly difficult when I didn't know what I was looking for, and I would just end up in some deep corner of a domain which had nothing to do with what I originally wanted. So, I decided to enlist everyone's favourite search engine, Google. It would find the articles I wanted, but only on the websites I had the extraction-codes for. This meant I could get the pure text, very fast (I built this when I needed a lot of data for another project).
<br>


<h2>Current Project state:</h2>
Since then, the project has grown and expanded so that now most of the process is fully automated:<br>

<h3>Step #1:</h3> the article URLs are automatically found via Google Search results.<p></p>

<ul>
<li>We restrict the search query with certain criterion:<br>

<ul>
<li>specific words eg: company names, names of persons etc.<br></li>
<li>specific range of dates <br></li>
<li>only over websites of your choice <br></li>
</ul></li>
<li>Doing such a specialized search ensures that the articles are of a higher quality. <br></li>
<li>Note: This step is deliberately a slower than the others (taking around 3 mins per page of results). This is because Google tends to notice if you spam it with hundreds of search queries in a short period of time, and temporarily blocks your IP. <br>To counter this as much as possible, the project code includes a redirect function: every few searches, it Google Searches something totally unrelated. This means that your IP does not get restricted too fast, allowing the code to get more results before you need to wait and run the script again. <br></li>
</ul>

<p><br>
<br></p>

<h3>Step #2:</h3>the text of the articles are extracted from the URLs, provided you have included the extraction-code for those domains.<br>
<ul>
<li> This step is almost instantaneous with a fair internet connection:<br>
  <ul><li> a 2MBps connection takes about 5 seconds per extraction.</li></ul></li>
<li> It is unfortuantely not possible to build a single extraction-code for all website, as the HTML formatting used varies from site to site (and even time to time). <br>
  <ul><li> However, with the few examples of extraction-codes provided, it is easy to extract the most relevant features: the headline, the sub-headlines and the body of the article.</li>
  <li> The basic template can then be tweaked to work for other websites and updates to existing websites.</li> 
  <li> Inside the file "regex_builder_helper.py", there is an example template of how I went about building the extraction codes.</li></ul>
<li> The extraction-codes have been made as reusable as possible, with the old extraction codes being saved in a MySQL table. When extracting text from a particular domain, the most recently updated code is tried first, and if that doesn't work, it falls back to the older extraction-codes, with the hope that they will work.<br></li> 
</ul>
<p><br>
<br></p>
  
<h3>Step #3:</h3> Assuming the text has been extracted (from the URL and into an ArticleObject), the relevant features of the article (headline, sub-headline, body and URL) are written to a file, in a directory of your choosing. <br>
<ul>
  <li> The filenames are automatically truncated to fit within the host OS's path size.<br></li>
  <li> The salient feature of this design step is that, we obtain Google results by 30-day periods (one 'month'), and thus, all articles in that month go into a single directory. We thus organize our database by months. Each month contains a specified number of articles. Note: the "month"s do NOT start on the 1st and go till the 30th/31st. They are just 30-day blocks, used for organization.<br></li>
  <li> On subsequent runs of the script (which might be necessary due to the Google IP problem), we thus do not need to start from the beginning, but can start from a later month if we are satisfied with the articles obtained proviously. <br></li>
  <li> In this structure, you can also expand the number of articles we get each month. The code supports this: it does not re-extract articles which aleady exist in our database (it looks at the URL part of the files which are already saved).<br></li>
  <li> This step becomes more clear if you look inside the "test_example" folder, whose contents are all generated automatically by running the script.<br></li>
  </ul>
<br>
<br>

<h2>Conclusion:</h2>
The end effect of all this is that, we can quickly and painlessly build a large, high quality database of articles, just by specifying the following:<br><ul>
  <li> The search query topic (eg. "Reliance Industries").</li>
  <li> How many months of articles do you want (from a specified starting point or from the present day).</li>
  <li> How many articles do you want to get per month.</li>
  <li> Which websites do you want to get these articles from (the extraction-code must already exist).</li><br>
  
<h3>A test example of a complete script is already present: just execute <i>test_code.py</i></h3>
    



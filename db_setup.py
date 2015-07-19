import MySQLdb
import simpleMySQL
import datetime

dbname='article_extraction_db'


def get_conn():
	conn = MySQLdb.connect(	host="localhost", # your host, usually localhost
	                    		user="root", # your username
	                      	passwd="", # your password
	                      	db="%s"%dbname) # name of the database
	if(conn):
		print '\n\n\t\tSuccessfully connected\n\n'
	else: 
		print '\n\n\t\tERROR: Unable to establish SQL connection.\n\n'
	return conn




def init_db():
	conn = MySQLdb.connect(user="root", # your username
	                      	passwd="") # your password
	if(conn):
		cur=conn.cursor()
		cur.execute('''Select SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '%s' '''%dbname)
		if cur.fetchone()==None:
			cur.execute('Create database %s;'%dbname)
		cur.execute('use %s;'%dbname)

		# cur.execute('Drop table if exists website_regex;')
		cur.execute('''SHOW TABLES LIKE 'website_regex' ''');
		if cur.fetchone()==None:
			cur.execute('''	Create table if not exists website_regex(
								base_url varchar(200) NOT NULL,
								exec_code text NOT NULL,
								date_of_addition date NOT NULL,
								primary key(base_url, date_of_addition)
							);''')
		return get_conn()






def website_regex_insert(conn, website_code_dict):
	now=datetime.datetime.now()
	tuple_values_list=[]
	for i in website_code_dict:
		tuple_values_list.append((i,website_code_dict[i], '%s-%s-%s'%(now.year, now.month, now.day)))
	print tuple_values_list

	simpleMySQL.push_update(conn=conn, tablename="website_regex", parameters_list=["base_url", "exec_code", "date_of_addition"], tuple_values_list=tuple_values_list)












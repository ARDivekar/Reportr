import MySQLdb

def database_in_use(conn):
	cursor=conn.cursor()
	cursor.execute("select database()")
	print "\n\n\t\tDatabase in use: "+cursor.fetchone()[0]+""

class Table:
	def __init__ (self, input_attributes, input_table):
		self.table=input_table
		self.attributes=input_attributes

	def __len__(self):
		return len(self.table)
	def __getitem__(self,i): 
		'''
			works for 2D or 3D or any-D yay!
			works because if a[i][j][k], a[i] returns a tuple, for the ith row. Let, row=a[i]. 
			Then, a[i][j][k] becomes row[j][k]. We start call the function again, to get the column entry.

		'''
		# print type(self)
		if type(i)==int:
			return self.table[i]
		elif type(i)==str:
			#assume that they are searching by column, i.e.
			#table['col_name']
			#this allows access by column and then row
			ind=self.attributes.index(i)
			col=[]
			for row_no in range(0, len(self.table)-1):
				col.append(self.table[row_no][ind])
			return tuple(col)




def verified_select(conn, select_query, fetch="all", printing=True):
	'''This function verifies that the entered query is a valid select query (to prevent SQL injection). 
	If it is, it executes it and gets the table object. It  returns None if the table is Empty, and prints an ERROR.
	If the table is non-empty, it returns the table object.'''
	if 'select' in select_query.lower():
		temp = select_query.strip()
		if not ';' in temp:
			temp+=';'
		# print temp
		if temp.index(';') == (len(temp)-1):
			cursor=conn.cursor()
			cursor.execute(temp)
			attributes=[]
			for i in cursor.description:
				attributes.append(i[0])
			result_table=()
			if fetch.lower()=="all":
				result_table=cursor.fetchall()
			elif fetch.lower()=="one":
				result_table=cursor.fetchone()
			else:
				if printing: print "verified_select() ERROR: Improper value '%s' passed to argument 'fetch'"%fetch
				return None 

			if result_table is ():
				if printing: print 'verified_select() ERROR: Empty table'
				return None
			return Table(input_table=result_table, input_attributes=attributes)
			
		else:
			if printing: print 'verified_select() ERROR: Only one query can be fired at a time'
	else:
		if printing: print 'verified_select() ERROR: Only select queries can be executed'

def build_where_clause(where_params_list, where_values_list):
	if where_params_list!=None and where_values_list!=None:
		where_clause=" WHERE "
		where_clause+=" %s='%s' "%(str(where_params_list[0]), str(where_values_list[0]))
		for i in range(1,len(where_values_list)):
			where_clause+=" AND %s='%s' "%(str(where_params_list[i]), str(where_values_list[i]))
	else : 
		where_clause=""
	return where_clause



def build_select_query(tablename, select_params_list, where_params_list=None, where_values_list=None):
	select_query="SELECT "
	select_query+=" %s"%select_params_list[0]
	for i in range(1,len(select_params_list)):
		select_query+=", %s"%select_params_list[i]
	select_query+=" FROM %s "%tablename
	select_query+=build_where_clause(where_params_list=where_params_list, where_values_list=where_values_list)
	select_query+=";"
	return select_query


def build_update_query(tablename, update_params_list, update_values_list, where_params_list=None, where_values_list=None):
	update_query="UPDATE "+tablename+" SET " 
	update_query+=" %s='%s' "%(str(update_params_list[0]), str(update_values_list[0]))
	for i in range(1,len(update_values_list)):
		update_query+=", %s='%s' "%(str(update_params_list[i]), str(update_values_list[i]))	
	update_query+=build_where_clause(where_params_list=where_params_list, where_values_list=where_values_list)
	update_query+=";"		
	return update_query


def build_insert_query(tablename, insert_params_list, tuple_values_list):
	insert_query="INSERT INTO %s(" %tablename+"%s"%insert_params_list[0]
	# print insert_query
	
	for param in insert_params_list:
		if  insert_params_list[0]!= param:
			insert_query+=", %s"%param
	insert_query+=") VALUES "
	#print insert_query
	
	insert_query+="\n('%s'"%tuple_values_list[0][0]
	for j in range(1,len(tuple_values_list[0])):
		insert_query+=" ,'%s'"%tuple_values_list[0][j]
	insert_query+=")"


	for i in range(1,len(tuple_values_list)):
		insert_query+=",\n('%s'"%tuple_values_list[i][0]
		for j in range(1,len(tuple_values_list[i])):
			insert_query+=" ,'%s'"%tuple_values_list[i][j]
	insert_query+=";"
	# print insert_query
	return insert_query



def insert_table_mysql(tablename, insert_params_list, tuple_values_list, conn,commit=True ):
	
	insert_query= build_insert_query(tablename=tablename, insert_params_list=insert_params_list, tuple_values_list=tuple_values_list)
	# print insert_query
	cursor=conn.cursor()
	cursor.execute(insert_query)
	if commit:
		conn.commit()
	# database_in_use(conn)
	return

def print_table(conn, select_query):
	table = verified_select(conn, select_query)
	if table is not None:
		for row in table:
			print '\n\n\n'
			for i in range(0,len(row)):
				print row[i]




def push_update(conn, tablename, update_params_list, update_values_list, where_params_list=None, where_values_list=None, commit=True): 
	# can only hanndle one update at a time

	if len(update_params_list)!=len(update_values_list):
		print "ERROR: invalid input to push_update()"
		return 

	'''this function inserts data into a table if it does not exist.
	However, if an entry with the same primary key does exist, 
	it only updates certain fields, on the condition that other fields remain the same.
	This is useful to push updates to a database without adding unnecessary entries.
		Eg: I want to update the price of a product. If I keep checking multiple times but the price 
		does not change, I don't really want to save all the times the price remains same. It is more
		space-efficient if I just store the time the price was different, and the price when I last
		updated it. It's obvious that in between those two, it was the same price. '''

	push_select_query=build_select_query(tablename=tablename, select_params_list=update_params_list, where_params_list=where_params_list, where_values_list=where_values_list)

	if verified_select(conn=conn, select_query=push_select_query, printing=False) == None:
		#the item does not exist, so we must now insert
		#we have two cases: one with the where clause, and one without

		if where_params_list==None and where_values_list==None:
			#there is no 'where' clause in the update, thus we only insert parameters of the 'set' clause
			insert_table_mysql(tablename=tablename, insert_params_list=update_params_list, tuple_values_list=[tuple(update_values_list)], conn=conn, commit=commit)

		elif where_params_list!=None and where_values_list!=None:
			# There is a 'where' clause in the update, thus we insert parameters of both the 'set' clause and where clause.
			# We do so by combining them. 
			'''
			eg: We have accidentally entered the wrong age of a person:
			UPDATE Person SET Age='19', DOB='1995-12-01' WHERE Name='John Smith' AND Age='190';
				>>becomes:
			push_update(conn, 'Person', update_params_list=['Age', 'DOB'], update_values_list=['19', '1995-12-01'],
				where_params_list=['Name', 'Age'], where_values_list=['John Smith', '190'])
				>>now,
				>>if we do not find the entry in the table, we must insert it
				>>and so, we do: 
			INSERT into Person ('Age', 'DOB', 'Name') VALUES ('19', '1995-12-01', 'John Smith');
			'''
			# as we see in the example above, we have the problem of overlapping parameters: 'Age' is seen in both 
			# update_params_list and where_params_list. We only want to retain the one which corresponds to the update_values_list 
			# value. To do so, we use a dictionary, which, in case of overlap, only stores the update_values_list values.
			params_values_dict={}
			# print where_params_list
			# print update_params_list
			for  i in range(0,len(where_params_list)): 
				params_values_dict[where_params_list[i]]=where_values_list[i]
			for i in range(0,len(update_params_list)):  #overwrites overlapping values
				params_values_dict[update_params_list[i]]=update_values_list[i]
			
			
			push_insert_params_list=[]
			push_tuple_values_list=[]
			for param in params_values_dict:
				push_insert_params_list.append(param)
				push_tuple_values_list.append(params_values_dict[param])
			

			insert_table_mysql(tablename=tablename, insert_params_list=push_insert_params_list, tuple_values_list=[tuple(push_tuple_values_list)], conn=conn, commit=commit)



	else:
		
		# the item exists, so we just have to update it.
		update_query=build_update_query(tablename=tablename, update_params_list=update_params_list, update_values_list=update_values_list, where_params_list=where_params_list, where_values_list=where_values_list)
		cursor=conn.cursor()
		cursor.execute(update_query)
	if commit:
		conn.commit()


'''
#eg of usage of push_update():

create_table_query="Create table if not exists test_table(
	ID int PRIMARY KEY,
	Name varchar(100) NOT NULL,
	DOB Date,
	Age int(3),
	Salary int
);"
cur=conn.cursor()
cur.execute(create_table_query)


tablename='test_table'

# operation 1:
update_params_list=['Age', 'Salary']
update_values_list=['96', '2900']
where_params_list=['ID', 'Name','DOB']
where_values_list=['75', 'Kalifa','1995-06-09']
simpleMySQL.push_update(conn=conn, tablename=tablename, update_params_list=update_params_list, update_values_list=update_values_list, where_params_list=where_params_list, where_values_list=where_values_list)

"""
Output: 
+----+--------+------------+------+--------+
| ID | Name   | DOB        | Age  | Salary |
+----+--------+------------+------+--------+
| 75 | Kalifa | 1995-06-09 | 96   | 2900   |
+----+--------+------------+------+--------+
"""

# operation 2:
update_params_list=['Age', 'Salary']
update_values_list=['96', '1000']
where_params_list=['ID', 'Name','DOB']
where_values_list=['123', 'Aquila','1994-05-10']

"""
Output: 
+-----+--------+------------+------+--------+
| ID  | Name   | DOB        | Age  | Salary |
+-----+--------+------------+------+--------+
| 123 | Aquila | 1994-05-10 | 96   | 1000   |
| 75  | Kalifa | 1995-06-09 | 96   | 2900   |
+-----+--------+------------+------+--------+
"""


# operation 3:
update_params_list=['Age', 'Salary']
update_values_list=['19', '1000']
where_params_list=['ID', 'Name','DOB']
where_values_list=['123', 'Aquila','1994-05-10']

"""
Output: 
+-----+--------+------------+------+--------+
| ID  | Name   | DOB        | Age  | Salary |
+-----+--------+------------+------+--------+
| 123 | Aquila | 1994-05-10 | 19   | 1000   |
| 75  | Kalifa | 1995-06-09 | 96   | 2900   |
+-----+--------+------------+------+--------+
"""


'''
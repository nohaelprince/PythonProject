#!/usr/bin/python
import fileinput
import csv
import os
import sys
# load the adapter
import psycopg2
# load the psycopg extras module
import psycopg2.extras

from collections import defaultdict

lst = defaultdict(list)
d_lst = defaultdict(list)
domainPR_lst = defaultdict(list)

# ======================== Defined Functions ======================
def get_file_path(filename):
    currentdirpath = os.getcwd()  
    # get current working directory path
    filepath = os.path.join(currentdirpath, filename)
    return filepath
# ===========================================================
def read_CSV(filepath):
    
   domain_list = []
   domain_date_list = []
   sorted_domain_list_bydate = defaultdict(list)
      
   with open(filepath, 'rb') as csvfile:
       reader = csv.reader(csvfile)
       
       for row in reader:
          # insert the 1st & 2nd column of the CSV file into a set called input_list
           email = row[0].strip().lower()
           date  = row[1].strip()
           #print type(email) #type 'str'
           #email_list.append([date, email])
           
           domain_date_list.append([date, email[ email.find("@") : ]])
           domain_list.append(email[ email.find("@") : ])
           
   for k, v in domain_date_list: 
         sorted_domain_list_bydate[k].append(v)
               
           
   # remove duplicates from domain list
   domain_list = list(set(domain_list))
   
   return sorted_domain_list_bydate, domain_list
# ===========================================================
def update_DB(lst):
    
    # open a database connection
    try:
        conn = psycopg2.connect("dbname='db1' host='localhost'")
    except:
        print "I am unable to connect to the database"
    
    cur = conn.cursor()
    
    # Add counter to the lst's values (i.e add counter for domains per day)
    from collections import Counter # needs python 2.7 or 3.0 (scalable)
    a = []
    for k, v in lst.items():
        a = v # store the values of the ith element of lst in a
        x = Counter(a) # add Counter and store in x (hashable list)
        for k1, v1 in x.iteritems():
           query = "INSERT INTO domains(domain_name, cnt, date_of_entry) VALUES (%s, %s, %s);"
           data  = (k1, v1, k)
           cur.execute(query, data)
           
    conn.commit()
    conn.close()
# ==========================================================
def calc_PR(lst, d_lst):
    
 # Objective: Create a dictionary list called domainPR_lst to store the domain and its rate of it's percentage growth for the recent 30 days compared to the total:  <key, value> = <domain_name, PR_30/PR_total>
    domainPR_lst = {}
    
    
  # Calc last 30 days from current date (call it target_date)
    from datetime import date, timedelta
    days_to_subtract = 30
    target_date = date.today() - timedelta(days=days_to_subtract)
    
  # open a database connection
    try:
        conn = psycopg2.connect("dbname='db1' host='localhost'")
    except:
        print "I am unable to connect to the database"
        
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # iterate over domain list (d_lst)
    for dom_name in d_lst:
        # print "dom_name = ", dom_name
        # initialize variables
        v_present=0.0
        v_past30=0.0
        v_past=0.0
        PR30 = 0.0     # perecntage of growth rate for recent 30 days
        PR_total = 0.0 # perecntage of total growth rate
        
       # query1: counts the no. of users for each domain within the recent 30 days  (call it v_past30).
        query1 = "SELECT COALESCE(cnt,0) FROM domains WHERE date_of_entry = %s AND domain_name = %s;"
        data1 = (target_date, dom_name)
        cur.execute(query1, data1)
        rows_query1 = cur.fetchall()  # access the database rows
        for row in rows_query1:
             #print "%s %s" % (row["domain_name"], row["cnt"])
             v_past30 = row[0]  
        
        # print "v_past30 = ", v_past30
        
        # query2: counts the no. of users for each domain that occured today (call it v_present).
        query2 = "SELECT COALESCE(cnt, 0) FROM domains WHERE date_of_entry = %s AND domain_name = %s;"
        data2 = (date.today(), dom_name)
        cur.execute(query2, data2)
        rows_query2 = cur.fetchall()  # access the database rows
        for row in rows_query2:
            #print "%s %s" % (row["domain_name"], row["cnt"])
            v_present = row[0]  
    
        # print "v_present = ", v_present
        
        # calculate perecntage of growth rate for recent 30 days (called PR30) 
        # if condition to avoid division by zero
        if v_past30 == 0: 
            PR30 = -999999 # stands for undefined
        else : 
            # use float to enforce float calculations
            PR30 = ((v_present - v_past30)/ float(v_past30)) * 100 
    
        # print "PR30 = ", PR30
        
        #cur1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # query3: counts the no. of users for each domain that occured in the earliest date (call it v_past).
        query3 = "SELECT COALESCE(cnt,0) from domains where domain_name = %s and date_of_entry=(select min(date_of_entry) from domains where domain_name=%s);"
        data3 = (dom_name, dom_name)
        cur.execute(query3, data3)
        rows_query3 = cur.fetchall()  # access the database rows
        for row in rows_query3:
            #print "%s %s" % (row["domain_name"], row["cnt"])
            v_past = row[0]
        
        # print "v_past = ", v_past
        
        # Calculate perecntage of total growth rate for (called PR_total) 
        # if condition to avoid division by zero
        if v_past == 0: 
            PR_total = -999999 # stands for undefined
        else:
            # use float to enforce float calculations
            PR_total = ((v_present - v_past)/ float(v_past) ) * 100.0 
            
        # print "PR_total = ", PR_total
        
        # fill the list: domainPR_lst
        if (PR30 == -999999) or (PR_total == -999999): # undefined
             domainPR_lst[dom_name] = -999999
        elif (PR_total==0):
             domainPR_lst[dom_name] = -999999
        else:
             domainPR_lst[dom_name] = PR30/PR_total
    
        # print "PR_total/PR_total = ", domainPR_lst[dom_name]
        
    conn.close()
    
    # sort the list descendingly
    domainPR_lst = [(k, domainPR_lst[k]) for k in sorted(domainPR_lst, key=domainPR_lst.get, reverse=True)]
    
    return domainPR_lst
# ============================================================================
def printReport(domainPR_lst):
    
    # writing a CSV file : max. 50 domains
    max = 50
    count = 1
    try:
      with open('data1/Final_Report.csv', 'w') as f1:
          writer = csv.writer(f1)    
          
          for v in domainPR_lst:
               writer.writerow(v)
               count +=1
               if (count > max): break
               
        
          print "==========================================================="
          print "Report is succeffuly written in file: data1/Final_Report.csv"
          print "HAVE A GOOD DAY!"
          print "==========================================================="
     
    except IOError as e:
         print "Unable to open file" # no read permissions 
# ======================= main program =======================================
path = get_file_path('data1/emails.csv') 
[lst, d_lst] = read_CSV(path) # read the input file
#print "d_lst = ", d_lst
update_DB(lst) # insert data into domains table
# calculate % of growth (PR) for each domain and stores it in a dictionary list
domainPR_lst={}
domainPR_lst = calc_PR(lst, d_lst) 
printReport(domainPR_lst)
# ========================= END program =====================================
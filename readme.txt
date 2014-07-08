This Program is written by Noha Elprince using python 2.7.6 and database postgres 9.3.4

Objective:
===========
Given a table 'mailing':

CREATE TABLE mailing (
	addr VARCHAR(255) NOT NULL
);

The mailing table will initially be empty.  New addresses will be added on a daily basis.  It is expected that the table will store at least 10,000,000 email addresses and 100,000 domains.

Write a python script that updates another table which holds a daily count of email addresses by their domain name.

This table will be used to report the top 50 domains by count sorted by percentage growth of the last 30 days compared to the total.




Notes :
======

1. Inorder to run the program, go to a terminal and write:  ./run.sh
2. The main program is found in file called (main.py)
3. The input (emails.csv) and the output (Final_Report.csv) are found in 3 folders : data1, data2 and data3.
   Each folder corresponds different test.
4. There is an Excell sheet called (dataAnalysis_.xls) in each folder : data1, data2 and data3.
   This file contains step by step the calculations and the formula and was used by the programmer for verification.
5. The database schema is found in file (schema.sql)

   
     

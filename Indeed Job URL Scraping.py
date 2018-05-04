# -*- coding: utf-8 -*-
"""
Created on Fri May  4 10:11:46 2018
Automation that extracts relevant URL's for job application. Replaces RSS Feed.
Created by Umang Shah

Pending to fix Line 96

@author: alexgu
"""

from bs4 import BeautifulSoup
import urllib.request as ur
import re
import sys


red_flags = ["intern","Chief Financial Officer","CFO"] #List of words to avoid in job title
#required = ["software"] #Can also check for required words

#====================================================
def qualifies(title):
    title = title.lower()
    #Define a function to check if a job title is worth checking out  
    for word in red_flags:
        if word in title: return False
    return True

#====================================================

# Now define the Regex, 
# 1. Should not have the phrase 1+ years, 1-2 Years, so on..
p1 = re.compile('[2-9]\s*\+?-?\s*[1-9]?\s*[yY]e?a?[rR][Ss]?')


# 2. Should not have mention of "Citizenship", "Citizens", so on..
p2 = re.compile('[Cc]itizens?(ship)?')

t1 = p1.search("2+ Years of experiencce")
t2 = p1.search("0-1 Year")
print (t1, "\n",t2)



#The first page with search results#The fir 
url_base = "https://www.indeed.com/jobs?q=Chief+Technology+Officer&l=Los+Angeles%2C+CA"

pgno = 0
try:
        response = ur.urlopen(url_base+"&start="+str(pgno))
        print('RESPONSE_1', url_base+"&start="+str(pgno))
        html_doc = response.read()
        
        
except:
        print("URL not accesible")
        exit();
soup = BeautifulSoup(html_doc, 'html.parser')


#====================================   
try:
    total_results = soup.find(id="searchCount").get_text()
    last_page = int(int(total_results[total_results.index("of")+2: total_results.index("jobs")].strip()) / 10) * 10
    
except:
    print ("No jobs found")
    


#====================================    
jobs_per_page = 10
goodlinks = []
for pgno in range(0,last_page,jobs_per_page):
    print("RESULT PAGE>>", pgno)
    if pgno > 0:
        try:
            response = ur.urlopen(url_base+"&start="+str(pgno))
            print('RESPONS_2', url_base+"&start="+str(pgno))
            html_doc = response.read()
            
           
        except:
            break;
        soup = BeautifulSoup(html_doc, 'html.parser')
    for job in soup.find_all(class_='result'):
        link = job.find(class_="turnstileLink")
        try:
            jt = link.get('title')
        except:
            jt = ""
        try:
            comp = job.find(class_='company').get_text().strip()
        except:
            comp = ""

        if(qualifies(jt.lower())):
            #toVisit = "http://www.indeed.com"+link.get('href')
            try:
                html_doc = ur.urlopen(toVisit).read().decode('utf-8')
            except:
                continue;
            #print(jt,",",comp,":",toVisit,"\n")   *** original con URL
            print(jt,",",comp,":","\n")   # Sin URL
            """m = p1.search(html_doc)
            n = p2.search(html_doc)
            if not m and not n:
                print(jt,",",comp,":",toVisit,"\n")
                goodlinks.append(toVisit)"""
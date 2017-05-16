Hello!
The directory structure is as follows
Gold (Folder)
Test (Folder)
scraper.py
url.txt

scraper.py will scrape and extract the text out of the html parsed data.
it takes a file that contains URLs as input
url.txt is that file. 


scraper.py outputs two folders Gold and Test
Each file in Gold corresponds to the UID of that Debate topic.
a UID is basically the last number of the URL
Example:
http://idebate.org/print/17645 
Here, 17645 is the UID of the Debate topic contained in this URL. 


Each Gold file contains metadata about which point corresponds to a counterpoint
Each test file contains the actual point and counterpoint in it for each topic.

The current sample size contains 100 debate topics and point and counterpoints of those.

NOTE: The debate topics have in total 4 permutations
There are points and counterpoints for 'FOR' the topic
There are points and counterpoints for 'AGAINST' the topic

In this sample set we have only chosen 'FOR' and not 'AGAINST' because a point in FOR does not exactly correspond as a counterargument of a point in 'AGAINST'
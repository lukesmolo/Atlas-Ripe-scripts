# Atlas-Ripe-scripts
Some useful scripts for querying Atlas Ripe infrastructure

Here there are some scripts useful for making automatically big numbers of queries to Atlas Ripe infrastructure.
You need to be an host in the Atlas Ripe infrastructure in order to obtain the keys for making queries.

dns_measurements.py: A python script for making dns queries
traceroute_measurements.py: A python script for making traceroute queries
download_measurements.py: A python script for downloading measurements previously made.

In each script you need to add your key!

In order to perform queries using the scripts for measurements, you need to have the list of all probes 
you want to use and their information about their continent, their country code, and their country iso code.
You can find an example in query_probes.json.
You also need to create a directory called requests_done, where scripts will save logs of queries made.
The directory sites already contains all the most visited sites for each country. Queries will use them as target.

Once you have all, scripts for measurements can start.
They will automatically make all the queries, handling http errors and some Atlas Ripe errors.
(see https://atlas.ripe.net/docs/measurement-creation-api/ for more information about Atlas Ripe errors)
By default, scripts will query the 100 most visited domains for each country. You can change this value in the script.
In case of interruption, you can restore the script specifying the last code of the country used and the next domain to query, respectively as first and second parameter of the script.

In order to download all the results obtained from queries, you can launch the script download_measurements. You just need to put into the same directory the log file containing all the numbers of queries made (it can be automatically made by one of the scripts above).
It automatically collects results in different directories, according to the name of the country. A different file will be created for each query made previously, with name the description of the query.
In case of interruption, you can restore the script specifying the last number of result downloaded as first parameter of the script.

# jordan_kail_crypto_project 
Hey! Thanks for chekcing out my github jordan_kail_crypto_project  repo!

Lots of fun examples of using Pandas and BOTO3 to call web apis and generate good usable data. 

This is just a fun side project to better understand crypto currency and its correlations to other data sources such as social mentions, prices of rare materials in foreign countries, or even us stock prices. 

This is just a sample of my skill set on a off hours passion project. I haven't yet created a real how to doc or workflow but thats coming soon. 

All that is needed at this time is to download awscli to your local and running aws_config. Then running the balpha_runner.sh file under alpha, this should launch the runner with hourly params. 

If you'd like to setup cron jobs and deploy on ec2 its fully compatible to run hourly or even minute runner due to the fact most of the python is multithreaded.

Alpha:
Data Ingestion aquistion and storage

Omega:
Automation of reporting/ machine learning components to detect trends amongst data sets. 
Unfortunately I haven't had enough time in the past few months to work on this component as much as I hoped and cut out all of the "half baked" step wise regression and k means clustering python it had been working but I didn't have the time to correct some noise in the data models. So to save you the hassle of working with crappy models I took it out. If you would like these anyways please feel free to hit me up via my contact information below. 

I recommend using dbt to manage data models if you decide to warehouse the data sadly it does not currently support Athena. Luckily AWS glue does a great job of categorizing data in combination with using the "data models " directory attached to this repo and just saving as standard sql Queries. 

PLEASE NOTE: 
Do what ever with my code, its public on github for a reason.

ALSO! There are a few keys from API's hard coded in some of they python scripts, this is a bad practice and laziness 

REQUIREMENTS: 
BUGS:
VERSION 1.0 
Dependencies: 


-- Example Workflow --
Configure AWS (Check Connection)
Run Setup (check for and/or create directories)
Call API to mine data 
Store data on local 
Transform to JSON and Zip 
Save to S3
Run Glue Crawler

Run Query via athena / Visualize data via Tableau(athena driver) / Athena Query --> Pandas data frame --> Scikit learn ML 


-Jordan Kail
jckail13@gmail.com
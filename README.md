# loyce.club addresses dumper 

File `import.py` dumps http://alladdresses.loyce.club/ daily updates
(and a sample script to manually import the old dump), add it to cron and have fun.

File `manual_import.py` accepts a `file` parameter for you to download and extract the file before executing the script.

File `import.log` is set at `20230724` in the repo as a mock value, to allow all (at time of writing) files to be downloaded and imported from the "repo".




Change YOUR_USERNAME and YOUR_PASSWORD in `.py` and `.sql` file you're using and godspeed.

The tables were created in a separate tablespace, as I've dedicated a disk to this dataset, it's not a requirement, feel free to remove it from the `.sql` file.

Dependencies are installable with `python3 -m pip install lxml psycopg2 requests`.
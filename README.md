# CommandStrip

![Banner](Banner.png)

CommandStrip is an elegant command line solution for accessing CommitStrip comics. You can download as well as search for your favourite CommitStrip comics using this tool.


## Installation:
```
git clone https://github.com/Aniruddha-Deb/CommandStrip.git && cd CommandStrip
chmod +x CommandStrip.py
./CommandStrip.py download -n [NUMBER]
```

for the full usage manual, see usage.

## Usage:
```
Usage: 
  ./CommandStrip.py {download|search}
  ./CommandStrip.py download [-h] [-d DIRECTORY] [-g SLUG] [-i ID] [-n NUMBER]
  ./CommandStrip.py search [-h] [q QUERY]

optional arguments: 
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory in which to store comics
  -g SLUG, --slug SLUG  Comic slug (to download a particular comic)
  -i ID, --id ID        Comic ID (to download a particular comic)
  -n NUMBER, --number NUMBER
                        Number of comics to download (latest first)
  q QUERY, --query QUERY
                        Search query
```

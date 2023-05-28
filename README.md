# Youtube Music Mass Artist/Album Importer

This quick script I made that takes a CSV file with the artist in the first column and album in the second column and then adds the artist and album to your Library in YouTube Music.

## Usage

Follow these steps to set up authentication to your YTMusic account:

Download the repo to a folder anywhere on your computer and open the directory in terminal/cmd.

To install ytmusicapi to set up authentication, run:
```
pip install ytmusicapi
```

After you have installed ytmusicapi, simply run
```
ytmusicapi oauth
```
and follow the instructions. This will create a file oauth.json in the current directory.

After this add your csv named "music.csv" in the same format as the "music.csv.template"

Run these command to start the run:
```
python yt_music_import.py
```
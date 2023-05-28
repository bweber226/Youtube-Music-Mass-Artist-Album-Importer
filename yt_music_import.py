import csv
import re

from ytmusicapi import YTMusic

ytmusic = YTMusic("oauth.json")

def remove_punctuation(punctuation_string: str) -> str:
    """
    Removes the punctiation and other non alphanumeric characters from a string
    """
    return re.sub(r'\W+', '', punctuation_string)


with open("music.csv", encoding="utf8") as csvfile:
    music_csv = csv.reader(csvfile)
    artist = ""
    for row in music_csv:
        # If the artist from the new line is different than the last line get the new info
        if artist != row[0]:
            artist = row[0]
            added_artist = False
            yt_search = ytmusic.search(artist, filter="artists")
            if yt_search != []:
                yt_artist = ytmusic.get_artist(yt_search[0]["browseId"])
        if yt_search != []:
            album = row[1]
            added_album = False
            if yt_artist.get("albums"):
                yt_artist_albums = yt_artist["albums"]["results"]
                if yt_artist["albums"].get("params"):
                    yt_artist_albums = ytmusic.get_artist_albums(
                        yt_artist["channelId"], yt_artist["albums"]["params"]
                    )
            else:
                yt_artist_albums = []

            # Add the artist if it hasn't been added
            if not added_artist:
                try:
                    ytmusic.subscribe_artists([yt_artist["channelId"]])
                    print(f"Added {artist}.")
                    added_artist = True
                except:
                    print(
                        f"ERROR: There was an error adding {artist}. "
                        "Most commonly a group linking to a single person."
                    )

            # Add the album if the album from this row of the CSV hasn't been added
            for yt_artist_album in yt_artist_albums:
                if (
                    str.capitalize(yt_artist_album["title"]) == str.capitalize(album)
                    and not added_album
                ):
                    if yt_artist_album.get("playlistId"):
                        yt_album_ID = yt_artist_album["playlistId"]
                    else:
                        yt_album_ID = ytmusic.get_album(yt_artist_album["browseId"])[
                            "audioPlaylistId"
                        ]
                    ytmusic.rate_playlist(yt_album_ID, "LIKE")
                    print(f"Added {yt_artist_album['title']} by {artist}.")
                    added_album = True

            # Print that the album or artist was not able to be found before going to next row
            if not added_artist:
                print(f"ERROR: {artist} was not able to be added.")
            if not added_album:
                # Try again but if the album title is in the YT album title instead of equals
                # This will catch stuff like deluxe and anniversary editions
                for yt_artist_album in yt_artist_albums:
                    if (
                        remove_punctuation(str.capitalize(album))
                        in remove_punctuation(str.capitalize(yt_artist_album["title"]))
                        and not added_album
                    ):
                        if yt_artist_album.get("playlistId"):
                            yt_album_ID = yt_artist_album["playlistId"]
                        else:
                            yt_album_ID = ytmusic.get_album(
                                yt_artist_album["browseId"]
                            )["audioPlaylistId"]
                        ytmusic.rate_playlist(yt_album_ID, "LIKE")
                        print(f"Added {yt_artist_album['title']} by {artist}.")
                        added_album = True
            if not added_album:
                print(f"ERROR: {album} by {artist} was not able to be added.")

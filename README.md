# fantasyfootball
Handy script to make creating ESPN fantasy league notes a breeze. This script
handles:

1. Uploading images stored in a folder on disk to a public location
   (www.imgur.com)
1. Generating an ESPN fantasy football league note template, complete with
   formatting and referencing newly-uploaded images

> NOTE: The generated template will output image links based on the ordering of
> the filename, so be sure your images are stored with an appropriate name.

## Requirements

* [Python 3+](https://www.python.org/downloads/)
* [Requests](http://docs.python-requests.org/en/master/) - HTTP for Humans
* [Imgur OAuth 2.0](https://apidocs.imgur.com/#authorization-and-oauth)
  * Script requires an Imgur `client_id`, `client_secret`, and `refresh_token`
  * [Registration](https://api.imgur.com/oauth2/addclient) gives you your
   `client_id` and `client_secret`
  * [Authorization](https://apidocs.imgur.com/#authorization) gives you your
   `refresh_token`

#### Installing on OSX
* [Homebrew](https://brew.sh/)
```bash
brew update && brew install python3
pip3 install requests 
```

## Running the Script

`uploadffpics.py` takes 4 required, positional arguments, along with an
optional description.

```bash
python3 uploadffpics.py --help
usage: uploadffpics.py [-h] [--description DESCRIPTION]
                       client_id client_secret refresh_token upload_folder

Facilitates image upload and formatting for league notes

positional arguments:
  client_id             The Client Id to use for Imgur's API calls
  client_secret         The Client Secret to use for Imgur's API calls
  refresh_token         The refresh token to use for Imgur's API calls
  upload_folder         The path to the folder containing images to upload

optional arguments:
  -h, --help            show this help message and exit
  --description DESCRIPTION
                        Optional description for the album/template
```

#### Example Execution

Below is an example of how to run the script, along with an idea of the output
to expect.

```bash
client_id=55b............
client_secret=e69.....................................
refresh_token=fe0.....................................
python3 python3 uploadffpics.py $client_id $client_secret $refresh_token ~/Downloads/NoellesNote/ --description "Noelle's League Note"

INFO:__main__:Retrieved access token for [username=curtis628]
INFO:__main__:Successfully created album [name=BandOfBrothers-2018-10-24] with [id=JRDC4nK]
INFO:__main__:Uploading files in /Users/tcurtis/Downloads/NoellesNote/ using [album_id=JRDC4nK]
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture01.png to Imgur: https://i.imgur.com/Q1DuKUb.png
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture02.png to Imgur: https://i.imgur.com/BqfcNq0.png
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture03.png to Imgur: https://i.imgur.com/jPsOehg.png
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture04.png to Imgur: https://i.imgur.com/rdDXZK9.png
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture05.png to Imgur: https://i.imgur.com/kMwDW7m.png
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture06.png to Imgur: https://i.imgur.com/37g6WCV.png
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture07.png to Imgur: https://i.imgur.com/QU1by3w.png
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture08.png to Imgur: https://i.imgur.com/RzYHtZ5.png
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture09.png to Imgur: https://i.imgur.com/wyydw6b.png
INFO:__main__:Successfully uploaded /Users/tcurtis/Downloads/NoellesNote/Picture10.png to Imgur: https://i.imgur.com/Xz5DSrz.png
INFO:__main__:Successfully uploaded 10 files: ['https://i.imgur.com/Q1DuKUb.png', 'https://i.imgur.com/BqfcNq0.png', 'https://i.imgur.com/jPsOehg.png', 'https://i.imgur.com/rdDXZK9.png', 'https://i.imgur.com/kMwDW7m.png', 'https://i.imgur.com/37g6WCV.png', 'https://i.imgur.com/QU1by3w.png', 'https://i.imgur.com/RzYHtZ5.png', 'https://i.imgur.com/wyydw6b.png', 'https://i.imgur.com/Xz5DSrz.png']
INFO:root:Use the ESPN league note template below as a starting place...
Noelle's League Note

1. 
[center][image]https://i.imgur.com/Q1DuKUb.png[/image]
[/center]


2. 
[center][image]https://i.imgur.com/BqfcNq0.png[/image]
[/center]


3. 
[center][image]https://i.imgur.com/jPsOehg.png[/image]
[/center]


4. 
[center][image]https://i.imgur.com/rdDXZK9.png[/image]
[/center]


5. 
[center][image]https://i.imgur.com/kMwDW7m.png[/image]
[/center]


6. 
[center][image]https://i.imgur.com/37g6WCV.png[/image]
[/center]


7. 
[center][image]https://i.imgur.com/QU1by3w.png[/image]
[/center]


8. 
[center][image]https://i.imgur.com/RzYHtZ5.png[/image]
[/center]


9. 
[center][image]https://i.imgur.com/wyydw6b.png[/image]
[/center]


10. 
[center][image]https://i.imgur.com/Xz5DSrz.png[/image]
[/center]
```

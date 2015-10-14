#!/usr/bin/env python

import os
import sys
import argparse
import glob
import pprint

from dropbox import client, rest

# XXX Fill in your consumer key and secret below
# You can find these at http://www.dropbox.com/developers/apps
APP_KEY = 'jxaiq7pb3ewondu'
APP_SECRET = 'mkxkohh6r3tpuna'

class DropboxClient():
    TOKEN_FILE = "token_store.txt"
    
    def __init__(self, app_key, app_secret, current_path="Public/FantasyFootball"):
        self.app_key = app_key
        self.app_secret = app_secret
        self.api_client = None
        self.current_path = current_path

        try:
            token = open(self.TOKEN_FILE).read()
            self.api_client = client.DropboxClient(token)
            print("[loaded access token]")
        except IOError:
            pass # don't worry if it's not there

    def login(self):
        """log in to a Dropbox account"""
        flow = client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        authorize_url = flow.start()
        sys.stdout.write("1. Go to: " + authorize_url + "\n")
        sys.stdout.write("2. Click \"Allow\" (you might have to log in first).\n")
        sys.stdout.write("3. Copy the authorization code.\n")
        code = raw_input("Enter the authorization code here: ").strip()

        try:
            access_token, user_id = flow.finish(code)
        except rest.ErrorResponse as e:
            self.stdout.write('Error: %s\n' % str(e))
            return

        with open(self.TOKEN_FILE, 'w') as f:
            f.write(access_token)
        self.api_client = client.DropboxClient(access_token)
        
        print("Login successful! userId = ", user_id)

    def logout(self):
        """log out of the current Dropbox account"""
        self.api_client = None
        os.unlink(self.TOKEN_FILE)
        self.current_path = ''
        print("Logout successful!")
        
    def print_metadata(self, path):
        """prints Dropbox metadata for all items in 'path', including ESPN fantasy football syntax"""
        folder_metadata = self.api_client.metadata(self.current_path + "/" + path)
        account_info = self.api_client.account_info()
        uid = account_info['uid']
        
        metadata = "[center][image]http://dl.dropboxusercontent.com/u/{uid}/{filePath}[/image]\n\n[/center]\n"
        for file in folder_metadata['contents']:
            dropboxPath = file['path']
            print(metadata.format(uid=uid, filePath=dropboxPath[8:]))
        
    def print_account_info(self):
        """display account information"""
        f = self.api_client.account_info()
        pprint.PrettyPrinter(indent=2).pprint(f)

    def put(self, from_path, to_path):
        """
        Copy local file to Dropbox

        Examples:
        Dropbox> put ~/test.txt dropbox-copy-test.txt
        """
        
        from_file = open(os.path.expanduser(from_path), "rb")
		
        print("Uploading file from [{}] to Dropbox [{}]".format(from_path, to_path))
        self.api_client.put_file(self.current_path + "/" + to_path, from_file)

def main(folder, projectName, skipUpload=None):
    if APP_KEY == '' or APP_SECRET == '':
        exit("You need to set your APP_KEY and APP_SECRET!")
    client = DropboxClient(APP_KEY, APP_SECRET)
    
    if (client.api_client == None):
        client.login()

    if not skipUpload:
        files = os.listdir(folder)
        for file in files:
            client.put(folder + "/" + file, projectName + "/" + file)
    
    client.print_metadata(projectName)
    
    #client.logout()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This program uploads all items of a specified folder to a public Dropbox folder")
    parser.add_argument("folder",
    					help="the path to the folder to upload to Dropbox")
    parser.add_argument("projectName",
    					help="the name of the project (ie: leagueNote). The program will create this 'projectName' folder within Dropbox")
    parser.add_argument("-skipUpload", 
						help="Don't upload the folder; just print out the metadata of the folder on Dropbox",
						action="store_true")
    
    args = parser.parse_args()
    print("Parsed args: ",	args)
    main(args.folder, args.projectName, args.skipUpload)

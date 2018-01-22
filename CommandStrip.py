#!/usr/bin/env python3

import os
import argparse
import urllib.parse
import urllib.request
import json
from html.parser import HTMLParser

API_URL = "http://www.commitstrip.com/api4dfg/"

class Bcolors:
    """ASCII escape sequences for printing coloured text to terminal. 
    Taken from the blender build scripts"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ImageParser( HTMLParser ):
    """Quick and dirty image URL extractor"""

    def handle_starttag( self, tag, attrs ):
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src":
                    self.img_url = attr[1]

def get_json_data( url ):
    """Reads a JSON string response from a URL"""

    data = urllib.request.urlopen( url ).read()
    jsondata = json.loads( data.decode( "UTF-8" ) )

    if jsondata['status'] != "ok":
        raise Exception( "Error: could not execute statement" )

    return jsondata

def save_comic( url, title, directory ):
    """Retrieves a comic from the URL and saves it with the specified title 
    in the given directory"""

    print( "Retrieving comic at " + url )

    img_path = title + ".jpg"
    if directory != None:
        if not os.path.exists( directory ):
            print( Bcolors.WARNING + 
                  "Directory specified does not exist. Creating directory and saving images" 
                  + Bcolors.ENDC )
            os.makedirs( directory )
        print( "Saving comics in directory " + directory )
        img_path = args.directory + img_path
    
    if os.path.exists( img_path ):
        print( Bcolors.OKGREEN + "Image '" + title + ".jpg' already exists, not downloading" + Bcolors.ENDC )
    else:
        # The URL can contain French characters (is an IRI). The iri_to_uri
        # function takes care of those
        urllib.request.urlretrieve( iri_to_uri( url ), img_path )
        print( Bcolors.OKGREEN + "Retrieved comic '" + title + "'" + Bcolors.ENDC )

def iri_to_uri( iri ):
    """Converts an International Resource Identifier to a URL"""
    parts = urllib.parse.urlparse( iri )
    encoded_parts = []
    for part in list( parts ):
        encoded_parts.append( urllib.parse.quote( part ) )

    return urllib.parse.urlunparse( encoded_parts )

def download_comics( args ):
    """Downloads comics based on the argument set"""

    url = API_URL + "get_post"
    single = False

    params = {}
    if args.slug != None:
        params['slug'] = args.slug
        single = True
    if args.id != None:
        params['id'] = str(args.id)
        single = True
    if args.number != None:
        params['count'] = str(args.number)

    if not single:
        url += 's'
    url += '?'
    url += urllib.parse.urlencode( params )
    json = get_json_data( url )

    parser = ImageParser()
    comics = ( json['post'] if single else json['posts'] )

    if single:
            parser.feed( comics['content'] )
            save_comic( parser.img_url, comics['title'], args.directory )
    else: 
        for post in comics:
            parser.feed( post['content'] )
            save_comic( parser.img_url, post['title'], args.directory )

def search_comic( args ):
    """Searches for a particular comic based on an argument set"""

    url = API_URL + "get_search_results?" + urllib.parse.urlencode( { "search": args.query } )

    json = get_json_data( url )
    comics = json['posts']

    prompt_string = "Found {} ".format( len(comics) )
    if len( comics ) == 1:
        prompt_string += "comic:"
    else:
        prompt_string += "comics:"

    print( Bcolors.OKGREEN + prompt_string + Bcolors.ENDC )
    print( "ID | Title | publish date" )
    for post in comics:
        print( "{} | {} | {}".format( post['id'], post['title'], post['date'] ) )

def create_parser():
    parser = argparse.ArgumentParser( add_help=False )

    sp = parser.add_subparsers()
    sp_download = sp.add_parser( "download", parents=[parser],
                         help="Download an ordered set of comics (latest first)" )
    sp_download.add_argument( "-g", "--slug",
                         help="Comic slug (to download a particular comic)" )
    sp_download.add_argument( "-i", "--id", type=int,
                         help="Comic ID (to download a particular comic)" )
    sp_download.add_argument( "-n", "--number", type=int,
                         help="Number of comics to download (latest first)" )
    parser.add_argument( "-d", "--directory",
                         help="Directory in which to store comics" )
    sp_download.set_defaults( func=download_comics )

    sp_search = sp.add_parser( "search", help="Search for a comic", parents=[parser] )
    sp_search.add_argument( "-q", "--query", required=True,
                         help="Search query" )
    sp_search.set_defaults( func=search_comic )
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
    args.func( args )
    except Exception as e:
        print( Bcolors.FAIL + str(e) + Bcolors.ENDC )

main()
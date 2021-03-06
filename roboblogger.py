# Roboblogger: aggregates multiple blogs into a single, centralized blog.
# Copyright (C) 2010 Internet Archive. Software license AGPL version 3.

# This program is free software: you can redistribute it and/or  modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Contact info:
# Daniel Montalvo
# daniel.m@archive.org

# Prevents two instances of the script from running simultaneously
lock = "lock.txt" 
# The database where old posts are stored
database = 'posts.sqlite'
# The blog where you want to put the aggregated posts
aggBlog = "http://ianews.wordpress.com/xmlrpc.php"
# Blogs you want to aggregate
blogs = ["http://blog.openlibrary.org/feed/", "http://internetarchive.wordpress.com/feed/", "http://www.opencontentalliance.org/feed/", "http://words.nasaimages.org/feed/", "http://www.openbookalliance.org/feed/", "http://iawebarchiving.wordpress.com/feed/", "http://opds-spec.org/feed/"]
# Lets you look up a blog's name, given the url
feeds = {'blog.openlibrary.org':'The Open Library Blog', 'internetarchive.wordpress.com':'The Internet Archive Blog', 'www.opencontentalliance.org':'The Open Content Alliance Blog', 'words.nasaimages.org':'The NASA Images Blog', 'www.openbookalliance.org':'The Open Book Alliance Blog', 'iawebarchiving.wordpress.com':'The Web Archiving at archive.org Blog', 'opds-spec.org':'The OPDS blog'}

import os
import feedparser
import pyblog
from datetime import datetime
from urlparse import urlparse
from sys import argv
import re
import sqlite3

script, username, password = argv

if os.path.exists(lock):
    sys.exit("Lock file exists.")
else:
    f = open(lock, 'w')

conn = sqlite3.connect(database)
c = conn.cursor()

def aggregateBlogs(feedList, aggBlog):
    """Takes a list of blog feeds and an aggregator blog. Adds all unaggregated posts from the blogs in the list and adds them to the aggregator blog."""
    parsedList = parseFeeds(feedList)
    newPostList = getNewPosts(parsedList)
    postToWordPress(newPostList, aggBlog)

def parseFeeds(feedList):
    """Takes a list of feeds and returns them in parsed form."""
    parsedList = []
    for feed in feedList:
       parsedList.append(feedparser.parse(feed))
    return parsedList

def getNewPosts(parsedFeedList):
    """Takes a list of parsed feeds and returns a list of posts that haven't yet been aggregated. """
    newPostList = []
    for parsedFeed in parsedFeedList:
        for post in parsedFeed.entries:
            if not isPosted(post):
                newPostList.append(post)
    return newPostList

def isPosted(post):
    """Takes a post and checks to see if it's in the "old post" database."""
    c.execute('select * from posts where url = ?',(post.link,))
    fetch = c.fetchall()
    posted = [] != fetch
    return posted

def getContent(post):
    """Takes a post and returns the content, plus a link to the original."""
    content = post.content[0].value
    author = post.author
    link = post.link
    site = urlparse(link).netloc
    # Removes digg/reddit/etc. links, and unnecessary images
    content = re.sub('<a href="http://feeds.wordpress.com.*?</a>', '', content)
    content = re.sub('<img .*?http://stats.wordpress.com.*?>', '', content)
    # Adds in a link to the post on the original blog
    ref = '''<div><i><a href ="''' + link + '''">Originally posted on ''' + feeds[site] + ''' by ''' + author + '''.</a></i></div>'''
    content += ref
    return content

def postToWordPress(postList, aggBlog):
    """Takes a list of posts and the aggBlog and then adds the posts to the aggBlog. Adds the post to the database (to record it as "old")."""
    blog = pyblog.WordPress(aggBlog, username, password)
    for post in postList:
        content = getContent(post)
        title = post.title
        date = datetime(*post.updated_parsed[:6])
        tags = []
        x = 0
        for tag in post.tags:
            tags.append(post.tags[x].term)
            x += 1
        postDict = {'title':title, 'description':content, 'dateCreated':date, 'categories':tags}
        id = blog.new_post(postDict)
        updateDatabase(post, id)

def updateDatabase(post, id):
    """Adds the post url and id to the database of aggregated posts."""
    c.execute('insert into posts values (?,?)',(post.link,id))
    conn.commit()

aggregateBlogs(blogs, aggBlog)
c.close()
os.unlink(lock)

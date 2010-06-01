import feedparser
import pyblog
from datetime import datetime
from sys import argv
script, username, password = argv
old_posts = "posts.txt"

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
    """Takes a post and checks to see if it's in the "old post" file."""
    f = open(old_posts)
    urls = f.read()
    f.close()
    return urls.find(post.link) != -1

def postToWordPress(postList, aggBlog):
    """Takes a list of posts and the aggBlog and then adds the posts to the aggBlog. Writes the url of the post to a file (to record it as "old")."""
    blog = pyblog.WordPress(aggBlog, username, password)
    for post in postList:
        content = post.content[0].value
        title = post.title
        date = datetime(*post.updated_parsed[:6])
        postDict = {'title':title, 'description':content, 'dateCreated':date}
        blog.new_post(postDict)
    updateFile(postList)

def updateFile(postList):
    """Writes the posts in the list to a file."""
    f = open(old_posts, 'a')
    for post in postList:
        f.write(post.link)
        f.write("\n")
    f.close()

# blogs = ["http://blog.openlibrary.org/feed/", "http://internetarchive.wordpress.com/feed/", "http://www.opencontentalliance.org/feed/"]

blogs = ["http://blog.openlibrary.org/feed/"]
aggregateBlogs(blogs, "http://dmontalvo.wordpress.com/xmlrpc.php")

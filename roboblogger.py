import feedparser
old_posts = posts.txt

def aggregateBlogs(feedList, aggBlog):
    """Takes a list of blog feeds and an aggregator blog. Adds all unaggregated
    posts from the blogs in the list and adds them to the aggregator blog."""
    parsedList = parseFeeds(feedList)
    newPostList = getNewPosts(parsedList, aggBlog)

def parseFeeds(feedList):
    """Takes a list of feeds and returns them in parsed form."""
    parsedList = []
    for feed in feedList:
       parsedList.append(feedparser.parse(feed))
    return parsedList

def getNewPosts(parsedFeedList, aggBlog):
    """Takes a list of parsed feeds and the aggBlog and returns a list of posts
    not on the aggBlog. Reads a file to check which posts have already been
    aggregated."""
    newPostList = []
    for parsedFeed in parsedFeedList:
        for post in parsedFeed.entries:
            newPostList.append(post)
    return newPostList

def checkPost(post):
    """Checks a post to see if it's in the file of old posts."""

blogs = ["http://blog.openlibrary.org/feed/", "http://internetarchive.wordpress.com/feed/", "http://www.opencontentalliance.org/feed/"]

aggregateBlogs(blogs, "http://www.opencontentalliance.org/feed/")

import feedparser
old_posts = "posts.txt"

def aggregateBlogs(feedList, aggBlog):
    """Takes a list of blog feeds and an aggregator blog. Adds all unaggregated posts from the blogs in the list and adds them to the aggregator blog."""
    parsedList = parseFeeds(feedList)
    newPostList = getNewPosts(parsedList)

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

def postToWordpress(postList, aggBlog):
    """Takes a list of posts and the aggBlog and then adds the posts to the aggBlog. Writes the url of the post to a file (to record it as "old")."""

blogs = ["http://blog.openlibrary.org/feed/", "http://internetarchive.wordpress.com/feed/", "http://www.opencontentalliance.org/feed/"]

aggregateBlogs(blogs, "http://www.opencontentalliance.org/feed/")

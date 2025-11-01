import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

STOPWORDS = set("""
a about above after again against all am an and any are aren't as at be because been before
being below between both but by can can't could couldn't did didn't do does doesn't doing don't
down during each few for from further had hadn't has hasn't have haven't having he he'd he'll
he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is
isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only
or other ought our ours  ourselves out over own same shan't she she'd she'll she's should shouldn't
so some such than that that's the their theirs them themselves then there there's these they they'd
they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're
we've were weren't what what's when when's where where's which while who who's whom why why's with
won't would wouldn't you you'd you'll you're you've your yours yourself yourselves
""".split())


def scraper(url, resp):
    links, token_count, tokens = extract_next_links(url, resp) # token_count refers to the # of raw tokens with stop words, while tokens is the list of clean tokens
    return [link for link in links if is_valid(link)], token_count, tokens

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    linkList = list()
    tokens = list()
    raw_token_count = 0
    if resp.status == 200:
        try:
            soup = BeautifulSoup(resp.raw_response.content.decode(errors='strict'), 'lxml')
        except:
            print("Encoding Error")
            return list(), 0, list() # skip web pages that cannot be encoded as html
       
        text = soup.get_text(separator = " ")
        if soup == None or text == None or len(text) == 0:
            return list(), 0, list() # skip any web pages that have no information
        tokens, raw_token_count = extract_tokens(text) # get tokens in this url for report
        
        tags = soup.find_all('a')
        for tag in tags:
            link = tag.get('href')
            if link == None: # if link is Nothing, then skip it
                continue
            fragIdx = link.find('#') # find index of fragment part
            if fragIdx != -1:
                link = link[:fragIdx] # get rid of fragment part
            linkList.append(link)
    return linkList, raw_token_count, tokens

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if parsed.hostname != None and parsed.hostname.find("ics.uci.edu") == -1 and parsed.hostname.find("cs.uci.edu") == -1 and parsed.hostname.find("informatics.uci.edu") == -1 and parsed.hostname.find("stat.uci.edu") == -1:
            return False # if the hostname doesn't contain any of these domains then return false
        if parsed.query != None and parsed.query.find("ical") != -1:
            return False # if ical is found in query then it is a calendar so we should return false so we dont get stuck in a trap
        if re.search(r"\d{4}-\d{2}-\d{2}", parsed.path.lower()) or re.search(r"\d{4}-\d{2}-\d{2}", parsed.query.lower()) or re.search(r"\d{4}-\d{2}/", parsed.path.lower()) or re.search(r"\d{4}-\d{2}", parsed.query.lower()):
            return False # ignore calendar dates so we dont get stuck in an trap + they don't seem to have much info
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|ppsx)$", parsed.path.lower()) # added ppsx to remove Microsoft powerpoint slide files

    except TypeError:
        print ("TypeError for ", parsed)
        raise
    except ValueError:
        print("ValueError for ", url) 
        # return false if url is a fake/invalid url like the text: https://[YOUR_IP]:8443/manager/html that was found in a web page
        return False

def extract_tokens(text):
    """
    Extracts clean tokens (words) from webpage text.
    Removes punctuation, numbers, and stopwords for report analytics.
    """
    pattern2 = r"\w+[’'-]\w+" # pattern for words like: community's, t-mobile
    pattern3 = r"[0-9]+:[0-9]+" # pattern for words like the time: 10:30
    pattern4 = r"\w*[.]\w+" # pattern for words that use decimal numbers like 10.3 or v0.7 or .5 or other words like ph.d
    tokens = re.findall(pattern4 + "|" + pattern3 + "|" + pattern2 + "|" + r"[A-Za-z0-9]+", text) 

    clean_tokens = [t.lower() for t in tokens if t.lower() not in STOPWORDS]

    return clean_tokens, len(tokens)



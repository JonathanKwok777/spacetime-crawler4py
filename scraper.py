import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

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
    if resp.status == 200:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        text = soup.get_text()
        if text == None or len(text) == 0:
            return list() # skip any web pages that have no information
        tokens = extract_tokens(text) # get tokens in this url for report
        
        tags = soup.find_all('a')
        for tag in tags:
            link = tag.get('href')
            if link == None: # if link is Nothing, then skip it
                continue
            fragIdx = link.find('#') # find index of fragment part
            if fragIdx != -1:
                link = link[:fragIdx] # get rid of fragment part
            linkList.append(link)
    return linkList

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
        if parsed.port != None and parsed.scheme == "https" and parsed.port >= 8000:
            return False # return false for ports in the 8000s for https since its not common and crawler may not be able to access the page
        if parsed.query != None and parsed.query.find("ical") != -1:
            return False # if ical is found in query then it is a calendar so we should return false so we dont get stuck in a trap
        if re.search(r"\d{4}-\d{2}-\d{2}", parsed.path.lower()) or re.search(r"\d{4}-\d{2}-\d{2}", parsed.query.lower()) or re.search(r"\d{4}-\d{2}", parsed.path.lower()) or re.search(r"\d{4}-\d{2}", parsed.query.lower()):
            return False # ignore calendar dates so we dont get stuck in an trap + they don't seem to have much info
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

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
    tokens = re.findall(r"[A-Za-z0-9]+", text)
    clean_tokens = [t.lower() for t in tokens if t.lower() not in STOPWORDS]
    return clean_tokens


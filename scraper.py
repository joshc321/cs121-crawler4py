import re
from urllib.parse import urlparse
from nltk.tokenize import word_tokenize

# helpers import
from helpers import url_check, parse_content, status_check, common_words
from helpers.stopwords import EN_STOPWORDS
from helpers.simhash import simhash, similarity


LOW_VALUE = 25

def scraper(url, resp, fingerprints):
    links = extract_next_links(url, resp, fingerprints)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp, fingerprints):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # need to decide if url or resp.url should be used
    #   url - requested url | resp.url - actual url
    if(status_check.is_valid_status(resp) and is_valid(url)):
        links, text = parse_content.scrape_info(resp.raw_response.content, resp.url)

        tokens = word_tokenize(text.lower())
        page_length = len(tokens)
        # TODO save page length

        

        token_freq = parse_content.token_freq(tokens)
        # remove stop words
        for stop_word in EN_STOPWORDS:
            if stop_word in token_freq:
                token_freq.pop(stop_word)
        
        # remove puncuation and since characters
        for k in set(token_freq.keys()):
            if len(k) < 2:
                token_freq.pop(k)

        if len(token_freq) < LOW_VALUE:
            return []

        fingerprint = simhash(token_freq)

        if is_unique(fingerprints, fingerprint) == False:
            # duplicate page ignore it
            return []
        
        fingerprints[fingerprint] = url

        # TODO save fingerprint for similarity comparisons
        
        # todo store tokens
        common_words.update_data_shelf(token_freq, url)


        return links

    return []

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False

        if url_check.is_valid_domain(parsed) == False:
            return False

        if "archive.ics.uci.edu/ml/datasets.php" in url:
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|svg"
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

def is_unique(fingerprints, fingerprint):
    THRESHOLD = 0.98

    if fingerprint in fingerprints:
        print('duplicate ', fingerprints[fingerprint])
        return False
    
    for fp,url in fingerprints.items():
        if similarity(fp, fingerprint) > THRESHOLD:
            print('similar to', url, similarity(fp, fingerprint))
            return False

    return True

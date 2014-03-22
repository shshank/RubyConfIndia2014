import re
import config

stopWords = [" ", "a", "am", "about", "above", "across", "after", "again", "against", "all", "almost", "alone", "along",
 "already", "also", "although", "always", "among", "an", "and", "another", "any", "anybody", "anyone", 
  "anything", "anywhere", "are", "area", "areas", "around", "as", "ask", "asked", "asking", "asks", "at", 
  "away", "b", "back", "backed", "backing", "backs", "be", "became", "because", "become", "becomes", "been", 
  "before", "began", "behind", "being", "beings", "best", "better", "between", "big", "both", "but", "by", "c", 
  "came", "can", "cannot", "case", "cases", "certain", "certainly", "clear", "clearly", "come", "could", "d", 
  "did", "differ", "different", "differently", "do", "does", "done", "down", "downed", "downing", "downs", 
  "during", "e", "each", "early", "either", "end", "ended", "ending", "ends", "enough", "even", "evenly", 
  "ever", "every", "everybody", "everyone", "everything", "everywhere", "f", "face", "faces", "fact", "facts", 
  "far", "felt", "few", "find", "finds", "first", "for", "four", "from", "full", "fully", "further", 
  "furthered", "furthering", "furthers", "g", "gave", "general", "generally", "get", "gets", "give", "given", 
  "gives", "go", "going", "good", "goods", "got", "great", "greater", "greatest", "group", "grouped", 
  "grouping", "groups", "h", "had", "has", "have", "having", "he", "her", "here", "herself", "high", "higher", 
  "highest", "him", "himself", "his", "how", "however", "i", "if", "important", "in", "interest", "interested", 
  "interesting", "interests", "into", "is", "it", "its", "itself", "j", "just", "k", "keep", "keeps", "kind", 
  "knew", "know", "known", "knows", "l", "large", "largely", "last", "later", "latest", "least", "less", "let", 
  "lets", "like", "likely", "long", "longer", "longest", "looking", "m", "made", "make", "making", "man", "many", "may", 
  "me", "member", "members", "men", "might", "more", "most", "mostly", "mr", "mrs", "much", "must", "my", 
  "myself", "n", "necessary", "need", "needed", "needing", "needs", "never", "new", "newer", "newest", "next", 
  "no", "nobody", "non", "noone", "not", "nothing", "now", "nowhere", "number", "numbers", "o", "of", "off", 
  "often", "old", "older", "oldest", "on", "once", "one", "only", "open", "opened", "opening", "opens", "or", 
  "order", "ordered", "ordering", "orders", "other", "others", "our", "out", "over", "p", "part", "parted", 
  "parting", "parts", "per", "perhaps", "place", "places", "point", "pointed", "pointing", "points", 
  "possible", "present", "presented", "presenting", "presents", "problem", "problems", "put", "puts", "q", 
  "quite", "r", "rather", "really", "right", "room", "rooms", "s", "said", "same", "saw", "say", "says", 
  "second", "seconds", "see", "seem", "seemed", "seeming", "seems", "sees", "several", "shall", "she", 
  "should", "show", "showed", "showing", "shows", "side", "sides", "since", "small", "smaller", "smallest", 
  "so", "some", "somebody", "someone", "something", "somewhere", "state", "states", "still", "such", "sure", 
  "t", "take", "taken", "than", "that", "the", "their", "them", "then", "there", "therefore", "these", "they", 
  "thing", "things", "think", "thinks", "this", "those", "though", "thought", "thoughts", "three", "through", 
  "thus", "time", "to", "today", "together", "too", "took", "toward", "turn", "turned", "turning", "turns", 
  "two", "u", "under", "until", "up", "upon", "us", "use", "used", "uses", "v", "very", "w", "want", "wanted", 
  "wanting", "wants", "was", "way", "ways", "we", "well", "wells", "went", "were", "what", "when", "where", 
  "whether", "which", "while", "who", "whole", "whose", "why", "will", "with", "within", "without", "work", 
  "worked", "working", "works", "would", "x", "y", "year", "years", "yet", "you", "young", "younger", 
  "youngest", "your", "yours", "z", 'ur', 'via', 'url']


stopWords = stopWords+config.ignore_words

def processTweet(tweet):
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet


def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
 

def getFeatureVector(tweet):
    featureVector = []
    #get processedTweet
    tweet = processTweet(tweet)
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w.lower() in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector

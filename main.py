from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
import nltk
import requests 

nltk.download('stopwords')
nltk_stop_words = set(stopwords.words('english'))
custom_stop_words = ["to", "in", "min", "read", "news", "fox", "of", "the", "for", "and", "a", "an", "on", "at", "by", "as", 
                     "&", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "menu", "games", "video", "watch", "cnn", "ad",
                     "•", "images", "sign", "show", "weather", "newsletters", "food", "videos", "subscribe", "sports", "science",
                     "entertainment", "oan"]

stop_words = set(nltk_stop_words.union(custom_stop_words))


def page_contents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    contents = requests.get(url, headers=headers)
 
    if contents.status_code == 200:
        return contents
    
    raise Exception("Error retrieving contents for " + url)

def extract_headlines(contents):
    contents = page_contents(contents)

    soup_results = BeautifulSoup(contents.text, 'html.parser')

    soup_results.select('[class*=__headline-text]')
    headlines = [element.get_text(separator=" ", strip=True) for element in soup_results]
    return headlines

def word_frequency(list):
    word_frequencies = Counter(list)
    # sort the list by most commonly used words
    freq_list = word_frequencies.most_common(10)
    # filter out words that are not contained in nltk stopwords and custom stopwords
    filtered_frequencies = {word: freq for word, freq in word_frequencies.items() if word.lower() not in stop_words}
    # orders the words by frequency in decending order
    prdered_freq_list = sorted(filtered_frequencies.items(), key=lambda x: x[1], reverse=True)
    return prdered_freq_list

def get_words(list):
    all_headlines = Counter({})
    for website in list: 
        headlines = extract_headlines(website)
        all_headlines += word_frequency(headlines)

    return all_headlines


# initialize news sources as immutable lists
# catagorize them into right/left leaning bias
left_leaning = ["https://www.cnn.com",
"https://www.msnbc.com",
"https://www.washingtonpost.com",
"https://www.huffpost.com",
"https://www.vox.com"]


right_leaning = ["https://www.foxnews.com",
"https://www.breitbart.com",
"https://www.dailycaller.com",
"https://www.nationalreview.com",
"https://www.washingtontimes.com",
"https://www.oann.com"]



print(get_words(left_leaning))
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

    # ***__headline-text is used across many news organizations to denote headlines on the front page
    soup_results = soup_results.select('[class*=__headline-text]')
    print(soup_results)
    headlines = [element.get_text(separator=" ", strip=True) for element in soup_results]
    print(headlines)
    return headlines

def word_frequency(headlines):
    words = []
    for headline in headlines:
        words.extend(headline.split())
    word_frequencies = Counter(words)
    # Filter out stop words
    filtered_frequencies = {word: freq for word, freq in word_frequencies.items() if word.lower() not in stop_words}
    ordered_freq_list = sorted(filtered_frequencies.items(), key=lambda x: x[1], reverse=True)
    return ordered_freq_list

def get_words(list):
    all_headlines = []
    for website in list: 
        print("Processing Website: " + website)
        headlines = extract_headlines(website)
        freq = word_frequency(headlines)
        all_headlines = all_headlines + freq

    return all_headlines


# initialize news sources as immutable lists
# catagorize them into right/left leaning bias
left_leaning = ["https://www.cnn.com",
"https://www.msnbc.com",
"https://www.huffpost.com",
"https://www.vox.com"] 


right_leaning = ["https://www.foxnews.com",
"https://www.breitbart.com",
"https://www.dailycaller.com",
"https://www.oann.com"]



print(get_words(right_leaning))
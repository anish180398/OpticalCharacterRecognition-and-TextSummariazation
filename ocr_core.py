try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import re
import nltk
import heapq 
nltk.download('punkt')
def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    output_file("ConvertedFile.txt", text)
    article_text = text
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    formatted_article = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article = re.sub(r'\s+', ' ', formatted_article)
    tokenize_sentence = nltk.sent_tokenize(article_text)
    
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequency = {}
    for word in nltk.word_tokenize(formatted_article):
        if word not in stopwords:
            if word not in word_frequency.keys():
                word_frequency[word] = 1
            else: 
                word_frequency[word] += 1
    maximum_frequncy = max(word_frequency.values())
    for word in word_frequency.keys():
        word_frequency[word] = (word_frequency[word] / maximum_frequncy)
    sentence_score = {}
    for sent in tokenize_sentence:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequency.keys():
                if len(sent.split(' ')) < 50:
                    if sent not in sentence_score.keys():
                        sentence_score[sent] = word_frequency[word]
                    else:
                        sentence_score[sent] += word_frequency[word]
    sentence_summary = heapq.nlargest(10, sentence_score, key = sentence_score.get)
    summary = ' '.join(sentence_summary)
    output_file("SummarizedFile.txt",summary)
    return text  # Then we will print the text in the image

def output_file(filename, data):
	file = open(filename, "w+")
	file.write(data)
	file.close()


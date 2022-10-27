from flask import Flask, jsonify,request
import json
response=''
app = Flask(__name__)


@app.route('/api',methods=['GET'])
def nlp():
    d={}
    global response
    text=str(request.args['query'])
    summary=''
    '''Text summarization on the basis of frequency of words'''
    # lang=input("Enter language:")

    lang = 'english'
    '''Step 1'''
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    import nltk

    nltk.download('punkt')
    nltk.download('stopwords')

    '''step 2'''
    # fullSummary=""

    # filename = 'unlabelled_documents/' + str(i)+'.txt'
    lines = []

    # f = open(filename,'r',encoding="cp437")
    # text = f.read()
    # f.close
    # text=inptext['text']
    # text = "When combining the AD curve and AS curve together, it will form a AD/AS graph and there’s an intersection of the two curves which gives the overall equilibrium level of real output (GDP) and the price level. If a price level is above equilibrium level, there is more output being supplied than people want to buy. The excess supply will cause producers to drop their prices and hence the price level will fall back to equilibrium. The quantity of goods and services supplied will also contract. If the price level is too low, the demand for output exceeds the supply and a combination of rising prices and rising output will restore to the equilibrium level."
    '''sent means sentence'''
    '''file divided into sentences'''
    sent_tokens = nltk.sent_tokenize(text)
    '''file divided into words'''
    word_tokens = nltk.word_tokenize(text)

    word_tokens_lower = []
    for word in word_tokenize(text):
        word_tokens_lower.append(word.lower())

    stopWords = list(set(stopwords.words(lang)))

    word_tokens_refined = []
    for x in word_tokens_lower:
        if x not in stopWords:
            word_tokens_refined.append(x)

    '''print(len(word_tokens_refined))'''

    '''step 3'''
    freqTable = dict()
    for word in word_tokens_refined:
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    '''print(len(freqTable))'''

    '''step 4'''
    sentenceValue = dict()
    for sentence in sent_tokens:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    '''step 5'''
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))
    summary = ''
    for sentence in sent_tokens:
        if (sentence in sentenceValue) and sentenceValue[sentence] > (1.2 * average):
            summary += " " + sentence
    print(summary)
    answer=str(summary)
    d['output']=answer
    print(d)
    res = jsonify({'output': answer})
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res



if __name__ =="__main__":
    app.run(debug=True)
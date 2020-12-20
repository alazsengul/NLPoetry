from flask import Flask, render_template, Response, request, jsonify, url_for
import random
import csv
import os
import spacy
import numpy as np
import pandas as pd


app = Flask(__name__)

poets_to_files = {
    "Maya Angelou" : "maya_angelou_poems.csv",
    "Langston Hughes" : "langston_hughes_poems.csv",
    "Pablo Neruda" : "pablo_neruda_poems.csv",
    "William Wordsworth" : "william_wordsworth_poems.csv",
    "William Shakespeare" : "william_shakespeare_poems.csv",
    "Charles Bukowski" : "charles_bukowski_poems.csv",
    "Robert Burns" : "robert_burns_poems.csv",
    "Rabindranath Tagore" : "rabindranath_tagore_poems.csv",
    "Robert Frost" : "robert_frost_poems.csv",
    "Edgar Allan Poe" : "edgar_allan_poe_poems.csv",
    "Sylvia Plath" : "sylvia_plath_poems.csv",
    "Walt Whitman" : "walt_whitman_poems.csv",
    "William Blake" : "william_blake_poems.csv",
    "Dylan Thomas" : "dylan_thomas_poems.csv",
    "John Keats" : "john_keats_poems.csv",
    "Wilfred Owen" : "wilfred_owen_poems.csv",
    "Roald Dahl" : "roald_dahl_poem.csv"
}

#

@app.route('/')
def index():
    return(render_template("index.html"))

def poem_generator(file, word, num_sen=12):
    spacy_nlp = spacy.load("en_core_web_sm")
    subject = spacy_nlp(word)
    sentences = pd.read_csv(os.getcwd() +'/'+ file).fillna("")
    poem_id = int()
    poem_lst = []
    
    for i in range(num_sen):
        rand = np.random.randint(0, sentences.shape[0], size = 30)
        docs = spacy_nlp.pipe(list(sentences.sentence.iloc[rand]))
        
        similarities = []
        for s in docs:
            similarities.append(spacy_nlp(word).similarity(s))
            
        s_dict = {
            'similarity' : similarities,
            'doc_id' : sentences.doc_id.iloc[rand]
        }
        
        df_sim = pd.DataFrame(s_dict, index=rand)
        df_sim = df_sim[df_sim.doc_id != poem_id]
        df_sim.sort_values(by='similarity', inplace=True, ascending=False)
        
        s = sentences.sentence[df_sim.index[0]]
        
        change_chars = {
            '\n' :  '', 
            '\r' :  '', 
        }
        
        for x, y in change_chars.items():
            s = s.replace(x, y)
        
        poem_lst.append(s)
        poem_id = df_sim.doc_id.iloc[0]
        subject = spacy_nlp(s)
    
    poem = ("\n".join(poem_lst))
    return poem

def poem_format(text):
    return (text[:1].upper() + text[1:])[:-1] + '.'

@app.route('/fetch_poems', methods=['GET'])
def fetch_poems():

    global poets_to_files

    poet = random.choice(list(poets_to_files.keys()))
    poet_filename = poets_to_files[poet]

    with open("poems/" + poet_filename) as f:

        reader = csv.reader(f)
        next(reader)
        random_row = random.choice(list(reader))
    
    poem_label = f"\"{random_row[1].upper()}\" — {poet.upper()}"
    poem_text = random_row[2]

    sentences_csv = "sentences/sentences_" + poet_filename
    fake_poem = poem_generator(file=sentences_csv, word="valor")
    fake_poem = poem_format(fake_poem)

    fake_poem = "<br>".join([i for i in fake_poem.lower().splitlines()])
    poem_text = "<br>".join([i for i in poem_text.lower().splitlines() if i][:12])

    return(jsonify(poem_label=poem_label, poem_text=poem_text, fake_poem=fake_poem))


if __name__ == '__main__':
    app.run(debug = True)

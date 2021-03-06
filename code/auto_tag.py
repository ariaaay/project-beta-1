import nltk
import json
import sys




affordance_dict_fpath = sys.argv[1] #loadin the json file with all unique words as keys

with open(affordance_dict_fpath) as fid:
    affordanceDict = json.loads(fid.readlines()[0])
fid.close()

all_words = affordanceDict.keys()
word_dict = dict.fromkeys(all_words)



def get_wn_synsets(lemma):
   """
   Get all synsets for a word, return a list of [wordnet_label,definition, hypernym_string]
   for all synsets returned.
   """
   from nltk.corpus import wordnet as wn
   synsets = wn.synsets(lemma)
   out = []
   for s in synsets:
       # if not '.v.' in s.name(): continue # only verbs!
       hyp = ''
       for ii,ss in enumerate(s.hypernym_paths()):
           try:
               hyp+=(repr([hn.name() for hn in ss])+'\n')
           except:
               hyp+='FAILED for %dth hypernym\n'%ii
       out.append(dict(synset=s.name(), definition=s.definition(),hypernyms=hyp))
   return out

def get_wn_meaning(lemma):
    """get meaning of a word using wordNet labels"""
    # from nltk.corpus import wordnet as wn
    # return wn.synset(lemma).definition()
    return None


for w in all_words:
    if get_wn_synsets(w) == []:
        word_dict.pop(w)
    else:
        word_dict[w] = [get_wn_synsets(w)[0]['synset']]

with open("../description_pp/word2wn.json", 'w') as f:
    json.dump(word_dict, f) 

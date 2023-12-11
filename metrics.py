import re
import json 
import pandas as pd
import os
def has_word(sentence, word):
    pattern = r"\b" + re.escape(word) + r"\b"
    match = re.search(pattern, sentence)
    if match:
        return True
    else:
        return False
def remove_special_chars(s):
    pattern = r"[^a-zA-Z0-9\s]"
    s = re.sub(pattern, "", s)
    return s

def load_jsonl(path):
    data=[]
    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            data.append(json.loads(line))
    return data 

class VQAEval:
    def __init__(self):
        self.contractions = {
            "aint": "ain't",
            "arent": "aren't",
            "cant": "can't",
            "couldve": "could've",
            "couldnt": "couldn't",
            "couldn'tve": "couldn't've",
            "couldnt've": "couldn't've",
            "didnt": "didn't",
            "doesnt": "doesn't",
            "dont": "don't",
            "hadnt": "hadn't",
            "hadnt've": "hadn't've",
            "hadn'tve": "hadn't've",
            "hasnt": "hasn't",
            "havent": "haven't",
            "hed": "he'd",
            "hed've": "he'd've",
            "he'dve": "he'd've",
            "hes": "he's",
            "howd": "how'd",
            "howll": "how'll",
            "hows": "how's",
            "Id've": "I'd've",
            "I'dve": "I'd've",
            "Im": "I'm",
            "Ive": "I've",
            "isnt": "isn't",
            "itd": "it'd",
            "itd've": "it'd've",
            "it'dve": "it'd've",
            "itll": "it'll",
            "let's": "let's",
            "maam": "ma'am",
            "mightnt": "mightn't",
            "mightnt've": "mightn't've",
            "mightn'tve": "mightn't've",
            "mightve": "might've",
            "mustnt": "mustn't",
            "mustve": "must've",
            "neednt": "needn't",
            "notve": "not've",
            "oclock": "o'clock",
            "oughtnt": "oughtn't",
            "ow's'at": "'ow's'at",
            "'ows'at": "'ow's'at",
            "'ow'sat": "'ow's'at",
            "shant": "shan't",
            "shed've": "she'd've",
            "she'dve": "she'd've",
            "she's": "she's",
            "shouldve": "should've",
            "shouldnt": "shouldn't",
            "shouldnt've": "shouldn't've",
            "shouldn'tve": "shouldn't've",
            "somebody'd": "somebodyd",
            "somebodyd've": "somebody'd've",
            "somebody'dve": "somebody'd've",
            "somebodyll": "somebody'll",
            "somebodys": "somebody's",
            "someoned": "someone'd",
            "someoned've": "someone'd've",
            "someone'dve": "someone'd've",
            "someonell": "someone'll",
            "someones": "someone's",
            "somethingd": "something'd",
            "somethingd've": "something'd've",
            "something'dve": "something'd've",
            "somethingll": "something'll",
            "thats": "that's",
            "thered": "there'd",
            "thered've": "there'd've",
            "there'dve": "there'd've",
            "therere": "there're",
            "theres": "there's",
            "theyd": "they'd",
            "theyd've": "they'd've",
            "they'dve": "they'd've",
            "theyll": "they'll",
            "theyre": "they're",
            "theyve": "they've",
            "twas": "'twas",
            "wasnt": "wasn't",
            "wed've": "we'd've",
            "we'dve": "we'd've",
            "weve": "we've",
            "werent": "weren't",
            "whatll": "what'll",
            "whatre": "what're",
            "whats": "what's",
            "whatve": "what've",
            "whens": "when's",
            "whered": "where'd",
            "wheres": "where's",
            "whereve": "where've",
            "whod": "who'd",
            "whod've": "who'd've",
            "who'dve": "who'd've",
            "wholl": "who'll",
            "whos": "who's",
            "whove": "who've",
            "whyll": "why'll",
            "whyre": "why're",
            "whys": "why's",
            "wont": "won't",
            "wouldve": "would've",
            "wouldnt": "wouldn't",
            "wouldnt've": "wouldn't've",
            "wouldn'tve": "wouldn't've",
            "yall": "y'all",
            "yall'll": "y'all'll",
            "y'allll": "y'all'll",
            "yall'd've": "y'all'd've",
            "y'alld've": "y'all'd've",
            "y'all'dve": "y'all'd've",
            "youd": "you'd",
            "youd've": "you'd've",
            "you'dve": "you'd've",
            "youll": "you'll",
            "youre": "you're",
            "youve": "you've",
        }
        self.manualMap = {
            "none": "0",
            "zero": "0",
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
            "ten": "10",
        }
        self.articles = ["a", "an", "the"]

        self.periodStrip = re.compile("(?!<=\d)(\.)(?!\d)")
        self.commaStrip = re.compile("(\d)(\,)(\d)")
        self.punct = [
            ";",
            r"/",
            "[",
            "]",
            '"',
            "{",
            "}",
            "(",
            ")",
            "=",
            "+",
            "\\",
            "_",
            "-",
            ">",
            "<",
            "@",
            "`",
            ",",
            "?",
            "!",
        ]

    def evaluate(self, answer, gt_answers):
        
        answer = answer.replace("\n", " ")
        answer = answer.replace("\t", " ")
        answer = answer.strip()
        answer = self.processPunctuation(answer)
        answer = self.processDigitArticle(answer)

        if type(gt_answers)==list:
            for i in range(len(gt_answers)):
                gt_answers[i] = gt_answers[i].replace("\n", " ")
                gt_answers[i] = gt_answers[i].replace("\t", " ")
                gt_answers[i] = gt_answers[i].strip()
                gt_answers[i] = self.processPunctuation(gt_answers[i])
                gt_answers[i] = self.processDigitArticle(gt_answers[i])
                if has_word(answer, gt_answers[i]):
                    return 1
            return 0
        else:
            gt_answers = gt_answers.replace("\n", " ")
            gt_answers= gt_answers.replace("\t", " ")
            gt_answers = gt_answers.strip()
            gt_answers = self.processPunctuation(gt_answers)
            gt_answers = self.processDigitArticle(gt_answers)

            if has_word(answer, gt_answers):
                return 1
            else:
                return 0

    def processPunctuation(self, inText):
        outText = inText
        for p in self.punct:
            if (p + " " in inText or " " + p in inText) or (
                re.search(self.commaStrip, inText) != None
            ):
                outText = outText.replace(p, "")
            else:
                outText = outText.replace(p, " ")
        outText = self.periodStrip.sub("", outText, re.UNICODE)
        return outText

    def processDigitArticle(self, inText):
        outText = []
        tempText = inText.lower().split()
        for word in tempText:
            # word = self.manualMap.setdefault(word, word)
            if word not in self.articles:
                outText.append(word)
            else:
                pass
        for wordId, word in enumerate(outText):
            if word in self.contractions:
                outText[wordId] = self.contractions[word]
        outText = " ".join(outText)
        return outText

# def automatic_metric(csv_filepath):
#     evaluator = VQAEval()

# def exact_match(filepath):
#     df = pd.read_csv(filepath)

#     model_a_em = 

#     pass

def get_human_response_distribution(filepath):
    # human distribution
    df = pd.read_csv(filepath).iloc[10:110]
    response_dict = {"(a)":0, "(b)":0, "(c)":0, "(d)":0}
    for idx in range(len(df)):
        for k, _ in response_dict.items():
            if k in df.at[10+idx, "response"]:
                response_dict[k]+=1

    print("--Summary--")
    # print(f"Model A is Better: {response_dict['(a)']/len(df)}")
    # print(f"Model B is Better: {response_dict['(b)']/len(df)}")
    # print(f"Both Model Good: {response_dict['(c)']/len(df)}")
    # print(f"Neither Model is Good: {response_dict['(d)']/len(df)}")
    b_win = (response_dict['(b)'] + (response_dict['(c)'] + response_dict['(d)'])*0.5)/len(df)
    a_win = 1 - b_win
    print(f"Model A Win Rate: {a_win}")
    print(f"Model B Win Rate: {b_win}")
def get_gpt_response_distribution(filepath):

    # gpt distribution
    data = load_jsonl(filepath)
    response_dict = {"(a)":0, "(b)":0, "(c)":0, "(d)":0}
    for d in data:
        if d["feedback"] in response_dict:
            response_dict[d["feedback"]]+=1

        else:
            response_dict["(d)"]+=1

    print("--Summary--")
    # print(f"Model A is Better: {response_dict['(a)']/len(data)}")
    # print(f"Model B is Better: {response_dict['(b)']/len(data)}")
    # print(f"Both Model Good: {response_dict['(c)']/len(data)}")
    # print(f"Neither Model is Good: {response_dict['(d)']/len(data)}")
    b_win = (response_dict['(b)'] + (response_dict['(c)'] + response_dict['(d)'])*0.5)/len(data)
    a_win = 1 - b_win
    print(f"Model A Win Rate: {a_win}")
    print(f"Model B Win Rate: {b_win}")



def model_win_rate(filepath):
    pass


if __name__ == "__main__":

    csv_dir = "./course/ann"
    output_dir = "./course/output"

    #human response distribution
    hfile_list = [
        "docvqa_final.csv",
        "infovqa_final.csv",
        "stvqa_final.csv"
    ]

    print("Human Distribution \n")
    for f in hfile_list:
        print(f"Dataset name: {f.split('_')[0]}\n")
        get_human_response_distribution(os.path.join(csv_dir,f))
        print()

    #gpt response distribution
    gfile_list = [
        "docvqa_final_indomain_1.jsonl",
        "docvqa_final_indomain_3.jsonl",
        "docvqa_final_outdomain_1.jsonl",
        "docvqa_final_outdomain_3.jsonl",
        "infovqa_final_indomain_1.jsonl",
        "infovqa_final_indomain_3.jsonl",
        "infovqa_final_outdomain_1.jsonl",
        "infovqa_final_outdomain_3.jsonl",
        "stvqa_final_indomain_1.jsonl",
        "stvqa_final_indomain_3.jsonl",
        "stvqa_final_outdomain_1.jsonl",
        "stvqa_final_outdomain_3.jsonl",
    ]

    print("GPT Distribution \n")
    for f in gfile_list:
        print(f"Dataset name: {f.split('_')[0]}\n")
        print(f"Domain: {f.split('_')[2]}\n")
        print(f"# In context ex: {f.split('_')[3].split('.')[0]}\n")

        get_gpt_response_distribution(os.path.join(output_dir,f))
        print()


import os
import csv
import time 
import openai
import argparse
import pandas as pd
from tqdm import tqdm
import json
import cv2
from constants import RANKINGS_PROMPT

openai.api_key = os.getenv("OPENAI_API_KEY")
parser = argparse.ArgumentParser()

parser.add_argument('--gpt_version', choices=['gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-16k'], default='gpt-3.5-turbo')
parser.add_argument('--input_filepath', type = str, default = 'chatgpt_feedback/without_dolly/test_pairwise_data.csv')
parser.add_argument('--save_feedback_filepath', type = str, default = None)
parser.add_argument('--start_index', type = int, default = 0)

args = parser.parse_args()

PROMPT_DICT = {
    "prompt_input": (
        "{instruction}\n\nOCR Text of the image:\n{input}"
    ),
    "prompt_no_input": (
        "{instruction}"
    ),
}

def dump_jsonl(data, output_path, append=False):
    """
    Write list of objects to a JSON lines file.
    """
    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + '\n')
    print('Wrote {} records to {}'.format(len(data), output_path))


def get_reward(instruction, input, gt_answer, output_1, output_2):
    if str(input) == "":
        instruction = PROMPT_DICT['prompt_no_input'].format(instruction = instruction)
        prompt = RANKINGS_PROMPT.format(instruction = instruction, gt_answer = gt_answer, output_1 = output_1, output_2 = output_2)
    else:
        instruction = PROMPT_DICT['prompt_input'].format(instruction = instruction, input = input)
        prompt = RANKINGS_PROMPT.format(instruction = instruction, gt_answer = gt_answer,output_1 = output_1, output_2 = output_2)

    messages = [{"role": "user", "content": prompt}]

    return messages


def main():

    df = pd.read_csv(args.input_filepath)
    df = df.iloc[args.start_index:] # 10 index

    chatgpt_eval_data = []
    cnt = 0
    for j in tqdm(range(len(df))):
        # if cnt == 20:
        #     break

        try:
            instruction = df.iloc[j]['question']
            # input = "" # to be changed
            gt_answer = pass
            output1 = pass
            output2 = pass
            completion = openai.ChatCompletion.create(
                model = args.gpt_version, 
                messages = get_reward(instruction, input, gt_answer, output1, output2))
            feedback_1 = completion['choices'][0]['message']['content']
            completion = openai.ChatCompletion.create(
                model = args.gpt_version, 
                messages = get_reward(instruction, input, gt_answer, output2, output1))
            feedback_2 = completion['choices'][0]['message']['content']
            if '(a)' in feedback_1 and '(b)' in feedback_2:
                feedback = '(a)'
            elif '(b)' in feedback_1 and '(a)' in feedback_2:
                feedback = '(b)'
            elif '(a)' in feedback_1 and '(a)' in feedback_2:
                feedback = '(d)'
            elif '(b)' in feedback_1 and '(b)' in feedback_2:
                feedback = '(d)'
            elif '(c)' in feedback_1 or '(c)' in feedback_2:
                feedback = '(c)'
            else:
                feedback = '(d)'

            print(instruction)
            print(gt_answer)
            print(feedback_1, feedback_2, feedback)
            cnt+=1
            chatgpt_eval_data.append({
                "instruction":instruction,
                "gt_answer":gt_answer,
                "output_1":output1,
                "output_2":output2,
                "feedback_1":feedback_1,
                "feedback_2":feedback_2,
                "feedback":feedback
            })
        except:
            print('Sleeping...')
            time.sleep(5)
            chatgpt_eval_data.append({
                "instruction":instruction,
                "gt_answer":gt_answer,
                "output_1":output1,
                "output_2":output2,
                "feedback_1":feedback_1,
                "feedback_2":feedback_2,
                "feedback":"NA"
            })
        if cnt%15==0:
            print("interval sleeping")
            time.sleep(10)
    dump_jsonl(chatgpt_eval_data, args.save_feedback_filepath)

if __name__ == '__main__':
    main()


# def has_word(sentence, word):
#     pattern = r"\b" + re.escape(word) + r"\b"
#     match = re.search(pattern, sentence)
#     if match:
#         return True
#     else:
#         return False
# def remove_special_chars(s):
#     pattern = r"[^a-zA-Z0-9\s]"
#     s = re.sub(pattern, "", s)
#     return s

# class VQAEval:
#     def __init__(self):
#         self.contractions = {
#             "aint": "ain't",
#             "arent": "aren't",
#             "cant": "can't",
#             "couldve": "could've",
#             "couldnt": "couldn't",
#             "couldn'tve": "couldn't've",
#             "couldnt've": "couldn't've",
#             "didnt": "didn't",
#             "doesnt": "doesn't",
#             "dont": "don't",
#             "hadnt": "hadn't",
#             "hadnt've": "hadn't've",
#             "hadn'tve": "hadn't've",
#             "hasnt": "hasn't",
#             "havent": "haven't",
#             "hed": "he'd",
#             "hed've": "he'd've",
#             "he'dve": "he'd've",
#             "hes": "he's",
#             "howd": "how'd",
#             "howll": "how'll",
#             "hows": "how's",
#             "Id've": "I'd've",
#             "I'dve": "I'd've",
#             "Im": "I'm",
#             "Ive": "I've",
#             "isnt": "isn't",
#             "itd": "it'd",
#             "itd've": "it'd've",
#             "it'dve": "it'd've",
#             "itll": "it'll",
#             "let's": "let's",
#             "maam": "ma'am",
#             "mightnt": "mightn't",
#             "mightnt've": "mightn't've",
#             "mightn'tve": "mightn't've",
#             "mightve": "might've",
#             "mustnt": "mustn't",
#             "mustve": "must've",
#             "neednt": "needn't",
#             "notve": "not've",
#             "oclock": "o'clock",
#             "oughtnt": "oughtn't",
#             "ow's'at": "'ow's'at",
#             "'ows'at": "'ow's'at",
#             "'ow'sat": "'ow's'at",
#             "shant": "shan't",
#             "shed've": "she'd've",
#             "she'dve": "she'd've",
#             "she's": "she's",
#             "shouldve": "should've",
#             "shouldnt": "shouldn't",
#             "shouldnt've": "shouldn't've",
#             "shouldn'tve": "shouldn't've",
#             "somebody'd": "somebodyd",
#             "somebodyd've": "somebody'd've",
#             "somebody'dve": "somebody'd've",
#             "somebodyll": "somebody'll",
#             "somebodys": "somebody's",
#             "someoned": "someone'd",
#             "someoned've": "someone'd've",
#             "someone'dve": "someone'd've",
#             "someonell": "someone'll",
#             "someones": "someone's",
#             "somethingd": "something'd",
#             "somethingd've": "something'd've",
#             "something'dve": "something'd've",
#             "somethingll": "something'll",
#             "thats": "that's",
#             "thered": "there'd",
#             "thered've": "there'd've",
#             "there'dve": "there'd've",
#             "therere": "there're",
#             "theres": "there's",
#             "theyd": "they'd",
#             "theyd've": "they'd've",
#             "they'dve": "they'd've",
#             "theyll": "they'll",
#             "theyre": "they're",
#             "theyve": "they've",
#             "twas": "'twas",
#             "wasnt": "wasn't",
#             "wed've": "we'd've",
#             "we'dve": "we'd've",
#             "weve": "we've",
#             "werent": "weren't",
#             "whatll": "what'll",
#             "whatre": "what're",
#             "whats": "what's",
#             "whatve": "what've",
#             "whens": "when's",
#             "whered": "where'd",
#             "wheres": "where's",
#             "whereve": "where've",
#             "whod": "who'd",
#             "whod've": "who'd've",
#             "who'dve": "who'd've",
#             "wholl": "who'll",
#             "whos": "who's",
#             "whove": "who've",
#             "whyll": "why'll",
#             "whyre": "why're",
#             "whys": "why's",
#             "wont": "won't",
#             "wouldve": "would've",
#             "wouldnt": "wouldn't",
#             "wouldnt've": "wouldn't've",
#             "wouldn'tve": "wouldn't've",
#             "yall": "y'all",
#             "yall'll": "y'all'll",
#             "y'allll": "y'all'll",
#             "yall'd've": "y'all'd've",
#             "y'alld've": "y'all'd've",
#             "y'all'dve": "y'all'd've",
#             "youd": "you'd",
#             "youd've": "you'd've",
#             "you'dve": "you'd've",
#             "youll": "you'll",
#             "youre": "you're",
#             "youve": "you've",
#         }
#         self.manualMap = {
#             "none": "0",
#             "zero": "0",
#             "one": "1",
#             "two": "2",
#             "three": "3",
#             "four": "4",
#             "five": "5",
#             "six": "6",
#             "seven": "7",
#             "eight": "8",
#             "nine": "9",
#             "ten": "10",
#         }
#         self.articles = ["a", "an", "the"]

#         self.periodStrip = re.compile("(?!<=\d)(\.)(?!\d)")
#         self.commaStrip = re.compile("(\d)(\,)(\d)")
#         self.punct = [
#             ";",
#             r"/",
#             "[",
#             "]",
#             '"',
#             "{",
#             "}",
#             "(",
#             ")",
#             "=",
#             "+",
#             "\\",
#             "_",
#             "-",
#             ">",
#             "<",
#             "@",
#             "`",
#             ",",
#             "?",
#             "!",
#         ]

#     def evaluate(self, answer, gt_answers):
        
#         answer = answer.replace("\n", " ")
#         answer = answer.replace("\t", " ")
#         answer = answer.strip()
#         answer = self.processPunctuation(answer)
#         answer = self.processDigitArticle(answer)

#         if type(gt_answers)==list:
#             for i in range(len(gt_answers)):
#                 gt_answers[i] = gt_answers[i].replace("\n", " ")
#                 gt_answers[i] = gt_answers[i].replace("\t", " ")
#                 gt_answers[i] = gt_answers[i].strip()
#                 gt_answers[i] = self.processPunctuation(gt_answers[i])
#                 gt_answers[i] = self.processDigitArticle(gt_answers[i])
#                 if has_word(answer, gt_answers[i]):
#                     return 1
#             return 0
#         else:
#             gt_answers = gt_answers.replace("\n", " ")
#             gt_answers= gt_answers.replace("\t", " ")
#             gt_answers = gt_answers.strip()
#             gt_answers = self.processPunctuation(gt_answers)
#             gt_answers = self.processDigitArticle(gt_answers)

#             if has_word(answer, gt_answers):
#                 return 1
#             else:
#                 return 0

#     def processPunctuation(self, inText):
#         outText = inText
#         for p in self.punct:
#             if (p + " " in inText or " " + p in inText) or (
#                 re.search(self.commaStrip, inText) != None
#             ):
#                 outText = outText.replace(p, "")
#             else:
#                 outText = outText.replace(p, " ")
#         outText = self.periodStrip.sub("", outText, re.UNICODE)
#         return outText

#     def processDigitArticle(self, inText):
#         outText = []
#         tempText = inText.lower().split()
#         for word in tempText:
#             # word = self.manualMap.setdefault(word, word)
#             if word not in self.articles:
#                 outText.append(word)
#             else:
#                 pass
#         for wordId, word in enumerate(outText):
#             if word in self.contractions:
#                 outText[wordId] = self.contractions[word]
#         outText = " ".join(outText)
#         return outText

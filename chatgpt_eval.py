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
from constants import INCONTEXT_PROMPT
from constants import QUESTION_PROMPT
import random




openai.api_key = os.getenv("OPENAI_API_KEY")
parser = argparse.ArgumentParser()

parser.add_argument('--gpt_version', choices=['gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-16k'], default='gpt-3.5-turbo')
parser.add_argument('--input_filepath', type = str, default = "Downloads\Copy of docvqa.csv")
parser.add_argument('--start_index', type = int, default = 0)
parser.add_argument('--no_incontext', type = int, default = 1)
# lets have 0 the default 
parser.add_argument('--incontext_type', type = int, default = 0)
# 0 is in domain, 1 is out of domain


args = parser.parse_args()


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



def get_messages(instruction, incontext_ex, ocr, img_caption, output1, output2):
    j=random.sample(range(1, len(incontext_ex)), args.no_incontext) # len of df
    prompt = RANKINGS_PROMPT
    for n in range(args.no_incontext):
        i=n
        instruction_ic = incontext_ex.iloc[j[i]]['question']
        gt_answer_ic = incontext_ex.iloc[j[i]]['gt_answer']
        ocr_ic = incontext_ex.iloc[j[i]]['ocr']
        img_caption_ic = incontext_ex.iloc[j[i]]['img_caption']
        output1_ic = incontext_ex.iloc[j[i]]['model_a_answer']
        output2_ic = incontext_ex.iloc[j[i]]['model_b_answer']
        label_ic =incontext_ex.iloc[j[i]]['response']
        prompt= "\n".join([prompt, INCONTEXT_PROMPT.format(n=n,instruction_ic=instruction_ic,gt_answer_ic=gt_answer_ic,ocr_ic=ocr_ic,img_caption_ic=img_caption_ic,output1_ic=output1_ic,output2_ic=output2_ic,label_ic=label_ic)])

    prompt1="\n".join([prompt, QUESTION_PROMPT.format(instruction=instruction, ocr=ocr, img_caption=img_caption, output1=output1, output2=output2)])
    message1 = [{"role": "user", "content": prompt1}]

    prompt2="\n".join([prompt, QUESTION_PROMPT.format(instruction=instruction, ocr=ocr, img_caption=img_caption, output1=output2, output2=output1)])
    message2 = [{"role": "user", "content": prompt2}]
    message_list = [message1, message2]

    # print(prompt1)
    return message_list


def main():

    df = pd.read_csv(args.input_filepath)
    df = df.iloc[10:] # 10 index

    '''
    if it is in domain
    we extract 10 ex from that file itself df of 10

    if it is out of domain
    you load the other two files
    then extract 10 samples from each
    combine that into a df of 20 ex

    get_reward(instruction, ...)
    
    '''

    if args.incontext_type == 0:
        incontext_ex = pd.read_csv(args.input_filepath).iloc[:10]

    else:
        common_path = "/".join(args.input_filepath.split("/")[:-1])
        doc_ex = pd.read_csv(os.path.join(common_path, "docvqa_final.csv")).iloc[:10]
        info_ex = pd.read_csv(os.path.join(common_path, "infovqa_final.csv")).iloc[:10]
        st_ex = pd.read_csv(os.path.join(common_path, "stvqa_final.csv")).iloc[:10]

        if "doc" in args.input_filepath:
            incontext_ex = pd.concat([info_ex, st_ex])

        elif "info" in args.input_filepath:
            incontext_ex = pd.concat([doc_ex, st_ex])
            
        elif "st" in args.input_filepath:
            incontext_ex = pd.concat([doc_ex, info_ex])
    
    chatgpt_eval_data = []
    cnt = 0
    for j in tqdm(range(len(df))):

        try:
            instruction = df.iloc[j]['question']
            # input = "" # to be changed
            gt_answer = df.iloc[j]['gt_answer']
            ocr= df.iloc[j]['ocr']
            img_caption= df.iloc[j]['img_caption']
            output1 = df.iloc[j]['model_a_answer']
            output2 = df.iloc[j]['model_b_answer']

            message_list = get_messages(instruction, incontext_ex, ocr, img_caption, output1, output2)
            completion = openai.ChatCompletion.create(
                model = args.gpt_version, 
                messages = message_list[0])
            feedback_1 = completion['choices'][0]['message']['content']
            completion = openai.ChatCompletion.create(
                model = args.gpt_version, 
                messages = message_list[1])
            feedback_2 = completion['choices'][0]['message']['content']

            if '(a)' in feedback_1 and '(b)' in feedback_2:
                feedback = '(a)'
            elif '(b)' in feedback_1 and '(a)' in feedback_2:
                feedback = '(b)'
            elif '(a)' in feedback_1 and '(a)' in feedback_2:
                feedback = '(e)'
            elif '(b)' in feedback_1 and '(b)' in feedback_2:
                feedback = '(e)'
            elif '(c)' in feedback_1 or '(c)' in feedback_2:
                feedback = '(c)'
            else:
                feedback = '(d)'

            print(feedback_1, feedback_2, feedback)
            chatgpt_eval_data.append({
                "question_id":j,
                "instruction":instruction,
                "gt_answer":gt_answer,
                "output_1":output1,
                "output_2":output2,
                "feedback_1":feedback_1,
                "feedback_2":feedback_2,
                "feedback":feedback
            })
        except Exception as E:
            print(f"Exception raised: {E}")
            print('Sleeping...')
            time.sleep(5)
            chatgpt_eval_data.append({
                "question_id":j,
                "instruction":instruction,
                "gt_answer":gt_answer,
                "output_1":output1,
                "output_2":output2,
                "feedback_1":feedback_1,
                "feedback_2":feedback_2,
                "feedback":"NA"
            })

        cnt+=1
        if cnt==100:
            break
        if cnt%15==0:
            print("interval sleeping")
            time.sleep(10)

    dataset_name = args.input_filepath.split('/')[-1].split('.')[0]
    domain_context = "indomain" if args.incontext_type == 0 else "outdomain"
    save_feedback_filepath = f"./course/output/{dataset_name}_{domain_context}_{args.no_incontext}.jsonl"
    dump_jsonl(chatgpt_eval_data, save_feedback_filepath)

if __name__ == '__main__':
    main()



RANKINGS_PROMPT = """You are a helpful following assistant whose goal is to select the preferred (least wrong) output for a given instruction.
Answer the question by printing only a single choice from ["Response (a)", "Response (b)", "Response (c)", "Response (d)"] (without quotes) corresponding to the correct answer with no other text.

## Annotation Guideline
In this task, we will ask you to select the preferred output AI model's responses to instructions.

You will read a examples, which are composed of the following:

1. an Instruction we give to the AI system
2. a Ground Truth Response for the Instruction
3. OCR Text of the image
4. Image Caption
5. The output from the first AI system 
6. The output from the second AI system
7. Answer for the example

You have to select from one of the option
1. Response (a), the output from the First AI system
2. Response (b), the output from the Second AI system
3. Response (c), the output from both AI systems
4. Response (d), the output from both AI systems do not match

Your task is to decide which response is better for each example. 

Accuracy: The output sentence should be factually consistent with the Ground Truth Response.

Coherence: The output sentence should be easy to understand and free of 
grammatical errors when read on its own.

Non-repetitive: DO NOT Prefer long output sentence if it is not factually consistent with the Ground Truth Response.The output sentence by AI system should not be preferred if it repeats the text in the instruction but does not answer the instruction with Accuracy.

In extractive instructions like who, when, count and so on, Please Focus on matching the value of the entity like person, time, number than the actual phrasing of the response.

In summative instructions like summarize, purpose, understand, Please Focus on matching the gist conveyed in Output from First AI system and Output from Second AI system to the Ground Truth Response. 

You do not provide Human Explaination of the answer. Human Explaination only provided in examples to help build your reasoning.

You should answer using only Response (a), Response (b), Response (c) or Response (d)

## Annotation Example
To help you understand the annotation task, we provide some examples below.
I will give an explanation for the correct answer, but you should only answer with the preferred output.

"""

INCONTEXT_PROMPT="""

### Example {n}:

#### Instruction:
{instruction_ic}

#### Ground Truth Response for Example:
{gt_answer_ic}

#### OCR Text of the image for Example:
{ocr_ic}

#### Image Caption for Example:
{img_caption_ic}

#### Output of First AI system for Example:
{output1_ic}

#### Output of Second AI system for Example:
{output2_ic}

#### Answer for Example:
{label_ic}
"""


QUESTION_PROMPT="""
Now give me answer for this test question.

## Test Question 

### Instruction for Test Question :
{instruction}

#### OCR Text of the image for Test Question 
{ocr}

#### Image Caption for Test Question 
{img_caption}

### Output of First AI system for Test Question:
{output1}

### Output of Second AI system for Test Question :
{output2}

## Answer for Test Question:
"""

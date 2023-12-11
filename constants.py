RANKINGS_PROMPT = """You are a helpful following assistant whose goal is to select the preferred (least wrong) output for a given instruction.
Answer the question by printing only a single choice from ["Response (a)", "Response (b)", "Response (c)", "Response (d)"] (without quotes) corresponding to the correct answer with no other text.

## Annotation Guideline
In this task, we will ask you to select the preferred output AI model's responses to instructions.

You will read a examples, which are composed of the following:

1. An Visual Question Answering instruction given to the AI system
2. An OCR Text of the Image
3. An Image Caption of the Image
4. The output from the first AI system 
5. The output from the second AI system
6. Answer for the example

Additionally you will be given the ground truth for the examples to understand the task.

You have to select from one of the option
1. Response (a), the output from the First AI system
2. Response (b), the output from the Second AI system
3. Response (c), the output from both AI systems are equally good
4. Response (d), the output from both AI systems are equally bad or insufficient visual information

Your task is to decide which response is better for each example. 

Accuracy: The output sentence should be factually consistent with the Ground Truth Response.

Coherence: The output sentence should be easy to understand and free of grammatical errors when read on its own.

Non-repetitive: DO NOT Prefer if AI system repeats the text in the instruction but does not answer the instruction with Accuracy.

Factuality: Please Focus on matching the value of the entity like person, time, number than the actual phrasing of the response.

You should answer using only Response (a), Response (b), Response (c) or Response (d).

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
Now give me answer for this Test Example.

## Test Example

### Instruction for Test Example:
{instruction}

#### OCR Text of the image for Test Example:
{ocr}

#### Image Caption for Test Example:
{img_caption}

### Output of First AI system for Test Example:
{output1}

### Output of Second AI system for Test Example:
{output2}

## Answer for Test Example:
"""

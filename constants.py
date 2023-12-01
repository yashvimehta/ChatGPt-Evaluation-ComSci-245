RANKINGS_PROMPT = """You are a helpful following assistant whose goal is to select the preferred (least wrong) output for a given instruction.
Answer the question by printing only a single choice from ["Response (a)", "Response (b)", "Response (c)"] (without quotes) corresponding to the correct answer with no other text.

## Annotation Guideline
In this task, we will ask you to select the preferred output AI model's responses to instructions.

You will read a examples, which are composed of the following:

1. an Instruction we give to the AI system
2. OCR Text of the image
3. a Ground Truth Response for the Instruction
4. The output from the first AI system 
5. The output from the second AI system

You have to select from one of the option
1. Response (a), the output from the First AI system
2. Response (b), the output from the Second AI system
3. Response (c), the output from both AI systems

Your task is to decide which response is better for each example. 

Accuracy: The output sentence should be factually consistent with the Ground Truth Response.

Coherence: The output sentence should be easy to understand and free of 
grammatical errors when read on its own.

Non-repetitive: DO NOT Prefer long output sentence if it is not factually consistent with the Ground Truth Response.The output sentence by AI system should not be preferred if it repeats the text in the instruction but does not answer the instruction with Accuracy.

In extractive instructions like who, when, count and so on, Please Focus on matching the value of the entity like person, time, number than the actual phrasing of the response.

In summative instructions like summarize, purpose, understand, Please Focus on matching the gist conveyed in Output from First AI system and Output from Second AI system to the Ground Truth Response. 

You do not provide Human Explaination of the answer. Human Explaination only provided in examples to help build your reasoning.

You should answer using only Response (a), Response (b) or Response (c)

## Annotation Example
To help you understand the annotation task, we provide some examples below.
I will give an explanation for the correct answer, but you should only answer with the preferred output.

### Example 1

#### Instruction 1:

#### OCR Text of the image

#### Ground Truth Response 1:

#### Output of First AI system for Example 1:

#### Output of Second AI system for Example 1:

#### Answer for Example 1:
Response (a)

#### Human Explaination for Example 1: Indeed, Response (a) as ....

## Example n+1

### Instruction n+1:
{instruction}

#### Ground Truth Response n+1:
{gt_answer}

### Output of First AI system for Example n+1:
{output_1}

### Output of Second AI system for Example n+1:
{output_2}

## Answer for example n+1:
"""
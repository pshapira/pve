import pickle as pkl
import pandas as pd
import random
import openai
import copy

openai.api_key = "<ENTER YOUR OWN API KEY HERE>"

def generate_text(prompt, n = 1): # n is the number of responses you want to generate
    model_engine = 'gpt-4' # gpt-3.5-turbo for GPT-3.5, which is 10 times cheaper than GPT-4, but with lesser capabilities
    completions = openai.ChatCompletion.create(
        model = model_engine,
        messages = prompt,
        max_tokens = 1000, # maximum number of tokens you want the model to generate
        n = n,
        temperature = 0.2, # randomness of the output
    )
    message = completions.choices[0]
    return message

def prompt_gpt3(prompt_text):
    prompt = prompt_text
    generated_text = generate_text(prompt)
    return generated_text

starting_prompt = [
  {"role": "system", "content": "You are a helpful assistant that categorizes the sentences into 'Public Value Expression' or 'No Public Value'. If the sentence is categorized as 'Public Value Expression', further classify it into 'Direct PVE' or 'Contextual PVE'. Use the following definitions:\n\n\
  Public Value Expression: A public value expression (PVE) is one that indicates societal benefits promised to or for people, organizations, or ecosystems.  Societal benefits for people includes, among other aspects, potential enhancement of safety, security, privacy, justice, equality, human rights, civil liberties, health, and avoidance of bias and discrimination. Social benefits generated at the organizational level include, among other aspects, enhancements in accountability, transparency, honesty, responsibility and security which are not purely pecuniary and that create shared utility for users and networks. Societal benefits for ecosystems include, among other aspects, enhancements to sustainability, nature and the environment. Enhancement includes both positive improvement and the mitigation or prevention of adverse conditions.\n\n\
  No Public Value: Do not code a sentence as a 'Public Value Expression' if it only refers to information technology or other technical aspects without any explicit indication of broader societal benefits. Do not code a sentence as 'Public Value Expression' if its benefits present only as accruing to the assignee organization (private value) without any explicit indication of broader societal benefit. Absent such explicit indication, do not code a sentence as 'Public Value Expression' by generalizing from private value to public value based on inferences (by the assistant) about potential connections. Avoid assumptions or inferences about potential positive or negative societal, economic, or environmental spillovers that are not explicitly stated. Furthermore, do not code a sentence as 'Public Value Expression' if it only refers to improving user experience. User experience enhancement does not imply Public Value Expression. User experience enhancement focuses on individual users, is narrow in scope and individualistic, and is measured with usability metrics (e.g., task completion, user satisfaction). PVE focuses on society as a whole, is broader in scope and societal, and is measured with social impact metrics (e.g., environmental impact, social justice, democratic participation).\n\n\
  Direct PVE: Code a sentence as a 'Direct PVE' if the sentence states that the invention being patented explicitly addresses one or more PVEs (see definition of public value expression).\n\n\
  Contextual PVE: Code a sentence as a 'Contextual PVE' if the sentence mentions a contextual situation that allows us to infer a concern or intention to create or protect PVEs. The sentence must be explicit in its reference to a public value or concern about a societal, environmental, or ethical concern. However, it is contextual because it is not explicitly connected to the invention being patented."},
  
  {"role": "user", "content": "an inventive solution to the need to prevent private information inferencing from document collections is presented."},
  {"role": "assistant", "content": "Let's think step by step. The sentence highlights the importance of preventing the inference of private information from document collections, which is a critical aspect of enhancing privacy, safety, and security for individuals. This directly aligns with the societal benefits outlined in the guidelines. Furthermore, the sentence clarifies that the patented invention offers an innovative solution to this issue, as evidenced by the segment stating 'an inventive solution to the...'.\nBased on these considerations, I would categorize this sentence as: PVE, Direct PVE."},

  {"role": "user", "content": "a disease risk prediction method according to the present invention includes: predicting a development risk of an infectious disease using a prediction model for predicting a development status of the infectious disease, the prediction model being learned based on electronic data of a patient; and outputting the predicted development risk"},
  {"role": "assistant", "content": "Let's think step by step. The sentence clearly states that the invention being patented addresses the need for disease risk prediction, which falls under the potential enhancement of health for individuals. The segment of the sentence that says 'a disease risk prediction method according to the present invention' identifies that the patented invention is the one addressing this issue.\nBased on these considerations, I would categorize this sentence as: PVE, Direct PVE."},

  {"role": "user", "content": "yet another object of the disclosure is to provide a system and method to characterize risk of occupational health hazards and implement control measures to protect workers, with real time evaluations of environmental conditions and exposure concentrations that provides a guide through a task exposure risk assessment."},
  {"role": "assistant", "content": "Let's think step by step. The sentence clearly states that the invention being disclosed aims to improve occupational health by characterizing risks and implementing control measures to protect workers. This aligns with the guidelines' definition of potential enhancements in health, as well as accountability or security that benefit users and networks beyond monetary gain. Therefore, the invention promises a societal benefit for individuals and organizations. We can identify the patented invention as the one addressing this issue, as indicated by the segment of the sentence that reads 'yet another object of the disclosure is to provide a system and method to…'.\nBased on these considerations, I would categorize this sentence as: PVE, Direct PVE."},

  {"role": "user", "content": "brief description of the disclosure  in one aspect, a computer-implemented method for selecting participants from an applicant pool to participate in a program to exit poverty is described"},
  {"role": "assistant", "content": "Let's think step by step. The sentence describes a computer-based method for selecting participants from an applicant pool to exit poverty, which is a societal benefits for individuals and organizations. The invention is explicitly identified as addressing this issue, as the sentence begins with a brief description of the disclosure and then explains how the invention benefits society.\nBased on these considerations, I would categorize this sentence as: PVE, Direct PVE."},

  {"role": "user", "content": "Social robots may be used to augment teaching and may have particular efficacy in working with autistic children as well as in providing companionship to elderly persons who live alone"},
  {"role": "assistant", "content": "Let's think step by step. The sentence is explicit in its reference to a public value, which is the potential benefit to both autistic children and elderly people who live alone. The sentence suggests that the use of social robots can enhance teaching and provide companionship to these two vulnerable groups. Therefore, the sentence indicates a concern for the enhancement of the quality of life and well-being of individuals who are otherwise disadvantaged or isolated. However, the connection between the patented invention and public value is not explicit in the sentence.\nBased on these considerations, I would categorize this sentence as: PVE, Contextual PVE."},

  {"role": "user", "content": "such an enabled machine would be of an immense assistance to the development of human civilization much further and much faster leading to abundance, economic prosperity, biological and mental health, and well-being of society"},
  {"role": "assistant", "content": "Let's think step by step. The sentence is explicit in its reference to a public value, which is the potential benefit to society as a whole, including abundance, economic prosperity, biological and mental health, and well-being. The sentence suggests that an enabled machine could significantly contribute to the development of human civilization, leading to broad societal benefits. However, the connection between the patented invention and public value is not explicit in the sentence. \nBased on these considerations, I would categorize this sentence as: PVE, Contextual PVE."},

  {"role": "user", "content": "The natural ecology of many aquatic environments around the world is under threat due to human activity, climate change, and other sources."},
  {"role": "assistant", "content": "Let's think step by step. The sentence highlights the potential danger that human activity, climate change, and other sources pose to the natural ecology of aquatic environments globally. While it does not explicitly mention any actions or intentions to address this threat, the sentence conveys a sense of concern for the well-being of ecosystems.\nBased on these considerations, I would categorize this sentence as: PVE, Contextual PVE."},

  {"role": "user", "content": "malicious network information has seriously impacted and threatened individuals, enterprises and even countries, as well as safety and social public interests."},
  {"role": "assistant", "content": "Let's think step by step.The impact of malicious network information on individuals, enterprises, and even countries highlights the need to protect safety and social public interests. Although the sentence does not specify any particular actions or intentions to address this concern, it implies a recognition of the importance of safeguarding the safety and security of individuals and society.\nBased on these considerations, I would categorize this sentence as: PVE, Contextual PVE."},

  {"role": "user", "content": "in some embodiments, the first sensor collects a real-time actual environmental condition at the first location of interest as the first source of sensor data, and the second sensor collects information that is a possible impact on the first source of sensor data."},
  {"role": "assistant", "content": "Let's think step by step. The sentence describes the technical aspects of an invention, specifically the use of two sensors to collect data, but it does not explicitly or implicitly mention any broader societal benefits. It only discusses the specific function of the two sensors and their relationship to each other, without indicating any public values.\nBased on these considerations, I would categorize this sentence as: No Public Value."},

  {"role": "user", "content": "on the other hand, human computer interfaces are not based on subtle human skills and are therefore cumbersome and unintuitive when compared to human spoken language and body language."},
  {"role": "assistant", "content": "Let's think step by step. The sentence discusses the limitations of human-computer interfaces in comparison to human communication, highlighting that interfaces are not based on subtle human skills and are therefore cumbersome and unintuitive. While this may imply a need for improvement in the user experience, it does not explicitly or implicitly relate to any public values or benefits. User experience enhancement do not imply public value.\nBased on these considerations, I would categorize this sentence as: No Public Value."},

  {"role": "user", "content": "at times, data obtained from historical analytics may be applied to existing enterprise software systems, in order to ensure that operational activities of organizations are optimized to generate better results and minimize risk."},
  {"role": "assistant", "content": "Let's think step by step. This sentence is about a technology used to improve business performance. It is not possible to infer from this that the technology also contributes to public value. As far as the sentence conveys, value creation is limited to the enterprise user.\nBased on these considerations, I would categorize this sentence as: No Public Value."},

  {"role": "user", "content": "further, a good understanding of the labor market may assist a company deciding where to establish a new site because the company may choose a site with a readily-available workforce"},
  {"role": "assistant", "content": "Let's think step by step. Something, perhaps a technology, helps the firm understanding the labor market. Such understanding assists the firm in its location decision. The only value reflected in the content of the sentence is that created for the firm. We cannot infer any public value from the sentence.\nBased on these considerations, I would categorize this sentence as: No Public Value."},

  {"role": "user", "content": "however, since types and strength of sensory effects desired by individual users may vary according to their user type which can be categorized by the user's gender, age, body, illness, and the like; current health state and mental state of the user; or a play environment (at dawn, an indoor or outdoor environment) of the sensory effects, standardized services which do not take into account the user preference cannot satisfy the user's requirements for experiencing diverse sensory effects."},
  {"role": "assistant", "content": "Let's think step by step. The sentence discusses the customization of sensory effects based on user preferences, which is related to user experience enhancement. However, there is no explicit mention of broader societal benefits or public values, such as sustainability, social justice, or civil liberties. Additionally, the focus is on individual users and their preferences, rather than society as a whole.\nBased on these considerations, I would categorize this sentence as: No Public Value."},

  {"role": "user", "content": "for example, if a user enters, via a user interface, a command for the autonomous floor cleaning system to 'clean kitchen,' without the user being able to confirm via a rendering of the environment that the autonomous floor cleaning system knows where the kitchen is, the autonomous floor cleaning system may clean the wrong part of the environment or otherwise misunderstand the command."},
  {"role": "assistant", "content": "Let's think step by step. While the sentence discusses a potential problem with the autonomous floor cleaning system's understanding of user commands, it primarily focuses on the individual user's experience and does not explicitly or implicitly reference broader societal benefits.\nBased on these considerations, I would categorize this sentence as: No Public Value."}

]

# read a csv file names random_100.csv and convert it to a pandas dataframe
df = pd.read_csv('10k_sententnces_to_annotate.csv')
# convert the column 'sent' to a list
sent_list = df['sent'].tolist()

# open a pikcle file in the append mode
f = open('10k_responses_gpt4.pkl', 'ab')

#  set random seed and shuffle the list
random.seed(42)
random.shuffle(sent_list)

count = 0
for sent in sent_list:
    # copt the starting prompt to a new variable
    curr_prompt = copy.deepcopy(starting_prompt)
    print(len(curr_prompt))
    curr_prompt.append({"role": "user", "content": sent})
    response = prompt_gpt3(curr_prompt)
    content = response["message"]["content"].strip()
    try:
        rationale = content.split("\nBased on these considerations,")[0].replace("Let's think step by step. ", "")
        label = content.split("\nBased on these considerations, I would categorize this sentence as:")[1].strip().replace(".", "")
    except IndexError: # handing of cases where GPT-4 generates a non-standard response
        rationale = "non-standard response (overwritten)"
        label = "non-standard response (overwritten)"
    pkl.dump([sent, rationale, label], f)
    print(count, " out of ", len(sent_list), " done")
    count += 1

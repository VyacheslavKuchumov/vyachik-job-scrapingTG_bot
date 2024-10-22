import ollama

qwen = 'qwen2.5-coder:7b'
mistral_nemo = "mistral-nemo:12b"

# response = ollama.chat(model=mistral_nemo, messages=[
# {
# 'role': 'user',
# 'content': 'Why is the sky blue?',
# },
# ])
#
# print(response['message']['content'])

jobNames = ["Врач терапевт", "Програмист на python"]

jobGroups = ["Врачи", "Програмисты"]
baseTask = "You have to assign a group to the job offer only by knowing it's name. ONLY answer with a group name. "

for i in range(len(jobNames)):
    promptik = f"{baseTask}\nDATA: job_offer_name={jobNames[i]} \njob_groups={jobGroups}"
    response = ollama.generate(model=mistral_nemo, prompt=promptik)
    print(jobNames[i], response['response'], sep=": ")

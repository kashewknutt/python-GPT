from openai import OpenAI
client = OpenAI(
    api_key='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'
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
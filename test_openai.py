from openai import OpenAI

client = OpenAI(api_key="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")

print(client.embeddings.create(
    model="text-embedding-3-small",
    input="test"
).data[0].embedding[:5])

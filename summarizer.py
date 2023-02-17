import openai
import os
openai.api_key = "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"
prompt = "ENTER TEXT HERE"

openai.Completion.create(
    model = "text-davinci-003",
    prompt = prompt,
    temperature = 1,
    max_tokens = 1000,
)
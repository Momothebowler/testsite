import os
import openai
import time

time.sleep(20)

openai.api_key = "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"

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "What ETF tickers are similar to the tickers SPY, AMZN, and AAPL and can you put - to the left AND right of the similar ETF tickers?",
        }
    ],
)

print(completion.choices[0].message.content)
for i in range(len(completion.choices[0].message.content.split("-"))):
    if i % 2 == 0:
        print(completion.choices[0].message.content.split("-")[i])

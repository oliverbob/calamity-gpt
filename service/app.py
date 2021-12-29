from flask import Flask, request, jsonify
import time

from transformers import pipeline, set_seed, GPT2Tokenizer
model_name = 'gpt2-xl'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
generator = pipeline('text-generation', model=model_name)
set_seed(int(time.time()))

def infer(prompt, tokens_count, num_sequences):
    input_tokens = len(tokenizer(prompt)['input_ids'])
    seqs = generator(prompt,
            max_length=input_tokens + tokens_count,
            num_return_sequences=num_sequences)
    return jsonify([seq['generated_text'] for seq in seqs])

app = Flask(__name__)

@app.route('/generate/', methods=['POST'])
def generate():
    params = request.get_json(force=True)
    # TODO: error handling
    return infer(params.get('text'), params.get('tokens', 10), params.get('n', 1))


# Copyright 2022 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     https://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import functions_framework  # Import the functions_framework library for HTTP functions
import vertexai  # Import the vertexai library for AI model handling
from vertexai.preview.language_models import TextGenerationModel  # Import the TextGenerationModel from vertexai
import json  # Import the JSON library for working with JSON data

PROJECT_ID  = os.environ.get('GCP_PROJECT','-')
LOCATION = os.environ.get('GCP_REGION','-')

# Define an HTTP function using the functions_framework library
@functions_framework.http
def text_summarizer(request):
    request_json = request.get_json(silent=True)

    if request_json and 'inputText' in request_json:
        inputText = request_json['inputText']

        # Process and clean the input data
        parsed_data = (str(inputText)).replace('"', "").replace("'", "").replace(",", "").replace("\n", "")
        print(f"Received request for inputText: {inputText}")

        vertexai.init(project=PROJECT_ID)
        model = TextGenerationModel.from_pretrained("text-bison@001")
        parameters = {
            "temperature": 0.2, # Control the randomness of the generated text
            "max_output_tokens": 256, # Limit the maximum number of output tokens
            "top_p": 0.8, # Set a nucleus sampling threshold
            "top_k": 40 # Set a top-k sampling threshold
        }
        summary_response = model.predict(f"Make a short summary : {parsed_data}",**parameters)
        print(f"PaLM Text Bison Model response: {summary_response.text}")
    else:
        summary_response = 'No text provided.'

    return json.dumps({"response_text":summary_response.text})

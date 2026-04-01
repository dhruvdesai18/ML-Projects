# from flask import Flask, request, jsonify, render_template
# import base64
# import os
# import json # Import json module for parsing the AI response
# import re

# # Assuming your generate function is here or imported from another file
# from google import genai
# from google.genai import types

# def generate(audio_base64_string):
#     client = genai.Client(
#         vertexai=True,
#         project="trycatch-project-465608",
#         location="global",
#     )

#     msg1_audio1 = types.Part.from_bytes(
#         data=base64.b64decode(audio_base64_string),
#         mime_type="audio/x-m4a",
#     )
#     si_text1 = """You are an Audio Diarizer or an Audio Transcriber.
# Identify the type of people speaking what is their role, etc and give labels to them accordingly.
# Return the exact conversation language it is in the audio but use english letters only. Also perform the sentiment analysis across the conversation. Write a summary in not more than 200 words explaining the conversation. Also provide the possible solution to the problem faced by the speakers in the audio in just one line. The output should be in JSON format (Conversation, Summary, Sentiment, Solution), and returns only what it is asked for."""

#     model = "gemini-2.5-flash"
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 msg1_audio1,
#                 types.Part.from_text(text="""Transcribe the audio""")
#             ]
#         ),
#     ]

#     generate_content_config = types.GenerateContentConfig(
#         temperature=0.2,
#         top_p=1,
#         seed=0,
#         max_output_tokens=65535,
#         safety_settings=[
#             types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
#             types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
#             types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
#             types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
#         ],
#         system_instruction=[types.Part.from_text(text=si_text1)],
#         thinking_config=types.ThinkingConfig(thinking_budget=-1),
#     )

#     full_response = ""
#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     ):
#         full_response += chunk.text
#     try:
#         # Remove markdown backticks if present in the AI's response
#         cleaned_response = re.sub(r"```json|```", "", full_response).strip()
        
#         print("yahayahwhshshwb111111111!!!!!", cleaned_response)
#         # response_added = json.loads(cleaned_response)
#         # print("@@@@@     @@@@@@", response_added)
#         return cleaned_response
#         # return json.loads(cleaned_response)
#     except json.JSONDecodeError:
#         print(f"Failed to parse JSON response: {full_response}") # Log the raw response for debugging
#         return {"error": "Failed to parse JSON response from AI model", "raw_response": full_response}


# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # This would temporarily store the processed data after an upload
# # In a real application, consider a more robust session management or database
# processed_audio_data = {}

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_audio():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No audio file provided"}), 400

#     audio_file = request.files['audio']
#     if audio_file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     if audio_file:
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
#         audio_file.save(file_path)

#         with open(file_path, 'rb') as f:
#             audio_raw = f.read()
#         audio_base64 = base64.b64encode(audio_raw).decode('utf-8')

#         # Process the audio
#         global processed_audio_data
#         result = generate(audio_base64)
#         result_added = json.loads(result)
#         print("@#@#@#@#@#@#@    #@#@#@#@#@#@", result_added)
#         print(result)
#         if "error" in result:
#             return jsonify(result), 500 # Return error from AI model processing
#         processed_audio_data = result_added
#         return jsonify({"message": "Audio processed successfully", "data_available": True})

# @app.route('/get_data/<data_type>', methods=['GET'])
# def get_data(data_type):
#     global processed_audio_data
#     if not processed_audio_data:
#         return jsonify({"error": "No audio processed yet. Please upload an audio file first."}), 404

#     if data_type == 'conversation':
#         # Return the entire conversation dictionary
#         return jsonify({"Conversation": processed_audio_data.get("Conversation")})
#     elif data_type == 'summary':
#         return jsonify({"Summary": processed_audio_data.get("Summary")})
#     elif data_type == 'sentiment':
#         return jsonify({"Sentiment": processed_audio_data.get("Sentiment")})
#     elif data_type == 'solution':
#         return jsonify({"Solution": processed_audio_data.get("Solution")})
#     else:
#         return jsonify({"error": "Invalid data type"}), 400



# if __name__ == '__main__':
#     # It's good practice to set a secret key for session management in production,
#     # though not strictly necessary for this simple example.
#     # app.secret_key = 'your_secret_key_here'
#     app.run(debug=True) # debug=True enables auto-reloading and helpful error messages




##########



from flask import Flask, request, jsonify, render_template
import base64
import os
import json # Import json module for parsing the AI response

# Assuming your generate function is here or imported from another file
from google import genai
from google.genai import types

def generate(audio_base64_string):
    client = genai.Client(
        vertexai=True,
        project="trycatch-project-465608",
        location="global",
    )

    msg1_audio1 = types.Part.from_bytes(
        data=base64.b64decode(audio_base64_string),
        mime_type="audio/x-m4a",
    )

    # --- UPDATED SYSTEM INSTRUCTION FOR CONVERSATION FORMAT ---
    si_text1 = """You are an Audio Diarizer or an Audio Transcriber.
Identify the type of people speaking what is their role, etc and give labels to them accordingly.
Return the exact conversation language it is in the audio but use English letters only.
Also perform the sentiment analysis across the conversation.
Write a summary in not more than 200 words explaining the conversation.
Also provide the possible solution to the problem faced by the speakers in the audio in just one line.

The output should be in JSON format with the following structure:
{
  "Conversation": [
    {"Speaker": "Speaker 1 (Role)", "Message": "First utterance by Speaker 1"},
    {"Speaker": "Speaker 2 (Role)", "Message": "First utterance by Speaker 2"},
    {"Speaker": "Speaker 1 (Role)", "Message": "Second utterance by Speaker 1"},
    // ... continue for all turns of conversation
  ],
  "Summary": "...",
  "Sentiment": "...",
  "Solution": "..."
}
Return only the JSON output and nothing else.
"""
    # --- END UPDATED SYSTEM INSTRUCTION ---

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                msg1_audio1,
                types.Part.from_text(text="""Transcribe the audio""")
            ]
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=1,
        seed=0,
        max_output_tokens=65535,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
        ],
        system_instruction=[types.Part.from_text(text=si_text1)],
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
    )

    full_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        full_response += chunk.text
    try:
        # Remove markdown backticks if present in the AI's response
        cleaned_response = full_response.replace("```json\n", "").replace("\n```", "")
        parsed_json = json.loads(cleaned_response)
        print(parsed_json)
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        print(f"Raw AI response:\n{full_response}") # Log the raw response for debugging
        return {"error": "Failed to parse JSON response from AI model", "raw_response": full_response}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

processed_audio_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if audio_file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(file_path)

        with open(file_path, 'rb') as f:
            audio_raw = f.read()
        audio_base64 = base64.b64encode(audio_raw).decode('utf-8')

        global processed_audio_data
        result = generate(audio_base64)
        if "error" in result:
            return jsonify(result), 500 # Return error from AI model processing
        processed_audio_data = result
        return jsonify({"message": "Audio processed successfully", "data_available": True})

@app.route('/get_data/<data_type>', methods=['GET'])
def get_data(data_type):
    global processed_audio_data
    if not processed_audio_data:
        return jsonify({"error": "No audio processed yet. Please upload an audio file first."}), 404

    if data_type == 'conversation':
        # Now returns a list of dictionaries
        return jsonify({"Conversation": processed_audio_data.get("Conversation")})
    elif data_type == 'summary':
        return jsonify({"Summary": processed_audio_data.get("Summary")})
    elif data_type == 'sentiment':
        return jsonify({"Sentiment": processed_audio_data.get("Sentiment")})
    elif data_type == 'solution':
        return jsonify({"Solution": processed_audio_data.get("Solution")})
    else:
        return jsonify({"error": "Invalid data type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
from openai import OpenAI
import re
import uuid

client = OpenAI()

def get_openai_response(messages):

    # Append the new user message to the messages list
    
    # Get the response from OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Extract the model's message from the response

    model_message = response.choices[0].message.content

    return model_message



def split_text_by_language(text):
    # Regular expressions to match Arabic, English, and punctuation
    arabic_pattern = r'[\u0600-\u06FF0-9\s.,;!?]+'
    english_pattern = r'''[a-zA-Z0-9\s.,;!?']+'''


    segments = []

    # Use a pointer to keep track of where we are in the text
    pointer = 0

    while pointer < len(text):
        # Check for Arabic segment
        arabic_match = re.search(arabic_pattern, text[pointer:])
        # Check for English segment
        english_match = re.search(english_pattern, text[pointer:])

        # If we find an Arabic segment and it comes before any English segment, append it
        if arabic_match and (not english_match or arabic_match.start() <= english_match.start()):
            segments.append(('arabic', arabic_match.group().strip()))
            pointer += arabic_match.end()
        # Otherwise, append the English segment
        elif english_match:
            segments.append(('english', english_match.group().strip()))
            pointer += english_match.end()
        else:
            # Move the pointer forward if no matches are found
            pointer += 1

    return segments

def combine_text_by_language(segments):
    segments_combined = []
    for segmant in segments:
        if len(segments_combined) == 0:
            segments_combined.append(segmant)
        else:
            if segments_combined[-1][0] == segmant[0]:
                segments_combined[-1] = (segments_combined[-1][0], segments_combined[-1][1] + " " + segmant[1])
            else:
                segments_combined.append(segmant)

    return segments_combined

def convert_audio_text(audio_path, language='', prompt=''):
    # use OPENAI API to convert audio to text
    file = open(audio_path, "rb")
    print('file', file)
    transcript = client.audio.transcriptions.create(model="whisper-1", file=file, response_format="text", language=language, prompt=prompt)
    return transcript

def convert_text_audio(text):
    # use OPENAI API to convert text to audio
    print('hhh', text)
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text,
    )

    file_name = str(uuid.uuid4()) + ".mp3"
    response.stream_to_file(file_name)
    return file_name

    
import streamlit as st
import pandas as pd
import speech_recognition as sr
from pydub import AudioSegment

st.title("Speech Recognition and Word Analysis")
st.write("Upload a .wav audio file")

uploaded_file = st.file_uploader("Drag and drop file here", type=["wav"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    audio_file_path = "uploaded_audio.wav"
    with open(audio_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # Convert the file to PCM WAV format
        audio = AudioSegment.from_wav(audio_file_path)
        audio.export("converted_audio.wav", format="wav", parameters=["-acodec", "pcm_s16le"])
        converted_audio_path = "converted_audio.wav"

        # Measure audio duration using pydub
        duration_seconds = len(audio) / 1000.0
        st.write(f"Audio duration (pydub): {duration_seconds:.3f} seconds")

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Load audio file for speech recognition
        with sr.AudioFile(converted_audio_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
            audio_data = recognizer.record(source)

        # Recognize speech using Google Speech Recognition
        result = recognizer.recognize_google(audio_data)
        st.write("Recognized text:", result)

        # Process text: split, count unique words, etc.
        result_str = result.split()
        unique_words = set(result_str)
        word_dict = {word: result_str.count(word) for word in unique_words}

        count_df = pd.DataFrame.from_dict(word_dict, orient='index', columns=['Repetition']).reset_index().rename(columns={'index': 'Word'})
        st.dataframe(count_df)

        # Summary
        st.write("Total number of words:", len(result_str))
        st.write(f"Total length of audio: {duration_seconds:.3f} seconds")
        st.write(f"Total number of words spoken per minute: {len(result_str) / (duration_seconds / 60):.2f}")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

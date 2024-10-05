import streamlit as st
import pandas as pd
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment

# Streamlit app title
st.title("Speech Recognition and Word Analysis")

# Upload the audio file
audio_file = st.file_uploader("Upload a .wav audio file", type=["wav"])

if audio_file is not None:
    # Load the audio file
    audio_file_path = audio_file.name

    # Measure audio duration using pydub
    audio = AudioSegment.from_wav(audio_file)
    duration_seconds = len(audio) / 1000.0  # Convert milliseconds to seconds
    st.write(f"Audio duration (pydub): {duration_seconds:.3f} seconds")

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file for speech recognition
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
        audio_data = recognizer.record(source)  # Read the entire audio file

    # Recognize speech using Google Speech Recognition
    try:
        result = recognizer.recognize_google(audio_data)
        st.write("### Recognized text:")
        st.write(result)
    except sr.UnknownValueError:
        st.write("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")

    if result:
        # Split the recognized text into words
        result_str = result.split()
        st.write("### Words in the text:")
        st.write(result_str)

        # Find unique words
        unique_words = set(result_str)
        st.write(f"### Unique words ({len(unique_words)}):")
        st.write(unique_words)

        # Count occurrences of each word
        word_dict = {word: result_str.count(word) for word in unique_words}
        st.write("### Word count:")
        st.write(word_dict)

        # Create a DataFrame for word repetition
        count_df = pd.DataFrame.from_dict(word_dict, orient='index', columns=['Repetition'])
        count_df = count_df.reset_index().rename(columns={'index': 'Word'})

        # Display the DataFrame
        st.write("### Word Repetition DataFrame:")
        st.dataframe(count_df)

        # Summary
        st.write("### Summary:")
        st.write(f"Total number of words: {len(result_str)}")
        st.write(f"Total length of audio: {duration_seconds:.3f} seconds ({duration_seconds / 60:.2f} minutes)")
        st.write(f"Total number of words spoken per minute: {len(result_str) / (duration_seconds / 60):.2f}")

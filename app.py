import streamlit as st
from pytube import YouTube
import os
import base64

def download_video(url, download_type):
    try:
        yt = YouTube(url)
        if download_type == "Video (MP4)":
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        elif download_type == "Audio (MP3)":
            stream = yt.streams.filter(only_audio=True).first()
        
        output_file = stream.download()
        
        if download_type == "Audio (MP3)":
            base, ext = os.path.splitext(output_file)
            new_file = base + '.mp3'
            os.rename(output_file, new_file)
            output_file = new_file
        
        return output_file
    except Exception as e:
        return str(e)

# Streamlit app
st.title("YouTube Downloader")

# Input URL
video_url = st.text_input("Paste YouTube URL here:")

# Select download type
download_type = st.radio("Select download type:", ("Video (MP4)", "Audio (MP3)"))

if st.button("Download"):
    if not video_url:
        st.error("Please paste a YouTube URL.")
    else:
        file_path = download_video(video_url, download_type)
        if not os.path.exists(file_path):
            st.error(f"Error: {file_path}")
        else:
            with open(file_path, "rb") as file:
                btn = st.download_button(
                    label="Click here to download",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4" if download_type == "Video (MP4)" else "audio/mp3"
                )
            os.remove(file_path)

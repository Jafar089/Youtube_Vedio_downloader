import streamlit as st
from pytube import YouTube
import os

def download_video(url, folder, download_type):
    try:
        yt = YouTube(url)
        if download_type == "Video (MP4)":
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            stream.download(folder)
        elif download_type == "Audio (MP3)":
            stream = yt.streams.filter(only_audio=True).first()
            file_path = stream.download(output_path=folder)
            base, ext = os.path.splitext(file_path)
            new_file = base + '.mp3'
            os.rename(file_path, new_file)
        return True
    except Exception as e:
        return str(e)

# Streamlit app
st.title("YouTube Downloader")

# Input URL
video_url = st.text_input("Paste YouTube URL here:", key="video_url")

# Select download type
download_type = st.radio("Select download type:", ("Video (MP4)", "Audio (MP3)"), key="download_type")

# Function to get default download path
def get_default_download_path():
    if os.name == 'nt':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

# Browse and select download folder
download_folder = st.text_input("Download folder path:", value=get_default_download_path(), key="download_folder")

if st.button("Set to Downloads Folder"):
    download_folder = get_default_download_path()
    st.text_input("Download folder path:", value=download_folder, key="download_folder_set")

if st.button("Download"):
    if not video_url:
        st.error("Please paste a YouTube URL.")
    else:
        result = download_video(video_url, download_folder, download_type)
        if result is True:
            st.success("Your video/audio downloaded successfully!")
        else:
            st.error(f"Error: {result}")

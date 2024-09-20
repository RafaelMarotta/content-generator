from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from moviepy.audio.fx import audio_loop

def add_background_music(video_path, music_path, output_path, music_volume=0.3):
    """
    Adds a background music track to a video, setting the music volume to 30%.

    Parameters:
    - video_path (str): Path to the input video file.
    - music_path (str): Path to the background music file (MP3).
    - output_path (str): Path where the output video will be saved.
    - music_volume (float, optional): Volume level for the background music (0.0 to 1.0). Default is 0.3 (30%).
    """
    try:
        # Load the video file
        video = VideoFileClip(video_path)
        print(f"Video loaded: {video.duration} seconds.")

        # Load the background music file
        music = AudioFileClip(music_path).volumex(music_volume)
        print(f"Background music loaded: {music.duration} seconds with volume set to {music_volume * 100}%.")

        # Ensure the music duration matches the video duration
        if music.duration < video.duration:
            # Loop the music to match the video duration
            music = audio_loop(music, duration=video.duration)
            print(f"Background music looped to match video duration of {video.duration} seconds.")
        else:
            # Trim the music to match the video duration
            music = music.set_duration(video.duration)
            print(f"Background music trimmed to match video duration of {video.duration} seconds.")

        # Combine the original audio with the background music if the video has audio
        if video.audio:
            print("Original audio found in video. Combining with background music.")
            final_audio = CompositeAudioClip([video.audio, music])
        else:
            print("No original audio found in video. Using only background music.")
            final_audio = music

        # Set the final audio to the video
        video_with_audio = video.set_audio(final_audio)

        # Export the final video
        print(f"Exporting the final video to {output_path}...")
        video_with_audio.write_videofile(
            output_path,
            codec='libx264',           # Video codec
            audio_codec='aac',         # Audio codec
            temp_audiofile='temp-audio.m4a',  # Temporary audio file
            remove_temp=True,          # Remove temporary files after processing
            threads=4,                 # Number of threads for processing
            preset='medium'            # Encoding preset (balance between speed and quality)
        )
        print("Export completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
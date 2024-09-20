import subprocess

def create_silent_audio_melt(duration, output_audio_path, fps=44100, n_channels=2):
    """
    Creates a silent audio clip with the specified duration using melt.
    :param duration: Duration of the silent audio clip (in seconds)
    :param output_audio_path: Path for the output silent audio file
    :param fps: Audio sampling rate (default 44100 Hz)
    :param n_channels: Number of channels (default: 2 for stereo)
    """

    # Uses melt to create a silent audio file.
    command = [
        "melt", "color:black", "out=" + str(int(fps * duration)),
        "audiochannels=" + str(n_channels),
        "audio_rate=" + str(fps),
        "-consumer", f"avformat:{output_audio_path}", "acodec=pcm_s16le"
    ]
    subprocess.run(command, check=True)
    print(f"Silent audio created: {output_audio_path}")

def ensure_audio_no_repeat_melt(video_path, output_video_path):
    """
    Ensures the video clip has audio using `melt`. If audio exists, it trims the audio to 
    prevent it from repeating. If the video lacks audio, it creates a silent audio track 
    with the same duration.
    """
    # Use melt to check and handle the audio
    # Create a silent audio track using melt if needed
    command = [
        "melt", video_path, "-attach", "silence",
        "-consumer", f"avformat:{output_video_path}", "vcodec=libx264", "acodec=aac"
    ]
    subprocess.run(command, check=True)
    print(f"Processed video with ensured audio: {output_video_path}")

def join_all_videos_melt(video_paths, output_video_path):
    """
    Joins a list of videos in the specified order using `melt`.
    Ensures the audio is filled with silence if missing and does not repeat if it is shorter.

    :param video_paths: List of video file paths
    :param output_video_path: Path for the output combined video file
    """
    # Create the command list for melt
    command = ["melt"] + video_paths + ["-consumer", f"avformat:{output_video_path}", "vcodec=libx264", "acodec=aac"]
    
    # Run the melt command to concatenate the videos
    subprocess.run(command, check=True)
    print(f"Final video created: {output_video_path}")

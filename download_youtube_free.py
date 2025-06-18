import yt_dlp
import os

def download_youtube_video(url, output_path):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"✅ 動画を保存しました: {output_path}")

if __name__ == "__main__":
    youtube_url = input("🎥 YouTubeのURLを入力してください: ")
    # 絶対パスで保存（自分で変更）
    save_path = "mp4を保存する絶対パスを入力して下さい。"
    download_youtube_video(youtube_url, output_path=save_path)

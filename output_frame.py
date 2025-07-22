# 動画のフレームを切り抜く（１秒ごと）
import os
import cv2
import yt_dlp

# === 設定 ===
SAVE_DIR = "/Users/yamashita_yuma/Documents/AI_Sem/project"
FRAME_DIR = os.path.join(SAVE_DIR, "frames")
VIDEO_PATH = os.path.join(SAVE_DIR, "input_video.mp4")

# === ディレクトリ作成 ===
os.makedirs(FRAME_DIR, exist_ok=True)

# === 動画をダウンロード ===
def download_youtube_video(url, output_path):
    if os.path.exists(output_path):
        print("⚠️ 既存の動画ファイルを削除します（破損対策）")
        os.remove(output_path)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': output_path,
        'quiet': False,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"✅ 動画を保存しました: {output_path}")

# === フレーム抽出 ===
def extract_frames_every_second(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("❌ 動画ファイルを開けませんでした。")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length = frame_count / fps
    frame_interval = int(fps)

    print(f"✅ FPS: {fps}")
    print(f"✅ フレーム数: {frame_count}")
    print(f"✅ 長さ: {video_length:.2f} 秒")
    print(f"✅ フレーム間隔（1秒ごと）: {frame_interval}")

    frame_idx = 0
    saved_idx = 0

    while True:
        success, frame = cap.read()
        if not success or frame is None:
            break

        if frame_idx % frame_interval == 0:
            filename = f"frame_{saved_idx:04d}.jpg"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
            saved_idx += 1

        frame_idx += 1

    cap.release()
    print(f"✅ {saved_idx} 枚のフレームを保存しました → {output_dir}")

# === 実行 ===
if __name__ == "__main__":
    youtube_url = input("🎥 YouTubeのURLを入力してください: ")
    download_youtube_video(youtube_url, VIDEO_PATH)
    extract_frames_every_second(VIDEO_PATH, FRAME_DIR)

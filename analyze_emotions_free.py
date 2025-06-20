import os
import cv2
import pandas as pd
from deepface import DeepFace
from tqdm import tqdm

def extract_frames_every_second(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    duration_msec = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS) * 1000

    current_msec = 0
    saved_idx = 0

    while current_msec < duration_msec:
        cap.set(cv2.CAP_PROP_POS_MSEC, current_msec)
        success, frame = cap.read()
        if not success:
            break
        out_path = os.path.join(output_dir, f"frame_{saved_idx:04d}.jpg")
        cv2.imwrite(out_path, frame)
        saved_idx += 1
        current_msec += 1000
    cap.release()
    return output_dir

def analyze_frames_to_csv(frame_dir, csv_path, output_frame_with_faces_dir=None):
    emotion_weights = {
        'angry': -0.5, 'disgust': -1.0, 'fear': 0.2,
        'happy': 1.0, 'sad': -0.8, 'surprise': 1.2, 'neutral': 0.0
    }

    results = []
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.jpg')])

    if output_frame_with_faces_dir:
        os.makedirs(output_frame_with_faces_dir, exist_ok=True)

    for idx, fname in tqdm(enumerate(frame_files), total=len(frame_files), desc="Analyzing"):
        frame_path = os.path.join(frame_dir, fname)
        try:
            #バックエンドをretinafaceに変更
            analysis_results = DeepFace.analyze(frame_path, actions=['emotion'], enforce_detection=False, detector_backend='retinaface')

            if analysis_results: # 顔が検出された場合
                # 最初の検出された顔の結果を使用
                result = analysis_results[0]
                emotions = result['emotion']
                score = sum(emotions[e] * emotion_weights.get(e, 0) for e in emotions)
                row = {'time_sec': idx, 'score': score, **emotions}
                results.append(row)

                # 顔を囲った画像を保存
                if output_frame_with_faces_dir:
                    x, y, w, h = result['region']['x'], result['region']['y'], result['region']['w'], result['region']['h']
                    frame = cv2.imread(frame_path)
                    if frame is not None:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        output_path_with_face = os.path.join(output_frame_with_faces_dir, f"face_detected_{fname}")
                        cv2.imwrite(output_path_with_face, frame)
            else:
                # 顔が検出されなかった場合もCSVに行を追加する（オプション）
                row = {'time_sec': idx, 'score': 0.0}
                for e in emotion_weights.keys():
                    row[e] = 0.0
                results.append(row)

        except Exception as e:
            print(f"⚠️ Error at {fname}: {e}")

    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False)
    print(f"✅ 表情スコアをCSV出力: {csv_path}")

if __name__ == "__main__":
    # 固定パス（自分で変更）
    video_path = "mp4の絶対パス"
    frame_dir = "各フレームの画像を保存する場所（保存するフォルダ名の例：frame）"
    csv_path = "計算した各感情の値をスコアに表示(保存するファイル名の例：emotion_scores.csv)"
    output_frame_with_faces_dir = "各フレームの顔検出画像を保存する場所（保存するフォルダ名の例：frame_with_faces）"

    extract_frames_every_second(video_path, frame_dir)
    analyze_frames_to_csv(frame_dir, csv_path, output_frame_with_faces_dir)
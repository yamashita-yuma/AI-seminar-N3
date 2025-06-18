import pandas as pd
import matplotlib.pyplot as plt  # type: ignore

# --- ファイルパス ---
file_path = "csvやエクセルファイルがあるパスを指定"  # 必要に応じて修正

# --- 感情一覧（インデックス付き） ---
emotion_columns = [
    'angry',    # 0
    'disgust',  # 1
    'fear',     # 2
    'happy',    # 3
    'sad',      # 4
    'surprise', # 5
    'neutral',  # 6
    'score'     # 7（総合スコア）
]

# --- 感情選択の案内を表示 ---
print("感情を選んでください（番号を入力）:")
for i, emo in enumerate(emotion_columns):
    print(f"{i}: {emo}")

# --- 入力受付（例: 3 → happy） ---
try:
    idx = int(input("番号を入力: "))
    selected_emotion = emotion_columns[idx]
except (ValueError, IndexError):
    print("❌ 無効な入力です。0〜7の番号を指定してください。")
    exit()

# --- データ読み込みと制限 ---
df = pd.read_excel(file_path)
df = df.head(100)  # 行数制限（必要に応じて変更可能）

# --- x軸（時間） ---
x = df["time_sec"]

# --- 選択した感情の単独グラフ ---
plt.figure(figsize=(10, 4))
plt.plot(x, df[selected_emotion], label=selected_emotion, color='blue')
plt.xlabel("Time (sec)")
plt.ylabel("Score")
plt.title(f"時間変化：{selected_emotion}")
plt.grid(True)
plt.legend()
plt.tight_layout()

# --- スコア以外の感情すべてをまとめて描画 ---
plt.figure(figsize=(12, 6))
for emo in emotion_columns[:-1]:  # score を除外
    plt.plot(x, df[emo], label=emo)

plt.xlabel("Time (sec)")
plt.ylabel("Emotion Scores")
plt.title("スコア以外の感情すべての時間推移")
plt.legend()
plt.grid(True)
plt.tight_layout()

# --- 表示 ---
plt.show()
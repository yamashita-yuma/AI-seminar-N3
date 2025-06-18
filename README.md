# それぞれの簡単な内容

**download_youtube_free.py**  
→ YouTube の URL を入力して、それを mp4 ファイルに変換するコード  

**analyze_emotions_free.py**  
→ 表情スコア（感情）を解析して CSV に保存するコード  

**plot_emotions_selectable_free.py**  
→ 結果を任意範囲でプロット可能な可視化ツール  
→ 選択した感情などのグラフの表示、その後全ての感情を同じ図に書いたグラフ

階層
project_folder/
├─ download_youtube_free.py ← MP4保存
├─ analyze_emotions_free.py ← 表情→CSV
├─ input_video.mp4 ← 出力された動画
├─ frames/ ← フレーム画像
├─ emotion_scores.csv ← 表情スコア
└─ plot_emotions_selectable_free ← スコアの可視化

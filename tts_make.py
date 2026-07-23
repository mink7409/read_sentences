import re
import os
import json
import asyncio
import edge_tts

# ===========================
# 설정
# ===========================
DATA_FILE = "data.js"
OUTPUT_DIR = "voice"

VOICE = "ja-JP-NanamiNeural"     # 여자
# VOICE = "ja-JP-KeitaNeural"    # 남자

# ===========================
# 파일명으로 사용할 수 없는 문자 제거
# ===========================
def safe_filename(text):
    text = re.sub(r'[\\/:*?"<>|]', "", text)
    text = text.replace(" ", "")
    return text[:150]


# ===========================
# JS -> JSON 변환
# ===========================
def load_data(filename):

    with open(filename, "r", encoding="utf-8") as f:
        txt = f.read()

    txt = txt.strip()

    # const allvoca =
    txt = re.sub(r'^const\s+allvoca\s*=\s*', '', txt)

    # 마지막 ;
    txt = txt.rstrip(";")

    # key를 JSON 형식으로
    txt = re.sub(r'(\w+)\s*:', r'"\1":', txt)

    return json.loads(txt)


# ===========================
# 음성 저장
# ===========================
async def save_tts(sentence):

    filename = safe_filename(sentence) + ".mp3"

    path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(path):
        print("이미 존재 :", filename)
        return

    communicate = edge_tts.Communicate(
        text=sentence,
        voice=VOICE
    )

    await communicate.save(path)

    print("저장 :", filename)


# ===========================
# 메인
# ===========================
async def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = load_data(DATA_FILE)

    for item in data:

        sentence = item.get("sentence", "").strip()

        if sentence:
            await save_tts(sentence)

    print("완료!")


if __name__ == "__main__":
    asyncio.run(main())
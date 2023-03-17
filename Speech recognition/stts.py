from playrobot import STT
from playrobot import TTS

while input() == 's':   #輸入鍵盤s開始錄音    
    TTS.wordToSound(STT.stt())

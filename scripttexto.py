import whisper
import os
import ffmpeg

# --- CONFIGURACIÓN ---
VIDEO_PATH = "video.mp4"
SRT_PATH = "subtitulos.srt"
OUTPUT_PATH = "video_con_subtitulos.mp4"

# --- TRANSCRIPCIÓN ---
print("Cargando modelo Whisper...")
model = whisper.load_model("base")  # Puedes usar "small", "medium", "large"

print("Transcribiendo audio del video...")
result = model.transcribe(VIDEO_PATH, fp16=False)

# Guardar en formato SRT
with open(SRT_PATH, "w", encoding="utf-8") as f:
    for i, segment in enumerate(result["segments"], start=1):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"].strip()
        
        def format_time(t):
            h = int(t // 3600)
            m = int((t % 3600) // 60)
            s = int(t % 60)
            ms = int((t - int(t)) * 1000)
            return f"{h:02}:{m:02}:{s:02},{ms:03}"
        
        f.write(f"{i}\n")
        f.write(f"{format_time(start)} --> {format_time(end)}\n")
        f.write(f"{text}\n\n")

print("Subtítulos guardados en", SRT_PATH)

# --- AÑADIR SRT AL VIDEO ---
print("Agregando subtítulos al video...")
ffmpeg.input(VIDEO_PATH).output(OUTPUT_PATH, vf=f"subtitles={SRT_PATH}").run()

print("¡Video subtitulado guardado como:", OUTPUT_PATH)

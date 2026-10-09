# -*- coding: utf-8 -*-
"""أداة بسيطة لتنزيل فيديوهات يوتيوب باستخدام yt-dlp."""

import subprocess
import sys
from pathlib import Path


def install_ytdlp():
    """تثبيت yt-dlp تلقائيًا عند عدم توفره."""
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        print("جاري تثبيت yt-dlp ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])


def get_choice():
    print("\n===== أداة تنزيل فيديوهات يوتيوب =====")
    print("1) تنزيل فيديو بأعلى جودة")
    print("2) تنزيل صوت فقط (MP3)")
    print("3) قائمة تشغيل كاملة (فيديو)")
    print("4) تنزيل بجودة محددة")
    print("0) خروج")
    return input("اختر رقم: ").strip()


def hook(download_info):
    if download_info["status"] == "downloading":
        percent = download_info.get("_percent_str", "").strip()
        print(f"\rجاري التنزيل... {percent}", end="", flush=True)
    elif download_info["status"] == "finished":
        print("\nاكتمل التنزيل ✓")


def download(url, mode):
    import yt_dlp

    output_dir = Path("downloads")
    output_dir.mkdir(exist_ok=True)

    options = {
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "noplaylist": mode != "playlist",
        "progress_hooks": [hook],
        "restrictfilenames": True,
    }

    if mode == "mp3":
        options.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )
    elif mode == "quality":
        quality = input("اكتب الجودة مثلاً: 1080 أو 720 أو 480: ").strip()
        if not quality.isdigit() or int(quality) <= 0:
            raise ValueError("يجب إدخال جودة رقمية موجبة.")
        options.update(
            {
                "format": f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
                "merge_output_format": "mp4",
            }
        )
    else:
        options.update(
            {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
            }
        )

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])


def main():
    install_ytdlp()

    while True:
        choice = get_choice()
        if choice == "0":
            break

        mode = {"1": "video", "2": "mp3", "3": "playlist", "4": "quality"}.get(choice)
        if not mode:
            print("اختيار غير صحيح!")
            continue

        url = input("ضع رابط الفيديو أو قائمة التشغيل: ").strip()
        if not url:
            print("يرجى إدخال رابط صالح.")
            continue

        try:
            download(url, mode)
        except KeyboardInterrupt:
            print("\nتم إيقاف التنزيل.")
        except Exception as error:
            print(f"حدث خطأ: {error}")

    print("مع السلامة!")


if __name__ == "__main__":
    main()

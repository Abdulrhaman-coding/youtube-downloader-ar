import py_compile


if __name__ == "__main__":
    py_compile.compile("youtube_downloader.py", doraise=True)
    print("Syntax check passed")

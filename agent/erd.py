import subprocess
import os

def erd_png():
    db_url = "postgresql://db:hehe123@db:5432/monitoring"
    dot_file = "erd.dot"
    png_file = "erd.png"

    # Remove old files if they exist
    if os.path.exists(dot_file):
        os.remove(dot_file)
    if os.path.exists(png_file):
        os.remove(png_file)

    # Create dot file from DB schema
    subprocess.run(["eralchemy", "-i", db_url, "-o", dot_file], check=True)

    # Convert dot file to png
    subprocess.run(["dot", "-Tpng", dot_file, "-o", png_file], check=True)

    return png_file

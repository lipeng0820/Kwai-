import os
import subprocess
import re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk

def load_images():
    global image_folder
    image_folder = filedialog.askdirectory()
    print("图像文件夹：", image_folder)

def load_videos():
    global video_folder
    video_folder = filedialog.askdirectory()
    print("视频文件夹：", video_folder)

def merge():
    global image_folder, video_folder
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
    video_files = sorted([f for f in os.listdir(video_folder) if f.endswith('.mov')])

    if len(image_files) != len(video_files):
        messagebox.showerror('糟糕', '你再确认下图片路径和视频路径!')
        return

    print("合成中...")
    progress_bar["maximum"] = len(image_files)
    for i, (image, video) in enumerate(zip(image_files, video_files)):
        #num = int(re.findall(r'\d+', image)[0])  # 解析文件名编号  
        output = f'{os.path.splitext(image)[0]}-merge.mov'  # 构建输出文件名
        cmd = f'ffmpeg -i {os.path.join(video_folder, video)} -i {os.path.join(image_folder, image)} -filter_complex "overlay=x=0:y=0" {os.path.join(video_folder, output)}'  # 调用ffmpeg进行合成
        subprocess.run(cmd, shell=True, check=True)
        print(f"{i+1}/{len(image_files)} 完成")
        progress_bar["value"] = i + 1
        progress_bar.update()
    print("合成完成")

root = Tk()
root.title("图像和视频合成")

image_folder = None
video_folder = None

image_load_btn = Button(root, text="图像加载", command=load_images)
image_load_btn.pack()

video_load_btn = Button(root, text="视频加载", command=load_videos)
video_load_btn.pack()

merge_btn = Button(root, text="合成", command=merge)
merge_btn.pack()

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack()

root.mainloop()

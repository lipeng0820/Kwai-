# -*- coding:utf-8 -*-
# 感谢chatGPT同学的大力支持，有问题联系lipeng10.
import os
import subprocess
import re
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk

def load_images():
    global image_folder, status_text
    image_folder = filedialog.askdirectory()
    status_text = "封面图像目录 " + str(image_folder)
    status_led(status_text)

def load_videos():
    global video_folder, status_text
    video_folder = filedialog.askdirectory()
    status_text = "素材视频目录 " + str(video_folder)
    status_led(status_text)

def save_merge_path():
    global save_merge_folder, status_text
    save_merge_folder = filedialog.askdirectory()
    status_text = "合成结果将存放在 " + str(save_merge_folder)
    status_led(status_text)

def video_merge():
    global image_folder, video_folder, status_text
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
    video_files = sorted([f for f in os.listdir(video_folder) if f.endswith('.mov')])

    if len(image_files) != len(video_files):
        messagebox.showerror('糟糕', '你再确认下图片路径和视频路径!')
        return

    status_text = "合成中..."
    status_led(status_text)
    progress_bar["maximum"] = len(image_files)
    for i, (image, video) in enumerate(zip(image_files, video_files)):
        #num = int(re.findall(r'\d+', image)[0])  # 解析文件名编号  
        output = f'{os.path.splitext(image)[0]}-merge.mov'  # 构建输出文件名
        cmd = f'ffmpeg -i {os.path.join(video_folder, video)} -i {os.path.join(image_folder, image)} -filter_complex "overlay=x=0:y=0" {os.path.join(save_merge_folder, output)}'  # 调用ffmpeg进行合成
        subprocess.run(cmd, shell=True, check=True)
        status_text = f"{i+1}/{len(image_files)} 完成"
        status_led(status_text)
        progress_bar["value"] = i + 1
        progress_bar.update()
    status_text = "合成完成"
    status_led(status_text)

def status_led(status_text):
    status_label.config(text= "当前状态：" + str(status_text))

root = Tk()
root.title("图像和视频合成")

image_folder = None
video_folder = None
status_text = "请选择封面图像和视频素材的存放文件夹…"

image_load_btn = Button(root, text="加载封面图像", command=load_images)
image_load_btn.pack()

video_load_btn = Button(root, text="加载视频素材", command=load_videos)
video_load_btn.pack()

save_btn = Button(root, text="选择存储路径", command=save_merge_path)
save_btn.pack()

merge_btn = Button(root, text="合成", command=video_merge)
merge_btn.pack()

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack()

status_label = tk.Label(root, text= "当前状态：" + "请选择封面图像和视频素材的存放文件夹…")
status_label.pack()

root.mainloop()

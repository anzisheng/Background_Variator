#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#get_ipython().system('pip install rembg')


# In[ ]:


#get_ipython().system('pip install onnxruntime # Install the missing dependency')


# In[ ]:


import os
import requests
from PIL import Image
from rembg import remove
from io import BytesIO
import matplotlib.pyplot as plt

# Create directories for saving images
os.makedirs('original', exist_ok=True)
os.makedirs('output', exist_ok=True)




# In[ ]:


# Function to download an image
# Function to download an image
def download_image(url):
    try:
        #response = requests.get(url, stream=True)  # Stream the response
        #response.raise_for_status()  # Raise an HTTPError for bad responses
        return Image.open(url)#Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None  # Return None if the image cannot be downloaded


# Input image
#img_url = 'D:\ComfyUI-aki-v1.4\input\0.jpg '#'https://images.pexels.com/photos/1996333/pexels-photo-1996333.jpeg?cs=srgb&dl=pexels-wildlittlethingsphoto-1996333.jpg&fm=jpg'
# img_name = img_url.split('/')[-1]
# img_name = img_name.split('?')[0]
input_image = None #download_image(img_url)
# input_image.save(f'original/{img_name}', format='jpeg')
img_name = "0.jpg"
# Background removal
input_path = f'photo/{img_name}'
output_path = f'output/removed_{img_name}'

with open(input_path, 'rb') as f:
    input_data = f.read()
output_data = remove(input_data)  # Rembg function to remove background
with open(output_path, 'wb') as f:
    f.write(output_data)

# Load the foreground image (with background removed)
foreground = Image.open(output_path).convert("RGBA")

# Backgrounds for variations
background_urls = [
    #'https://img.freepik.com/free-photo/design-space-paper-textured-background_53876-32191.jpg',
    'original/design-space-paper-textured-background_53876-32191.jpg',
    # 'https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg?cs=srgb&dl=pexels-pixabay-414612.jpg&fm=jpg',
    'original/pexels-photo-414612.jpeg',
    'original/brown-gradient-background_53876-104923.jpg',
    'original/field-6574455_640.jpg',
    'original/pexels-pixabay-1034662.jpg',
    # 'https://cdn.pixabay.com/photo/2021/08/25/20/42/field-6574455_640.jpg',
    # 'https://images.pexels.com/photos/1034662/pexels-photo-1034662.jpeg?cs=srgb&dl=pexels-pixabay-1034662.jpg&fm=jpg'
]

# ... previous code ...
# Generate multiple variations and store them
composite_images = [input_image]  # Start with the original image
for i, bg_url in enumerate(background_urls):
    background = Image.open(bg_url)#download_image(bg_url)
    if background is not None: # Check if download was successful
        background = background.convert("RGBA")
        background = background.resize(foreground.size)

        # Composite the images
        composite = background.copy()
        composite.paste(foreground, (0, 0), foreground)

        # Convert to RGB before saving as JPEG
        composite = composite.convert("RGB") # convert the image to RGB

        # Save the output
        output_filename = f'output/variation_{i+1}.jpeg'
        composite.save(output_filename, format='jpeg')
        composite_images.append(composite)
    else:
        print(f"Skipping invalid background URL: {bg_url}")

# Display all images side by side
#fig, axs = plt.subplots(1, len(composite_images), figsize=(15, 5))
#titles = ['Original'] + [f'Variation {i+1}' for i in range(len(background_urls))]

# for ax, img, title in zip(axs, composite_images, titles):
#     ax.imshow(img)
#     ax.set_title(title)
#     ax.axis('off')

# plt.tight_layout()
# plt.show()

import time
import cv2
import tkinter as tk
from PIL import Image, ImageTk
 
 
class CameraApp:
    def __init__(self):
        # 创建界面
        self.window = tk.Tk()  # 创建一个窗口对象
        self.window.title("照相机")  # 设置窗口标题
        self.window.geometry("700x600")  # 设置窗口大小
 
        # 创建显示拍摄照片的控件
        self.photo_label = tk.Label(self.window, width=700, height=550)  # 创建一个标签控件
        self.photo_label.pack()  # 将标签控件添加到窗口中
 
        # 创建拍照按钮
        self.take_photo_button = tk.Button(self.window, text="拍照", command=self.take_photo)  # 创建一个按钮控件
        self.take_photo_button.pack()  # 将按钮控件添加到窗口中
 
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象，打开默认摄像头
        _, self.frame = self.cap.read()  # 读取摄像头的一帧数据
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # 将 BGR 格式的图片转换为 RGB 格式
 
        self.image_flipped = True  # 控制是否镜像照片
 
        # 设置界面保持更新
        self.update_frame()
 
        self.window.mainloop()  # 进入窗口消息循环，等待用户操作
 
    def update_frame(self):
        _, self.frame = self.cap.read()  # 读取新的摄像头帧数据
 
        if self.image_flipped:
            self.frame = cv2.flip(self.frame, 1)  # 如果需要镜像显示照片，则在更新帧时进行翻转操作
 
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # 将 BGR 格式的图片转换为 RGB 格式
 
        # 将摄像头帧转为 PIL 图片格式
        pil_image = Image.fromarray(self.frame)
 
        # 将 PIL 图片转为 Tkinter 中可以显示的图片格式
        tk_image = ImageTk.PhotoImage(image=pil_image)
 
        # 更新显示照片的控件图片
        self.photo_label.configure(image=tk_image)  # 将标签控件的图片属性设置为新的图片
        self.photo_label.image = tk_image  # 将标签控件的 image 属性设置为新的图片
 
        # 循环更新帧
        self.window.after(10, self.update_frame)  # 在 10 毫秒之后调用 update_frame 函数，实现不断更新摄像头帧的效果
 
    def take_photo(self):
        # 拍照
        _, frame = self.cap.read()  # 读取摄像头的一帧数据
 
        if self.image_flipped:
            frame = cv2.flip(frame, 1)  # 如果需要镜像照片，则在拍照时进行翻转操作
 
        # 获取十三位时间戳
        now_time =Utils().getCurrentDateLong()  # 使用 Utils 类中的方法获取当前时间的 13 位时间戳
 
        # 保存照片，以时间戳命名
        cv2.imwrite(f"photo/0.jpg", frame)  # 保存图片到指定路径下，以当前时间戳作为文件名
 
        # 将照片显示在控件中
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将 BGR 格式的图片转换为 RGB 格式
        pil_image = Image.fromarray(frame)  # 将摄像头帧转换为 PIL 图片格式
        tk_image = ImageTk.PhotoImage(image=pil_image)  # 将 PIL 图片转为 Tkinter 可以显示的图片格式
        self.photo_label.configure(image=tk_image)  # 将标签控件的图片属性设置为新的图片
        self.photo_label.image = tk_image  # 将标签控件的 image 属性设置为新的图片
 
        print("照片已保存！")
 
 
class Utils():
    # 获取 13 位的时间戳
    def getCurrentDateLong(self):
        current_timestamp = int(round(time.time() * 1000))  # 获取当前时间的时间戳（精确到毫秒）
        return current_timestamp
 
# 主函数
# if __name__ == "__main__":
#     app = CameraApp()  # 创建 CameraApp 对象，启动程序
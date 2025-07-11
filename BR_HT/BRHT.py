#作者：程浩伦  学校：南京晓庄学院   项目：兵人后台程序  VISION:1.0  创作时间：2025年6月2日
#更新日志：该版本确定了基本布局并实现了基本功能，确定了文本文件作为数据获取的可行性。

#使用tkinter pythonGUI标准库
import tkinter as tk
from tkinter import messagebox

#获取数据功能板块
def data_get():
    data = {}
    key_list = []
    with open('data.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split(':', 1)
            data[f'{key}'] = value
            key_list.append(key)
    return data,key_list

#数据写入功能模块
def data_write(new_data, key_list):
    with open('data.txt', 'w') as file:
        for key in key_list:
            file.write(f"{key}:{new_data[key]}\n")

#保存按钮功能板块
def buttons_save(get_data,key_list):
    new_data={}
    for i, key in enumerate(key_list):
        new_data[key] = get_data[i].get()
    data_write(new_data,key_list)
    messagebox.showinfo('提示信息','保存成功')

#退出按钮功能板块
def buttons_exit(root):
    root.destroy()

#创建UI功能板块
def create_ui():
    root = tk.Tk()
    root.title("兵人后台程序")
    root.geometry("640x480")

    data, key_list = data_get()
    get_data = []

    label = tk.Label(root, text="数值：")
    label.pack(pady=10)

    for key in key_list:
        label=tk.Label(root, text=f'{key}:')
        label.pack(padx=100,pady=10,anchor='w')
        entry = tk.Entry(root, width=40)
        entry.insert(0, f"{data[f'{key}']}")
        entry.pack(padx=200,pady=0,anchor='w')
        get_data.append(entry)

    #创建按钮
    submit_button = tk.Button(root, text="保存", command=lambda:buttons_save(get_data,key_list))
    submit_button.pack(pady=10)
    submit_button = tk.Button(root, text="退出", command=lambda:buttons_exit(root))
    submit_button.pack(pady=10)

    root.mainloop()

#主函数板块
def main():
    create_ui()

main()
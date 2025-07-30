#时间：2025年6月26日 21:09:33
#更新日志：此版本与导航模块一起，修改停止标志符号为‘!’,‘#’改为跳过标志符号,添加了紧急中断按钮‘q’。
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from re import sub
import more_ability as tz
import subprocess

data_path1='/home/mowen/DHHT/datadh.txt'
data_path2='/home/mowen/DHHT/data.txt'
save_path='/home/mowen/DHHT/save.txt'

def data_change(value):
    value_list=[]
    if isinstance(value,tk.Entry):
        value=value.get().strip()
    if isinstance(value,str):
        value=sub(r'\(',' ',value)
        value=sub(r'\)', "*", value)
        value=value.strip()
    if isinstance(value,str):
        value_list=value.split('*')
        for i in range(0,len(value_list)):
            value_list[i]=value_list[i].strip()
    return value_list

def new_key(key_list,much):
    key=key_list[len(key_list)-1]
    name,i=key.split('*',1)
    new_name_list=[]
    i=int(i)
    for j in range(0,much):
        i=i+1
        new_name_list.append(f"{name}*{i}")
    return new_name_list

def data_in(path):
    goals={}
    key_list=[]
    with open(path,'r',encoding='utf-8') as file:
        for line in file:
            if '!' in line:
                break
            elif '#' in line:
                continue
            key,value = line.split(':',1)
            points=[]
            for point in value.split(','):
                point=point.strip()
                points.append(point)
            goals[key]=points
            key_list.append(key)
    return goals,key_list

def data_out(new_data,key_list):
    with open(data_path1,'w',encoding='utf-8') as file:
        for key in key_list:
            if key != key_list[-1]:
                file.write(f'{key}'+':'+ f'{new_data[key]}' + '\n')
            else:
                file.write(f'{key}'+':'+ f'{new_data[key]}')

def buttons_run():
    subprocess.Popen(['python', dh__path])

def buttons_save_exit(window,text_box):
    text=text_box.get('1.0',tk.END)
    print(text)
    with open(data_path2,'w',encoding='utf-8') as file:
        file.write(text)

    points=tz.old_to_new(data_path2)
    tz.write_new_data(points,save_path)

    goals,key_list=data_in(data_path1)

    with open(save_path,'r',encoding='utf-8') as file:
        value=file.read()

    value_list=data_change(value)
    much = len(value_list)-1
    new_key_name_list = new_key(key_list, much)

    for i in range(0, len(new_key_name_list)):
        goals[new_key_name_list[i]] = value_list[i]
        key_list.append(new_key_name_list[i])
        buttons_save(goals, key_list)

    messagebox.showinfo('提示信息', '保存成功')

    window.destroy()

def buttons_exit(root):
    root.destroy()

def buttons_save(get_data, key_list):
    out_data = {}
    for key in key_list:
        entry = get_data[key]
        if isinstance(entry, tk.Entry):
            out_data[key] = entry.get().strip().split(',')
        else:
            out_data[key] = entry
        if isinstance(out_data[key], list):
            out_data[key]=','.join(map(str,out_data[key]))
    data_out(out_data, key_list)

def create_new_window1(goals,key_list,title):
    window = tk.Toplevel()
    window.title(title)
    window.geometry('1080x720')

    change_position={}

    line_num_part1 = 0
    line_num_part2 = 0
    line_num_part3 = 0

    for key in key_list:
        position,i=key.split('*')
        i=int(i)
        key_value=','.join(goals[key])
        pt_key=sub(r"\*",' ',str(key))
        if i<=10:
            position_label = tk.Label(window, text=f'{pt_key}:')
            position_label.grid(row=line_num_part1,column=0,sticky='w')
            line_num_part1+=1
            entry = tk.Entry(window, width=40)
            entry.insert(0, f"{key_value}")
            entry.grid(row=line_num_part1,column=0,sticky='w')
            line_num_part1+=1
            change_position[key]=entry
        elif 10<i<=20:
            position_label = tk.Label(window, text=f'{pt_key}:')
            position_label.grid(row=line_num_part2,column=3,padx=50,sticky='w')
            line_num_part2+=1
            entry = tk.Entry(window, width=40)
            entry.insert(0, f"{key_value}")
            entry.grid(row=line_num_part2,column=3,padx=50,sticky='w')
            line_num_part2+=1
            change_position[key]=entry
        elif i>20:
            position_label = tk.Label(window, text=f'{pt_key}:')
            position_label.grid(row=line_num_part3,column=5,padx=50,sticky='w')
            line_num_part3+=1
            entry = tk.Entry(window, width=40)
            entry.insert(0, f"{key_value}")
            entry.grid(row=line_num_part3,column=5,padx=50,sticky='w')
            line_num_part3+=1
            change_position[key]=entry

    submit_button_save = tk.Button(window, text="保存", command=lambda:buttons_save(change_position,key_list))
    submit_button_save.grid(row=22,column=3,pady=10,sticky='nsew')
    submit_button_back=tk.Button(window,text="返回",command=lambda:buttons_exit(window))
    submit_button_back.grid(row=23,column=3,pady=10, sticky='nsew')

    window.mainloop()

def create_new_window2():
    window = tk.Toplevel()
    window.title('添加原始数据')
    window.geometry('720x720')

    label=tk.Label(window, text='输入原始数据')
    label.pack(padx=0,pady=5,anchor='center')
    text_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=30)
    text_box.pack(expand=True,pady=0,anchor='center')

    button_save_exit=tk.Button(window, text="保存", command=lambda:buttons_save_exit(window,text_box))
    button_save_exit.pack(pady=5,anchor='center')

    window.mainloop()

def buttons_check():
    goals,key_list = data_in(data_path1)
    create_new_window1(goals,key_list,'已保存的点')

def buttons_tz1():
    create_new_window2()

def create_ui_main():
    root = tk.Tk()
    root.title('导航定点管理')
    root.geometry("640x480")

    goals,key_list = data_in(data_path1)

    label = tk.Label(root, text="数值：")
    label.pack(pady=10)

    label_add = tk.Label(root, text="添加:")
    label_add.pack(padx=100, pady=10, anchor='w')
    entry_add = tk.Entry(root,width=40)
    entry_add.pack(padx=100, pady=10, anchor='w')

    def buttons_add():
        value_list = data_change(entry_add)
        much = len(value_list)-1
        new_key_name_list = new_key(key_list, much)
        if much:
            for i in range(0, len(new_key_name_list)):
                goals[new_key_name_list[i]] = value_list[i]
                key_list.append(new_key_name_list[i])
                buttons_save(goals, key_list)
                entry_add.delete(0, tk.END)
                messagebox.showinfo('提示信息', '保存成功')
        else:
            messagebox.showwarning('警告', '请输入有效的数值')

    submit_button_add = tk.Button(root,text="添加",command=buttons_add)
    submit_button_add.pack(padx=100,pady=10,anchor='w')
    submit_button_tz1 = tk.Button(root, text="添加原始数据", command=buttons_tz1)
    submit_button_tz1.pack(padx=100,pady=10,anchor='w')
    submit_button_run = tk.Button(root, text="运行", command=buttons_run)
    submit_button_run.pack(padx=100,pady=10,anchor='w')
    submit_button_check = tk.Button(root, text="查看保存的点", command=lambda:buttons_check())
    submit_button_check.pack(pady=10)
    submit_button_exit = tk.Button(root, text="退出", command=lambda:buttons_exit(root))
    submit_button_exit.pack(pady=10)

    root.mainloop()

def main():
    tz.data_init(data_path2)
    tz.data_init(save_path)
    create_ui_main()

if __name__ == '__main__':
    main()
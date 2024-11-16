import tkinter as tk  
from tkinter import scrolledtext  
from http import HTTPStatus  
from dashscope import Application  

# 创建主窗口  
root = tk.Tk()  
root.title("大模型对话界面")  
root.geometry("400x500")  

# 聊天历史区域  
chat_history = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)  
chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)  

# 输入框  
entry = tk.Entry(root, width=40)  
entry.pack(pady=10, padx=10)  

def call_agent_app(prompt):  
    try:  
        response = Application.call(  
            app_id='f705667d3c824420a9aacebc4333002b',  
            prompt=prompt,  
            api_key='sk-6e8c2d1210bb49fc8f32646d883cba94'  # 请替换为你的实际API密钥  
        )  
        return response  
    except Exception as e:  
        return None, str(e)  # 直接返回异常信息  

def send_message():  
    user_input = entry.get().strip()  # 清理用户输入  
    if not user_input:  
        return  

    # 展示用户输入到聊天历史  
    append_to_chat(f"你: {user_input}\n")  
    entry.delete(0, tk.END)  # 清空输入框  

    # 调用 Dashscope API 生成响应  
    response= call_agent_app(user_input)  

    if response is None:  # 处理API调用错误  
        append_to_chat(f"错误信息: {response}\n")  
        return  

    if response.status_code != HTTPStatus.OK:  
        append_to_chat(f"错误信息: {response.message}\n")  
        return  

    # 显示助手的响应到聊天历史  
    append_to_chat(f"助手: {response.output.text}\n")  

    # 检查是否为再见  
    if "再见" in response.output:  
        append_to_chat("助手: 再见！结束对话。\n")  
        end_conversation()  

def append_to_chat(message):  
    chat_history.config(state=tk.NORMAL)  
    chat_history.insert(tk.END, message)  
    chat_history.config(state=tk.DISABLED)  
    chat_history.yview(tk.END)  # 滚动到最新消息  

def end_conversation():  
    entry.config(state=tk.DISABLED)  # 禁用输入框  
    send_button.config(state=tk.DISABLED)  # 禁用发送按钮  

# 发送按钮  
send_button = tk.Button(root, text="发送", command=send_message)  
send_button.pack(pady=10)  

# 运行主循环  
root.mainloop()
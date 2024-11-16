import tkinter as tk  
from tkinter import scrolledtext  
from openai import OpenAI  

# 初始化OpenAI客户端  
client = OpenAI(  
    api_key="sk-6e8c2d1210bb49fc8f32646d883cba94",  
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  
)  

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

def send_message():  
    user_input = entry.get()  
    if user_input.strip() == "":  
        return  # 如果输入为空则不进行处理  

    # 展示用户输入到聊天历史  
    chat_history.config(state=tk.NORMAL)  
    chat_history.insert(tk.END, f"你: {user_input}\n")  
    chat_history.config(state=tk.DISABLED)  

    # 清空输入框  
    entry.delete(0, tk.END)  

    # 调用API生成响应  
    try:  
        # 将用户消息添加到消息列表  
        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},  
                    {'role': 'user', 'content': user_input}]  
        
        completion = client.chat.completions.create(  
            model="qwen-turbo",  
            messages=messages  
        )  
        
        assistant_response = completion.choices[0].message.content  
        
        # 显示助手的响应到聊天历史  
        chat_history.config(state=tk.NORMAL)  
        chat_history.insert(tk.END, f"助手: {assistant_response}\n")  
        chat_history.config(state=tk.DISABLED)  

        # 检查是否为再见  
        if "再见" in assistant_response:  
            chat_history.config(state=tk.NORMAL)  
            chat_history.insert(tk.END, "助手: 再见！结束对话。\n")  
            chat_history.config(state=tk.DISABLED)  
            entry.config(state=tk.DISABLED)  # 禁用输入框  
            send_button.config(state=tk.DISABLED)  # 禁用发送按钮  

    except Exception as e:  
        chat_history.config(state=tk.NORMAL)  
        chat_history.insert(tk.END, f"错误信息: {e}\n")  
        chat_history.config(state=tk.DISABLED)  

# 发送按钮  
send_button = tk.Button(root, text="发送", command=send_message)  
send_button.pack(pady=10)  

# 运行主循环  
root.mainloop()
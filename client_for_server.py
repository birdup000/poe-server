from tkinter import *
import requests
from datetime import datetime


def send_message(event=None):
    url = "http://localhost:8000/generate-response"
    headers = {"Content-Type": "application/json"}

    user_input = entry_field.get()
    payload = {"text": user_input}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises a stored HTTPError, if one occurred.
        server_response = response.json()
        server_response_text = server_response.get('response', 'No response')

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg_list.insert(END, timestamp + " You: " + user_input + '\n\n')
        entry_field.delete(0, END)

        # Disable send button during typing effect
        send_button.config(state=DISABLED)
        type_response(timestamp + " Server: " + server_response_text)

    except requests.exceptions.HTTPError as err:
        msg_list.insert(END, f"HTTP error occurred: {err}\n")
    except Exception as err:
        msg_list.insert(END, f"An error has occurred: {err}\n")

    # Set focus back to entry_field
    entry_field.focus()


def type_response(response):
    def append_character(character):
        msg_list.insert(END, character)
        msg_list.see(END)
        if character == '\n':
            # Re-enable send button after typing effect
            send_button.config(state=NORMAL)

    for character in response + '\n\n':
        root.after(50, append_character, character)  # Delay of 50ms between each character


root = Tk()
root.title("Chat Client")
root.geometry("800x600")

root.configure(bg='black')

messages_frame = Frame(root, bg='black')
messages_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

scrollbar = Scrollbar(messages_frame)

msg_list = Text(messages_frame, yscrollcommand=scrollbar.set, wrap=WORD, bg='black', fg='white', spacing2=5)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH, expand=True)

entry_field = Entry(root, bg='black', fg='white', insertbackground='white')
entry_field.bind("<Return>", send_message)
entry_field.grid(row=1, column=0, sticky='ew', padx=10, pady=10)

send_button = Button(root, text="Send", command=send_message, bg='black', fg='white', activebackground='grey')
send_button.grid(row=1, column=1, padx=10, pady=10)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()

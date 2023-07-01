import tkinter as tk

import file_handler


def _box_select(event: tk.Event):
    widget = event.widget
    selected_kube_name = widget.get(widget.curselection()[0])
    
    selected_kube_config = file_handler.get_kube_config_by_name(selected_kube_name)
    
    file_handler.set_kube_config(selected_kube_config)
    print(f"Set '{selected_kube_name}'!")
    exit(0)
    
def start():
    root = tk.Tk()
    root.geometry("300x350")
    root.title("KubeConfig Switcher")

    list_box=tk.Listbox(root,font=('times',16), width=0)
    list_box.bind('<<ListboxSelect>>', _box_select)
    list_box.pack(padx=10,pady=10,fill=tk.BOTH, expand=True)

    for file in file_handler.get_stored_kube_configs():
        list_box.insert(tk.END, file.name)
    
    root.mainloop()

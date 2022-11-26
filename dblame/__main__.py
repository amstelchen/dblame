import re
import os
import sys
import textwrap
import tkinter as tk
from tkinter import TclError
from tkinter import ttk
from subprocess import run

__version__ = "0.1.3"


def add_menu_bar(root):
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

def check_init_system():
    pass

def get_unit_desc(unit_name: str) -> str:
    # on Arch, /lib is a symlink to /usr/lib
    # on any other system, system-wide systemd units are in /lib
    unit_file = os.path.join("/lib/systemd/system/", unit_name)
    pattern = "\@\d+"
    # handle units like "/usr/lib/systemd/system/user@.service"
    # or "user-runtime-dir@1000.service"
    unit_file = re.sub(pattern, "@", unit_file, count=0, flags=0)

    if os.path.isfile(unit_file):
        with open(unit_file, "rt") as unit:
            for line in unit.readlines():
                if line.startswith("Description"):
                    return line.split("=")[1]
        return "User"
    return ""

def main():
    try:
        # create the Tkinter root window
        root = tk.Tk()
    except tk.TclError as e:
        # print a warning if the GUI is run on a console
        print(e, "\nExiting.")
        sys.exit()
    root.geometry("640x480")
    root.title('dblame' + " " + __version__)
    root.resizable(0, 0)

    icon_path = os.path.join(os.path.dirname(__file__), 'dblame.png')
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=icon_path))

    add_menu_bar(root)

    # configure the Tkinter grid
    root.columnconfigure(0, weight=1, pad=0)
    root.rowconfigure(0, weight=1, pad=0, minsize=70)
    root.rowconfigure(1, weight=1, pad=0, minsize=70)
    root.rowconfigure(3, weight=1, pad=0, minsize=70)
    root.rowconfigure(4, weight=1, pad=0, minsize=100)

    init_version = run(["init", "--version"], capture_output=True).stdout.decode("utf-8")
    if not "systemd" in init_version:
        print("This system is not using systemd. Exiting.")
        exit()
    command = "systemd-analyze"
    version = command + " --version | head -n 1"
    sd_version = run(version.split(), capture_output=True).stdout.decode("utf-8")
    sd_time = run([command, "time"], capture_output=True).stdout.decode("utf-8").strip()
    sd_blame = run([command, "blame"], capture_output=True).stdout.decode("utf-8")
    sd_units = run("systemctl list-units --type service --all".split(), capture_output=True).stdout.decode("utf-8")

    #time_temp = sd_time.replace("Startup finished in ", "").split("\n")[0]
    #time_items =  time_temp.split(" = ")[0].split(" + ")
    #total_time =  time_temp.split(" = ")[1]
    blame_items = sd_blame.split("\n") 
    #time_items.pop()
    #print(sd_time, total_time, time_items)^

    #time_items = {}
    #time_temp = sd_time.replace("Startup finished in ", "").replace("+ ", "").replace("= ", "").split(" \n")[0]
    #time_items = time_temp.split(" ")

    tokens = r"[\d]*[.][\d]+"
    time_items = [float(t) for t in re.findall(tokens, sd_time)]
    #print(time_items)

    #time_items = sd_time.replace("Startup finished in ", "").split(" \n")[0].split(" ")
    #time_items.append("total")
    #time_items = list(set(time_items))
    total_time = time_items[-2]

    box_height = 70
    abs_left = 5
    abs_right = 0
    padding = 5
    #colors = {"orange": "#fb0", "red": "#f50", "green": "#f60", "blue": "#05f"}
    colors = ["#81d4fa", "#fff9c4", "#80cbc4", "#ffcc80"]

    root.update()

    canvas = tk.Canvas(root, width=root.winfo_width() - 10) # bg='skyblue', 
    for box in range(len(time_items) - 2):
        percent = 100 * time_items[box] / total_time
        width = (root.winfo_width() - padding) * percent / 100
        abs_right += width
        canvas.create_rectangle(abs_left, padding, abs_right, box_height, outline=colors[box], fill=colors[box])
        abs_left = abs_right
    #canvas.create_rectangle(150, 10, 240, box_height,outline="#f50", fill="#f50")
    #canvas.create_rectangle(270, 10, 370, box_height, outline="#05f", fill="#05f")
    canvas.grid(column=0, row=0, sticky=tk.NSEW, padx=0, pady=0, ipady=0)


    #s = ttk.Style()
    #for box in range(len(time_items) // 2):
    #    s.configure('Danger.TFrame', background=colors[box], borderwidth=5, relief='flat')
    #    f = ttk.Frame(root, width=50, height=50, style='Danger.TFrame', padding=(0, 0))
    #    f.grid(column=box, row=0, columnspan=1)
    #f['padding'] = (0, 10)

    label = ttk.Label(root, text=sd_time) # font="Monospace 8 bold"
    label.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=10)

    label2 = ttk.Label(root, text=sd_version, wraplength=630, justify=tk.LEFT)
    label2.grid(column=0, row=4, sticky=tk.NSEW, padx=5, pady=0)

    #text = tk.Text(root, width=40, height=2)
    #text.insert('1.0', 'here is my\ntext to insert')
    #text.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=5)

    list_items = tk.Variable(value=blame_items)
    listbox = tk.Listbox(
        root,
        height=10,
        listvariable=list_items
    )
    #listbox.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

    tree = ttk.Treeview(root, height=30,)
    tree['columns'] = ('service', 'desc')
    tree.column('#0', width=20)
    tree.column('service', width=100)
    tree.column('desc', width=300)
    tree.heading('#0', text=' Time', anchor='w')
    tree.heading('service', text=' Service', anchor='w')
    tree.heading('desc', text=' Description', anchor='w')
    #id = tree.insert('', 'end', text='Tutorial')

    #for key, item in items.split(" "):
    for item in blame_items:
        if len(item) > 0:
            item = item.lstrip()
            t = item.split(" ")[0]
            s = item.split(" ")[1]
        tree.insert('', 'end', text=t, values=(s, get_unit_desc(s)))

    tree.grid(column=0, row=3, sticky=tk.NSEW, padx=5, pady=0)

    root.mainloop()

if __name__ == "__main__":
    main()
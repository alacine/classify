import json
import tkinter
from tkinter import filedialog
import classify


window = tkinter.Tk()
window.title('Classify 文档归类工具')

# file_path = filedialog.askopenfilename()
file_path = filedialog.askdirectory()
print(file_path)
source_dir = classify.Classify(file_path)
source_dir.sort_by_extension()
print('sorted: ', json.dumps(source_dir.extension_sorted, indent=4))

filetype_list = tkinter.Listbox(window)
for filetype, files in source_dir.extension_sorted.items():
    for filename in files:
        # print(filename)
        filetype_list.insert(1, filename)
filetype_list.pack()


# listb = tkinter.Listbox(window)
# for filename in filenames:
    # listb.insert(2, filename)
# listb.pack()

window.mainloop()

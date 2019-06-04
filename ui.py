import json
import tkinter
from tkinter import filedialog
import classify


class MyWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # 菜单栏
        menubar = tkinter.Menu(self)
        help_menu = tkinter.Menu(menubar, tearoff=0)
        more_menu = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='帮助', menu=help_menu)
        help_menu.add_command(label='如何使用？', command=self.how_to_use)
        menubar.add_cascade(label='更多', menu=more_menu)
        more_menu.add_command(label='项目地址', command=self.project_url)
        more_menu.add_command(label='提交 BUG', command=self.report_bug)
        self.config(menu=menubar)
        # 标题
        heading = tkinter.Label(self, text='Classify 文档归类工具', height=2)
        heading.pack()
        # 选择目录按钮
        select_dir_button = tkinter.Button(
            self, text='选择操作目录',
            height=2, command=self.open_dir
        )
        select_dir_button.pack(side=tkinter.LEFT)
        # 选择分类方式按钮
        select_way_button1 = tkinter.Radiobutton(self, text='根据文件类型分类')
        select_way_button1.pack(side=tkinter.LEFT)
        select_way_button2 = tkinter.Radiobutton(self, text='根据文件类型分类')
        select_way_button2.pack(side=tkinter.LEFT)
        # 分类后结果展示
        show_list = tkinter.Listbox(self)
        show_list.pack(fill=tkinter.BOTH, expand=True)
        # 清空分类结果按钮
        clean_button = tkinter.Button(
            self, text='清空分类结果',
            command=self.clean_show_list
        )
        clean_button.pack(side=tkinter.RIGHT)
        # 应用分类结果按钮
        apply_button = tkinter.Button(
            self, text='应用分类结果',
            command=self.apply_show_list
        )
        apply_button.pack(side=tkinter.RIGHT)

    def project_url(self):
        pass

    def report_bug(self):
        pass

    def how_to_use(self):
        pass

    def open_dir(self):
        self.file_path = filedialog.askdirectory()

    def clean_show_list(self):
        pass

    def apply_show_list(self):
        pass


if __name__ == '__main__':
    window = MyWindow()
    window.title('Classify 文档归类工具')
    # window.geometry('500x500')
    window.mainloop()

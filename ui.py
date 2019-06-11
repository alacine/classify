# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import classify


def change_status(button_func):
    """按钮装饰器, 使得按钮工作时可以显示是否工作完成"""
    def wrapper(self):
        self.status.set('{}{}...'.format('开始', button_func.__name__))
        button_func(self)
        self.status.set('{}{}'.format('结束', button_func.__name__))
    return wrapper


class MyWindow(tk.Tk):
    """文档分类窗口"""

    def __init__(self):
        """初始化"""
        super().__init__()
        self.status = tk.StringVar(value='启动')
        self.selection = tk.IntVar(value=0)
        self.clfy_ins = classify.Classify('.')
        self.setup_ui()

    def setup_ui(self):
        """构建 UI"""
        # 框架
        frame1 = tk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.X, expand=True)

        frame2 = tk.Frame(self)
        frame2.pack(side=tk.TOP, fill=tk.X, expand=True)
        frame2_a = tk.Frame(frame2)
        frame2_a.pack(side=tk.LEFT)
        frame2_b = tk.Frame(frame2)
        frame2_b.pack(side=tk.LEFT, fill=tk.X)
        frame2_c = tk.Frame(frame2)
        frame2_c.pack(side=tk.RIGHT)

        frame3 = tk.Frame(self)
        frame3.pack(side=tk.TOP, fill=tk.X, expand=True)

        frame4 = tk.Frame(self)
        frame4.pack(side=tk.TOP, fill=tk.X, expand=True)

        # 菜单栏
        menubar = tk.Menu(self)
        help_menu = tk.Menu(menubar, tearoff=0)
        more_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='帮助', menu=help_menu)
        help_menu.add_command(label='如何使用？', command=self.how_to_use)
        menubar.add_cascade(label='更多', menu=more_menu)
        more_menu.add_command(label='项目地址', command=self.project_url)
        more_menu.add_command(label='问题反馈', command=self.report_bug)
        self.config(menu=menubar)

        # 标题
        heading = tk.Label(
            frame1,
            text='Classify 文档归类工具',
            height=2,
            bg='green'
        )
        heading.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 选择目录按钮
        select_dir_button = tk.Button(
            frame2_a, text='选择操作目录',
            height=2, command=self.open_dir
        )
        select_dir_button.pack(side=tk.LEFT)

        # 选择分类方式按钮
        select_way_button1 = tk.Radiobutton(
            frame2_b,
            text='根据文件类型分类',
            variable=self.selection,
            value=0,
        )
        select_way_button1.pack(side=tk.TOP)
        select_way_button2 = tk.Radiobutton(
            frame2_b,
            text='根据给定文件名称分类',
            variable=self.selection,
            value=1,
        )
        select_way_button2.pack(side=tk.BOTTOM)

        # 分类预览按钮
        preview_button = tk.Button(
            frame2_c,
            text='分类预览', command=self.preview
        )
        preview_button.pack(side=tk.LEFT)

        # 分类后结果展示
        self.show_list = tk.Text(frame3)
        self.show_list.pack(fill=tk.BOTH, expand=True)

        # 状态显示
        self.show_status = tk.Label(frame4, textvariable=self.status)
        self.show_status.pack(side=tk.LEFT)

        # 应用分类结果按钮
        apply_button = tk.Button(
            frame4, text='应用分类结果',
            command=self.apply_show_list
        )
        apply_button.pack(side=tk.RIGHT)

        # 清空分类结果按钮
        clean_button = tk.Button(
            frame4, text='清空分类结果',
            command=self.clean_show_list
        )
        clean_button.pack(side=tk.RIGHT)

    @staticmethod
    def project_url():
        """项目地址按钮动作
        点击打开项目网址
        """
        webbrowser.open('https://gitee.com/ryanrui/classify')

    @staticmethod
    def report_bug():
        """问题反馈按钮动作
        点击打开新窗口, 显示提示信息和提交邮箱
        """
        msg_title = '问题反馈渠道'
        msg_content = (
            '反馈方式:\n'
            '1. 邮箱 ryanruirr@gmail.com\n'
            '2. 在项目地址中提交 Issue\n\n'
            '请说明遇到的问题，并附带一下内容:\n'
            '1. 你使用的操作系统\n'
            '2. 问题截图'
        )
        tk.messagebox.showinfo(title=msg_title, message=msg_content)

    @staticmethod
    def how_to_use():
        """如何使用按钮动作
        点击打开新窗口, 显示使用手册
        """
        msg_title = '使用说明'
        msg_content = (
            '1. 选择你要整理的目录\n'
            '2. 选择文件分类方式\n'
            '3. 点击分类预览\n'
            '4. 确认分类无误后点击应用分类结果'
        )
        tk.messagebox.showinfo(title=msg_title, message=msg_content)

    @change_status
    def open_dir(self):
        """选择目录按钮动作
        点击打开窗口, 手动选择目录
        """
        self.clfy_ins.target_dir = filedialog.askdirectory()

    @change_status
    def preview(self):
        """分类预览按钮动作
        点击后在预览框内显示分类结果(json 格式)
        """
        self.clean_show_list()
        # content_list_in_text = self.show_list.get('0.0', 'end-1c')
        content_list = ['111', '2', '33']
        # print(content_list_in_text)
        if self.selection.get() == 0:
            self.clfy_ins.sort_by_extension()
            preview_data = json.dumps(self.clfy_ins.extension_sorted, ensure_ascii=False, indent=4)
        else:
            self.clfy_ins.sort_by_name(content_list)
            preview_data = json.dumps(self.clfy_ins.name_sorted, ensure_ascii=False, indent=4)
        self.show_list.insert('end', preview_data)

    @change_status
    def clean_show_list(self):
        """清空预览结果按钮
        点击后清空预览框中的内容, 清空 clfy_ins 原有的分类结果
        """
        self.show_list.delete(0.0, 'end')
        self.clfy_ins.extension_sorted.clear()
        self.clfy_ins.name_sorted.clear()

    @change_status
    def apply_show_list(self):
        """应用分类结果按钮
        点击后弹出提示框确认, 确认后实施分类
        """
        # if self.selection == 0:
        if self.selection.get() == 0:
            self.clfy_ins.do_extension_sort(True)
        else:
            self.clfy_ins.do_name_sort(True)


if __name__ == '__main__':
    APP = MyWindow()
    # print(APP.winfo_screenwidth())
    APP.title('Classify 文档归类工具')
    APP.resizable(width=True, height=True)
    APP.geometry('{}x{}'.format(500, 800))
    APP.mainloop()

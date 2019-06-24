# -*- coding: utf-8 -*-
import os
import shutil
import json
from typing import List


class Classify:
    """文档分类工具

    Args:
        target_dir (str): 需要进行文档分类的根目录
        content (list(str)): 需要分类的字段集

    Attributes:
        target_dir (str): 需要进行文档分类的根目录
        extension_sorted (dict): 根据扩展名分类后的结果
        name_sorted (dict): 根据名称所含字段分类后的结果
    """
    def __init__(self, target_dir: str):
        """初始化
        Args:
            target_dir (str): 需要进行文档分类的根目录
        """
        self.target_dir = target_dir
        self.extension_sorted = {}
        self.name_sorted = {}

    def sort_by_extension(self):
        """根据文件的扩展名进行分类"""
        for dirpath, dirnames, filenames in os.walk(self.target_dir):
            for filename in filenames:
                path_to_file = os.path.join(dirpath, filename)
                file_ext = os.path.splitext(filename)[1]
                if not file_ext:
                    file_ext = '.No_extension_file'
                if file_ext not in self.extension_sorted:
                    self.extension_sorted[file_ext] = []
                self.extension_sorted[file_ext].append(path_to_file)

    def sort_by_name(self, content_list: List[str]):
        """根据文件名称中包含的字段分类
        Args:
            content (list[str]): 需要分类的字段集
        """
        contents = set(content_list)
        for dirpath, dirnames, filenames in os.walk(self.target_dir):
            for filename in filenames:
                for content in contents:
                    if content not in filename:
                        continue
                    path_to_file = os.path.join(dirpath, filename)
                    if content not in self.name_sorted:
                        self.name_sorted[content] = []
                    self.name_sorted[content].append(path_to_file)

    def do_extension_sort(self, copy=False):
        """根据扩展名的分类结果归类文件到相应扩展名的目录
        Args:
            copy (bool): 归类时是否保留原来的目录结构, 默认不保持
        """
        # 创建相应目录
        for extension in self.extension_sorted:
            if extension[1:] not in os.listdir(self.target_dir):
                os.mkdir(os.path.join(self.target_dir, extension[1:]))
        # 移动到相应目录
        for extension, filenames in self.extension_sorted.items():
            for filename in filenames:
                destination = os.path.join(
                    self.target_dir,
                    extension[1:],
                    os.path.split(filename)[1]
                )
                # print(destination)
                if copy:
                    shutil.copyfile(filename, destination)
                else:
                    shutil.move(filename, destination)

    def do_name_sort(self, copy=False):
        """根据名称的分类结果归类文件到相应的名称的目录
        Args:
            copy (bool): 归类时是否保留原来的目录结构, 默认不保持
        """
        # 创建相应目录
        for name in self.name_sorted:
            if name not in os.listdir(self.target_dir):
                os.mkdir(os.path.join(self.target_dir, name))
        # 移动到相应目录
        for filetype, filenames in self.name_sorted.items():
            for filename in filenames:
                destination = os.path.join(
                    self.target_dir,
                    filetype,
                    os.path.split(filename)[1]
                )
                # print(destination)
                if copy:
                    shutil.copyfile(filename, destination)
                else:
                    shutil.move(filename, destination)

    def export_dir(self, chosen: int, filename: str):
        """导出归类文件的目录结构到纯文本文件中
        Args:
            chosen (int): 0 表示使用的是文件扩展名归类, 否则是按名称归类
            filename (str): 导出的文件名
        """
        if chosen == 0:
            data = json.dumps(
                self.extension_sorted,
                ensure_ascii=False,
                indent=4
            )
        else:
            data = json.dumps(
                self.name_sorted,
                ensure_ascii=False,
                indent=4
            )
        with open(filename, 'w') as export_file:
            export_file.write(data)

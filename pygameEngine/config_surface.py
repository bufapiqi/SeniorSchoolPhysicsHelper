"""  进入主页面的配置页面
    比如 可以选择窗口的大小  i.e： 600 * 600
    保存的文件路径，或者选择读取文件的路径，或者一个空画布 等等
"""

# todo  熊凯奇

from tkinter import *
from tkinter.filedialog import askdirectory

from util.file_util import FileUtil, MyParser


class ConfigSurface:
    length: StringVar
    width: StringVar
    savePath: StringVar
    path: StringVar

    def select_path(self):
        path_: str = askdirectory()
        print(self.path)
        self.path.set(path_)

    def save_path(self):
        path_: str = askdirectory()
        self.savePath.set(path_)

    def print_path(self):
        print(self.path.get())
        self.path.set('')

    def update_config(self):
        a = FileUtil("../resources/static.config")
        a.add_section1("d")
        a.save()
        a.set_item("d", 'length', self.length.get())
        a.set_item('d', 'width', self.width.get())
        a.set_item('d', 'savepath', self.width.get())
        a.save()

    def __init__(self, command='新建'):
        root = Tk()
        root.title("hello")
        root.geometry("360x300")

        reader = MyParser()
        reader.read("../resources/static.config", encoding="utf8")
        params = reader.as_dict().get('d')
        if params is not None:
            self.length = StringVar(None, params.get('length')) if params.get('length') is not None else StringVar()
            self.width = StringVar(None, params.get('width')) if params.get('width') is not None else StringVar()
            self.savePath = StringVar(None, params.get('savepath')) if params.get('savepath') is not None else StringVar()
            self.path = StringVar(None, params.get('path')) if params.get('path') is not None else StringVar()
        else:
            self.length = StringVar()
            self.width = StringVar()
            self.savePath = StringVar()
            self.path = StringVar()

        shapeFrame = LabelFrame(root)
        shapeFrame.pack(side=TOP, padx=10, pady=5)
        newLabel = Label(shapeFrame, text='新建画布:', font=('Arial', 10)).pack(side=LEFT, padx=10, pady=5)

        lengthFrame = Frame(shapeFrame)
        lengthFrame.pack(padx=10, pady=5, expand=YES, fill=BOTH)
        lengthLabel = Label(lengthFrame, text="画布长:").pack(side=LEFT, padx=2, pady=5, anchor=W)
        lengthEntry = Entry(lengthFrame, textvariable=self.length).pack(side=RIGHT, padx=2, pady=5, anchor=E)

        widthFrame = Frame(shapeFrame)
        widthFrame.pack(side=TOP, padx=10, pady=5, expand=YES, fill=BOTH)
        widthLabel = Label(widthFrame, text="画布宽:").pack(side=LEFT, padx=2, pady=5, anchor=W)
        widthEntry = Entry(widthFrame, textvariable=self.width).pack(side=RIGHT, padx=2, pady=5, anchor=E)

        saveFrame = Frame(shapeFrame)
        saveFrame.pack(side=TOP, padx=10, pady=5, expand=YES, fill=BOTH)
        saveLabel = Label(saveFrame, text="保存路径:").pack(side=LEFT, padx=2, pady=5, anchor=W)
        saveEntry = Entry(saveFrame, textvariable=self.savePath).pack(side=LEFT, padx=2, pady=5, anchor=W)
        chooseBtn = Button(saveFrame, text="...", command=self.save_path).pack(side=LEFT, padx=0, pady=5, anchor=W)

        msFrame = Frame(shapeFrame)
        msFrame.pack(side=TOP, padx=10, pady=5)
        newBtn = Button(msFrame, text=command, command=self.update_config).pack(side=LEFT, padx=0, pady=5, anchor=W)

        pathChoose = LabelFrame(root)
        pathChoose.pack(side=TOP, padx=10, pady=5)
        pathLabel = Label(pathChoose, text="选择画布:").pack(side=LEFT, padx=2, pady=5, anchor=W)
        pathEntry = Entry(pathChoose, textvariable=self.path).pack(side=LEFT, padx=2, pady=5, anchor=W)
        chooseBtn = Button(pathChoose, text="路径选择", command=self.select_path).pack(side=LEFT, padx=0, pady=5, anchor=W)
        msBtn = Button(pathChoose, text="确认", command=self.print_path).pack(side=LEFT, padx=0, pady=5, anchor=W)
        root.mainloop()


if __name__ == '__main__':
    a = ConfigSurface()

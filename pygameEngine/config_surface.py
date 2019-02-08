"""  进入主页面的配置页面
    比如 可以选择窗口的大小  i.e： 600 * 600
    保存的文件路径，或者选择读取文件的路径，或者一个空画布 等等
"""

# todo  熊凯奇

from tkinter import *
from tkinter.filedialog import askdirectory


def select_path():
    path_ = askdirectory()
    path.set(path_)


def print_path():
    print(path.get())
    path.set('')


if __name__ == '__main__':
    root = Tk()
    root.title("hello")
    root.geometry("360x200")

    shapeFrame = LabelFrame(root)
    shapeFrame.pack(side=TOP, padx=10, pady=10)
    newLabel = Label(shapeFrame, text='新建画布:', font=('Arial', 10)).pack(side=LEFT, padx=10, pady=5)

    lengthFrame = Frame(shapeFrame)
    lengthFrame.pack(side=TOP, padx=10, pady=10)
    length = StringVar()

    lengthLabel = Label(lengthFrame, text="画布长:").pack(side=LEFT, padx=2, pady=5, anchor=W)
    lengthEntry = Entry(lengthFrame, textvariable=length).pack(side=LEFT, padx=2, pady=5, anchor=W)

    widthFrame = Frame(shapeFrame)
    widthFrame.pack(side=TOP, padx=10, pady=10)
    width = StringVar()
    widthLabel = Label(widthFrame, text="画布宽:").pack(side=LEFT, padx=2, pady=5, anchor=W)
    widthEntry = Entry(widthFrame, textvariable=width).pack(side=LEFT, padx=2, pady=5, anchor=W)

    pathChoose = LabelFrame(root)
    pathChoose.pack(side=TOP, padx=10, pady=10)
    path = StringVar()
    pathLabel = Label(pathChoose, text="选择画布:").pack(side=LEFT, padx=2, pady=5, anchor=W)
    pathEntry = Entry(pathChoose, textvariable=path).pack(side=LEFT, padx=2, pady=5, anchor=W)
    chooseBtn = Button(pathChoose, text="路径选择", command=select_path).pack(side=LEFT, padx=0, pady=5, anchor=W)
    msBtn = Button(pathChoose, text="确认", command=print_path).pack(side=LEFT, padx=0, pady=5, anchor=W)
    root.mainloop()

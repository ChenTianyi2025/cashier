import tkinter as tk
import xlrd
import datetime

# 初始化文件和变量
fp = None
thingxls = None
allmoney = 0
ifhave_thingnum = 1
thingnum = 0
thingnum_list = []
thingname_list = []
thingname = 0
thingmoney_list = []
thingmany = 0
path_xls = r'F:\cty.xls'
path_txt = r'F:\cty.txt'

try:
    fp = open(path_txt, 'a+')
except IOError as e:
    print(f"无法打开文件：{e}")

try:
    thingxls = xlrd.open_workbook(path_xls)
except IOError as e:
    print(f"无法打开Excel文件：{e}")

# 收银记录下载函数
def print_in_txt():
    global allmoney
    print('Time:'+datetime.datetime.now().strftime('%y-%m-%d %H:%M')+"  ThingNum:", end='', file=fp)
    for item in thingnum_list:
        print(item, end="  ", file=fp)
    print("Total:", allmoney, file=fp)

# 重置交易数据函数
def reset_transaction_data():
    global allmoney, thingmany, thingnum_list, thingname_list, thingmoney_list
    allmoney = 0
    thingmany = 0
    thingnum_list.clear()
    thingname_list.clear()
    thingmoney_list.clear()

# 按钮点击事件处理函数
def button_click_finishi():
    global allmoney  # 使用全局变量allmoney
    label.config(text=f"总金额：{allmoney}")  # 更新label显示allmoney的值

def button_click_print():
    global allmoney, thingmany
    # 打印小票信息
    for i in range(thingmany):
        print(thingname_list[i], thingmoney_list[i])
    print("-----------------------------")
    print("Allmoney is:", allmoney,"\n")
    print_in_txt()
    reset_transaction_data()  # 调用重置交易数据的函数

def button_click_thingok():
    global allmoney, thingmany  # 声明allmoney和thingmany为全局变量
    try:
        thingnum = entry.get()
        thingnum = int(thingnum)  # 尝试将输入转换为整数
    except ValueError:
        label.config(text="输入的条形码数字码无效，请输入数字！")
        return

    if thingxls is not None:
        sheet = thingxls.sheet_by_index(0)
        ifhave_thingnum = 1
        ifthing = int(thingnum)
        for i in range(sheet.nrows):
            thing = sheet.cell(i, 0).value
            if thing == ifthing:
                onemoney = sheet.cell(i, 1).value
                allmoney += onemoney  # 更新全局变量allmoney
                thingnum_list.append(thingnum)
                thingname = sheet.cell(i, 2).value  # mane
                thingname_list.append(thingname)
                thingmoney_list.append(onemoney)
                ifhave_thingnum = 2
                thingmany += 1  # 使用全局变量thingmany
                entry.delete(0, tk.END)  # 清除文本框
                break  # 找到后跳出循环
        if ifhave_thingnum == 2:
            label.config(text=f"已添加 {thingname} , 单价 {onemoney} 元")
        else:
            label.config(text=f"没有 {thingnum}")
    else:
        label.config(text="Excel文件未成功打开，请检查文件路径和文件完整性。")

# 创建主窗口
root = tk.Tk()
root.title("收银系统")  # 设置窗口标题
root.geometry("400x300")  # 设置窗口大小为 400x300 像素

# 创建一个标签，并将其添加到窗口中
label = tk.Label(root, text="请输入条形数字码：")
label.pack(pady=10)  # 使用 pack() 布局管理器，添加一些垂直间距

# 创建一个文本框，并将其添加到窗口中
entry = tk.Entry(root)
entry.pack(pady=10)  # 使用 pack() 布局管理器，添加一些垂直间距
entry.bind('<Return>', lambda event: button_click_thingok())  # 绑定回车键事件

# 创建一个按钮，并将其添加到窗口中
button_thingok = tk.Button(root, text="录入一个商品", command=button_click_thingok)  # 创建一个录入商品按钮
button_thingok.pack(pady=10)  # 使用 pack() 布局管理器，添加一些垂直间距
button_finish = tk.Button(root, text="查询总金额", command=button_click_finishi)  # 创建一个完成按钮
button_finish.pack(pady=10)  # 使用 pack() 布局管理器，添加一些垂直间距
button_print = tk.Button(root, text="结束交易并打印小票", command=button_click_print)  # 创建一个打印按钮
button_print.pack(pady=10)  # 使用 pack() 布局管理器，添加一些垂直间距

try:
    # 运行主事件循环
    root.mainloop()
finally:
    # 确保资源释放
    if fp is not None:
        fp.close()
    if thingxls is not None:
        thingxls.release_resources()
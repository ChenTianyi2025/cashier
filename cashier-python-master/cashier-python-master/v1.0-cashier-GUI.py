import tkinter as tk
import xlrd
import datetime
import json

# 初始化文件和变量
log_txt_fp = None
thing_xls_fp = None
settingslog_json_fp = None
allmoney = 0
ifhave_thingnum = 1
thingnum = 0
thingnum_list = []
thingname_list = []
thingname = 0
thingmoney_list = []
thingmany = 0
path_xls = r'F:\\cty.xls'
path_txt = r'F:\\cty.txt'
path_settingslog_json = r"F:\\log.json"

try:
    log_txt_fp = open(path_txt, 'a+')
except IOError as e:
    print(f"无法打开文件：{e}")

try:
    thing_xls_fp = xlrd.open_workbook(path_xls)
except IOError as e:
    print(f"无法打开Excel文件：{e}")

try:
    settingslog_json_fp = open(path_settingslog_json, 'a+', encoding='utf-8')
except IOError as e:
    print(f"无法打开文件：{e}")

# 收银记录下载函数
def print_in_txt():
    global allmoney
    print('Time:'+datetime.datetime.now().strftime('%y-%m-%d %H:%M')+"  ThingNum:", end='', file=log_txt_fp)
    for item in thingnum_list:
        print(item, end="  ", file=log_txt_fp)
    print("Total:", allmoney, file=log_txt_fp)

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

    if thing_xls_fp is not None:
        sheet = thing_xls_fp.sheet_by_index(0)
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

def next_step():
    pwsd = entry_pwsd.get()
    if(password_set_or_cheak(pwsd, 1) == True):
        #继续
        #TODO
    else:
        label_pwsd["text"] = "密码错误！重新输入"

def password_set_or_cheak(password, state):
    # 设置或检查密码
    # input: password, state -> output: true/false
    # state: 0 - 设置密码; state: 1 - 检查密码
    # 加密 set_pwsd = (password + 1) *7 - password
    if(state == 0):
        # 设置密码
        set_pwsd = (password + 1) *7 - password #简单加密
    else:
        # 检查密码
        goal_pwsd = read_json_file()["password__<>"]
        new_pwsd = (password + 1) *7 - password 
        if(new_pwsd == goal_pwsd):
            return True
        else:
            return False


def read_json_file():
    """读取 JSON 文件并返回解析后的字典"""
    try:
        data = json.load(settingslog_json_fp)  # 解析 JSON 数据
        return data
    except FileNotFoundError:
        print(f"错误：json文件不存在！")
        return None
    except json.JSONDecodeError:
        print("错误：文件内容不是有效的 JSON 格式！")
        return None

def settings():
    # 创建新窗口
    new_window = tk.Toplevel(root)
    new_window.title("设置")  # 设置窗口标题
    new_window.geometry("400x300")  # 设置窗口大小为 400x300 像素
    # 创建菜单栏
    menubar = tk.Menu(new_window)
    new_window.config(menu=menubar)
    # 创建退出菜单
    menubar.add_cascade(label="退出", command=new_window.quit)

    # 创建标签
    label_pwsd = tk.Label(new_window, text="请输入密码")
    label_pwsd.pack(pady=10)

    # 创建文本框
    entry_pwsd = tk.Entry(new_window)
    entry_pwsd.pack(pady=10)

    # 创建按钮
    button_go = tk.Button(new_window, text="确定", command=next_step)
    button_go.pack(pady=10)

# 创建主窗口
root = tk.Tk()
root.title("收银系统")  # 设置窗口标题
root.geometry("400x300")  # 设置窗口大小为 400x300 像素

# 创建菜单栏
menubar = tk.Menu(root)
root.config(menu=menubar)
# 创建菜单
# 添加菜单项--退出
menubar.add_cascade(label="退出", command=root.quit)
# 添加菜单项--设置
menubar.add_cascade(label="设置", command=settings)

# 创建一个标签，并将其添加到窗口中
label = tk.Label(root, text="请输入条形数字码：")
label.pack(pady=10)  # 使用 pack() 布局管理器，添加一些垂直间距

# 创建一个文本框，并将其添加到窗口中
entry = tk.Entry(root)
entry.pack(pady=10)  # 使用 pack() 布局管理器，添加一些垂直间距
entry.bind('<Return>', lambda event: button_click_thingok())  # 绑定回车键事件

# 创建一个按钮，并将其添加到窗口中
button_thingok = tk.Button(root, text="加入商品（Enter）", command=button_click_thingok)  # 创建一个录入商品按钮
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
    if log_txt_fp is not None:
        log_txt_fp.close()
    if thing_xls_fp is not None:
        thing_xls_fp.release_resources()
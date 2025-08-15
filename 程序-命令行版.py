import datetime
import xlrd

fp = open(r'F:\cty.txt','a+')
thingxls = xlrd.open_workbook('F:\cty.xls') #excel
allmoney = 0
ifhave_thingnum = 1
close_num = "kl" #kl
run = 3
thingnum_list = []
thingname_list = []
thingname = 0
thingmoney_list = []
thingmany = 0


while True:
    thingnum = input("请输入条形数字码：(输入ks可更改退出符 现在的退出符是"+close_num+")")
    if thingnum == "ks":
        close_num = input("请输入新的退出符 默认kl:")
    else:
        if thingnum == close_num:
            break
        else:
            sheet = thingxls.sheet_by_index(0)
            i = 1
            ifhave_thingnum = 1
            ifthing = int(thingnum)
            for i in range(sheet.nrows):
                thing = sheet.cell(i,0).value
                if (thing == ifthing):
                    onemoney = sheet.cell(i,1).value #单价
                    allmoney = allmoney + onemoney
                    thingnum_list.append(thingnum)
                    thingname = sheet.cell(i,2).value #mane
                    thingname_list.append(thingname)
                    thingmoney_list.append(onemoney)
                    ifhave_thingnum = 2
                    thingmany += 1
                    print(onemoney)
            if ifhave_thingnum == 2:
                print('time:'+datetime.datetime.now().strftime('%y-%m-%d %H:%M')+"  thingnum:"+thingnum,end="\n\n")
            else:
                print("NO this 没有"+thingnum+"商品",end="\n\n")

print('Time:'+datetime.datetime.now().strftime('%y-%m-%d %H:%M')+"  ThingNum:",end='',file=fp)
for item in thingnum_list:
    print(item,end="  ",file=fp)
print("Allmaney is:",allmoney,file=fp)

fp.close()


for i in range(thingmany):
    print(thingname_list[i],thingmoney_list[i])
print("-----------------------------")
print("Allmaney is:",allmoney)
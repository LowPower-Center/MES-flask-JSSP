import matplotlib.pyplot as plt

def process_data(str1):







    s=str1.split("-")
    ret=s[0].replace("."," ").split("][")
    PT=(ret[0]+"]").replace(" ",",").replace("[",",").replace("]",",").split(",")
    MT=("["+ret[1]).replace(" ",",").replace("[",",").replace("]",",").split(",")
    ST=(s[4]).replace(" ",",").replace("[",",").replace("]",",").split(",")
    MT_item=[]
    PT_item=[]
    ST_item=[]
    for i in MT:
        if i:
            MT_item.append(i)
    for i in PT:
        if i:
            PT_item.append(i)
    for i in ST:
        if i :
            ST_item.append(i)
    # print(eval(PT))
    print(MT_item,PT_item,ST_item)
    markspan=eval(s[1])
    n=eval(s[2])
    m=eval(s[3])

    print(markspan,n,m)
    PT=[]
    MT=[]
    ST=[]
    for i in range(m):
        PT_tmp = []
        MT_tmp = []
        ST_tmp=[]
        for j in range(n):
            PT_tmp.append(eval(PT_item[i*n+j]))
            MT_tmp.append(eval(MT_item[i*n+j])//m)
            ST_tmp.append(eval(ST_item[i * n + j]))
        PT.append(PT_tmp)
        MT.append(MT_tmp)
        ST.append(ST_tmp)
    print(MT,PT,ST)

    plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体,则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus'] = False  # 显示负号
    M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
         'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
         'navajowhite', 'navy', 'sandybrown', 'moccasin']
    Job_text = ['J' + str(i + 1) for i in range(100)]
    Machine_text = ['M' + str(i + 1) for i in range(50)]

    print(Job_text)
    for i in range(m):
        for j in range(len(ST[i])):
            if PT[i][j] - ST[i][j] != 0:
                plt.barh(i, width=PT[i][j] - ST[i][j],
                         height=0.8, left=ST[i][j],
                         color=M[MT[i][j]],
                         edgecolor='black')
                plt.text(x=ST[i][j] + (PT[i][j] - ST[i][j]) / 2 - 0.1,
                         y=i,
                         s=Job_text[MT[i][j]],
                         fontsize=12)
    plt.savefig("../static/gantti.png")
    # plt.show()

    return PT,MT,ST
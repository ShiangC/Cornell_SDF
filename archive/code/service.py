from tkinter import *
from Rhodium_Model.trade_speace_rhodium import TradeSpaceRhodium
from Decision_Model.tradespace_explore import Tradespace
from Decision_Model.decision_model import Decision
import hashlib
import time
import sys

LOG_LINE_NUM = 0

class RedirectText(object):

    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        self.output.insert(END, string)


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.index = 0
        self.priceVector = {
                                'yield': 100,
                                'electricity': 10,
                                'water': 5,
                                'pesticides': 50,
                                'labor': 300
                            }
        self.rhodium = TradeSpaceRhodium()



    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("Trade Space Exploration for The SDF")
        # self.init_window_name.geometry('320x160+10+10')
        self.init_window_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        # 标签
        self.init_data_label = Label(self.init_window_name, text="Farm Parameters")
        self.init_data_label.grid(row=0, column=0)
        self.corp_lbl = Label(self.init_window_name, text="Corp Type")
        self.corp_lbl.grid(row=2, column=0)
        self.numOfUsers_lbl = Label(self.init_window_name, text="Number of Users")
        self.numOfUsers_lbl.grid(row=3, column=0)
        self.latitude_lbl = Label(self.init_window_name, text="Latitude")
        self.latitude_lbl.grid(row=4, column=0)
        self.sampleEn_lbl = Label(self.init_window_name, text="Climate Entropy")
        self.sampleEn_lbl.grid(row=5, column=0)
        self.rainfall_lbl = Label(self.init_window_name, text="Precipitation")
        self.rainfall_lbl.grid(row=6, column=0)
        self.result_data_label = Label(self.init_window_name, text="Output")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="Log")
        self.log_label.grid(row=12, column=0)
        #文本框
        self.corp_txt = Text(self.init_window_name, width=10, height=1)
        self.corp_txt.grid(row=2, column=1, rowspan=1, columnspan=1)
        self.corp_txt.insert(INSERT, '0')
        self.numOfUsers_txt = Text(self.init_window_name, width=10, height=1)
        self.numOfUsers_txt.grid(row=3, column=1, rowspan=1, columnspan=1)
        self.numOfUsers_txt.insert(INSERT, '1000')
        self.latitude_txt = Text(self.init_window_name, width=10, height=1)
        self.latitude_txt.grid(row=4, column=1, rowspan=1, columnspan=1)
        self.latitude_txt.insert(INSERT, '45')
        self.sampleEn_txt = Text(self.init_window_name, width=10, height=1)
        self.sampleEn_txt.grid(row=5, column=1, rowspan=1, columnspan=1)
        self.sampleEn_txt.insert(INSERT, '2')
        self.rainfall_txt = Text(self.init_window_name, width=10, height=1)
        self.rainfall_txt.grid(row=6, column=1, rowspan=1, columnspan=1)
        self.rainfall_txt.insert(INSERT, '1303')
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        redir = RedirectText(self.result_data_Text)
        sys.stdout = redir


        #按钮
        self.enumeration_btn = Button(self.init_window_name, text="Enumeration", bg="lightblue", width=10,
                                      command=self.trade_space_enum, state=NORMAL)
        self.enumeration_btn.grid(row=5, column=11)
        self.optimize_btn = Button(self.init_window_name, text="Optimize", bg="lightblue", width=10,
                                      command=self.trade_space_optimize, state=DISABLED)
        self.optimize_btn.grid(row=6, column=11)
        self.setup_btn = Button(self.init_window_name, text="Update Model", bg="lightblue", width=10,
                                   command=self.rhodium_setup, state=DISABLED)
        self.setup_btn.grid(row=7, column=11)

    def trade_space_enum(self):
        print("******************** Enumerating ********************")
        self.index += 1
        self.ts = Tradespace(0, self.priceVector)
        self.enum = self.ts.tradeSpace
        self.nodes = self.ts.TS_nodes
        print('Number of Policies found: ' + str(len(self.enum)))
        self.enumeration_btn['state'] = DISABLED
        self.optimize_btn['state'] = NORMAL
        self.log_data_Text.insert(INSERT, "[ "+ str(self.index) +" ]" + " Finished Tradespace Enumeration, results saved to results/tradespace_enumeration.csv\n")

    def trade_space_optimize(self):
        print("******************** Calculating Pareto Front ********************")
        self.index += 1
        self.pareto_set = self.ts.calcPareto()
        self.ts.plotTS(self.pareto_set)
        self.setup_btn['state'] = NORMAL
        self.log_data_Text.insert(INSERT, "[ "+str(self.index) + " ]" + " Graphed the Tradespace Enumeration and the Pareto Set.\n")

    def rhodium_setup(self):
        self.index += 1
        print("******************** Updating Rhodium Model ********************")
        self.model = self.rhodium.setupModel(self.rhodium.farm_approach2,
                                             self.pareto_set,
                                             int(self.numOfUsers_txt.get("0.0", END)),
                                             int(self.latitude_txt.get("0.0", END)),
                                             int(self.sampleEn_txt.get("0.0", END)),
                                             int(self.rainfall_txt.get("0.0", END)),
                                             int(self.corp_txt.get("0.0", END)))
        self.log_data_Text.insert(INSERT, "[ "+str(self.index) +" ]" + " Updated Rhodium Model.\n")

    #功能函数
    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0,END).strip().replace("\n","").encode()
        #print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                #print(myMd5_Digest)
                #输出到界面
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,myMd5_Digest)
                self.write_log_to_Text("INFO:str_trans_to_md5 success")
            except:
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,"字符串转MD5失败")
        else:
            self.write_log_to_Text("ERROR:str_trans_to_md5 failed")


    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


def main():
    gui_start()


# if __name__ == "__main__":
#      main()
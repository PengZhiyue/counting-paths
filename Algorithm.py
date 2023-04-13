# -*- coding: utf-8 -*-
# @Time    : 2023/4/8 20:14
# @Author  : Bernard
# @File    : Algorithm.py
import pandas as pd
import configparser

class Run(object):
    def __init__(self, K=2, delta=2):
        '''
        初始化
        :param K: K的数值
        :param delta: δ的数值
        '''
        self.K = K
        self.delta = delta
        self.D = []
        self.c = None
        self.w = None

    def algorithm(self):
        '''
        计算数据 D 中最多 K 步长的所有因果路径的出现次数
        :return:None
        '''
        D = self.D
        delta = self.delta
        K = self.K
        N = len(D)
        c = {}
        W = []
        W_all = []
        for i in range(N):
            s, d, t = D[i]
            ci = dict()
            ci[f"{s}{d}"] = 1
            W_temp = W[:]
            for j in range(len(W)):
                sj, dj, tj, cj = W[j]
                if tj < t - delta:
                    W_temp.remove((sj, dj, tj, cj))
                else:
                    if dj == s and t > tj:
                        for p in cj.keys():
                            if self.path_length(p) < K:
                                if p + d not in ci.keys():
                                    ci[p + d] = cj[p]
                                else:
                                    ci[p + d] = ci[p + d] + cj[p]
            W = W_temp[:]

            for p in ci.keys():
                if p not in c.keys():
                    c[p] = ci[p]
                else:
                    c[p] = c[p] + ci[p]

            W.append((s, d, t, ci))
            W_all.append((s, d, t, ci))

        self.c = c
        self.w = W_all

    def path_length(self, p):
        '''
        计算路径 p 的路径长度
        :param p: 路径
        :return: 路径长度
        '''
        return len(p) - 1


    def loadData(self, num=16):
        '''
        加载数据
        :param num: 最大时刻，即加载的数量
        :return: None
        '''
        D = []
        for time in range(1, num + 1):
            df = pd.read_excel(f'./data/时刻{time}.xlsx')
            source = df['source']
            target = df['target']
            temp = []
            for i, s in enumerate(source):
                l = [s, target[i], time]
                temp.append(l)
            D = D + temp
        self.D = D


    def save(self):
        '''
        保存 causal paths 表格 和 W 表格
        :return: None
        '''
        K = self.K
        delta = self.delta

        # causal paths
        keys = self.c.keys()
        values = self.c.values()
        causal_path_df = pd.DataFrame()
        causal_path_df['path'] = keys
        causal_path_df['amount'] = values
        causal_path_df.to_csv(f'causal path K{K} delta{delta}.csv', index=False, encoding='utf-8')

        # W
        s_list = []
        d_list = []
        t_list = []
        c_list = []
        for i in range(len(self.w)):
            s, d, t, c = self.w[i]
            s_list.append(s)
            d_list.append(d)
            t_list.append(t)
            c_list.append(str(c).replace("{", "").replace("}", ""))

        W_df = pd.DataFrame()
        W_df['si'] = s_list
        W_df['di'] = d_list
        W_df['ti'] = t_list
        W_df['ci'] = c_list
        W_df.to_csv(f'W K{K} delta{delta}.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    '''
    K 的数值 跟 δ 的数值 在此设定
    delta 即 δ
    num 加载多少张表格，默认16，即加载所有表格的数据
    '''
    # delta = 3
    # K = 3

    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    delta = config.getint('section1', 'delta')
    K = config.getint('section1', 'K')
    num = config.getint('section1', 'num')

    print(f'K is {K}')
    print(f'delta is {delta}')
    print(f'num is {num}')

    print(f'start')
    run = Run(K=K, delta=delta)
    print(f'data Loading')
    run.loadData(num=num)  # 默认16，即加载所有表格的数据
    print(f'algorithm')
    run.algorithm()
    print(f'save data')
    run.save()
    # 命名规则：
    # causal path K“K的数值” delta“δ的数值”.csv
    # W K“K的数值” delta“δ的数值”.csv
    print(f'finish')






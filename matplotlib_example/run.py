#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2020/4/20 2:23 下午
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : run.py

# 导入库文件
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# from IPython.display import HTML
import matplotlib

from pyecharts.render.display import HTML

# 防止动漫内存太大，报错
matplotlib.rcParams['animation.embed_limit'] = 2 ** 128
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']


def random_color():
    """
    导入random函数，random_color用于生成颜色代码
    random_color生成颜色代码原理，
    【1-9/A-F】15个数字随机组合成6位字符串前面再加上一个“#”号键
    """
    cl = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ''
    for i in range(6):
        color += random.choice(cl)
    return '#' + color


def gen_data(current_date):
    """
    裁剪数据
    """
    df2 = df[df['date'].eq(current_date)]
    df3 = df2.groupby(by=['country']).head(1)
    df4 = df3.sort_values(by='confirmed', ascending=True).tail(10)
    return df4


def draw_bar_chart(current_date):
    """
    画横向柱状图
    """
    title = '全球各国新型冠状病例确诊数增长变化'
    author = 'by@Annihilater'
    df5 = gen_data(current_date)

    # 清除坐标标签
    ax.clear()
    ax.barh(df5['country'], df5['confirmed'], color=[colors[x] for x in df5['country']])
    for i, (name, value) in enumerate(zip(df5['country'], df5['confirmed'])):
        ax.text(value, i, f'{value:,.0f}', size=14, ha='left', va='center')
    # 设置标题
    ax.text(0, 1.05, title, transform=ax.transAxes, size=30, weight=600, ha='left', va='top')
    # 设置作者
    ax.text(1, 0.1, author, transform=ax.transAxes, color='#777777', size=18, ha='right',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    # 画布右中添加年份
    ax.text(1, 0.4, current_date, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)

    plt.yticks(fontsize=20)
    plt.box(False)


df = pd.read_csv('../source_data.csv', usecols=['date', 'country', 'confirmed'])

# 生成字典: {国家: 颜色}
country_list = set(df['country'])
color_list = []
for i in range(len(country_list)):
    color_list.append(random_color())
colors = dict(zip(country_list, color_list))

# 生成日期时序
date_list = list(set(df['date']))
date_list.sort()

# 将原来的静态图拼接成动画
fig, ax = plt.subplots(figsize=(15, 8))
animator = animation.FuncAnimation(fig, draw_bar_chart, frames=date_list[-20:])  # 保存到jshtml
HTML(animator.to_jshtml())

# 生成video，并保存至指定文件夹中
animator.to_html5_video()
animator.save('global_coronavirus_numbers.mp4')

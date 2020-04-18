#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2020/4/17 2:54 下午
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : main.py


# 整理数据
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

time_span = 20


def gen_data(path):
    df = pd.read_csv(path)
    # print(df.info())
    # print(df.head())
    df = df[['date', 'country', 'confirmed']]
    # print(df.head())
    UK = df[df['country'] == '英国']['confirmed'].to_list()[-time_span:]
    Italy = df[df['country'] == '意大利']['confirmed'].to_list()[-time_span:]
    US = df[df['country'] == '美国']['confirmed'].to_list()[-time_span:]
    Spain = df[df['country'] == '西班牙']['confirmed'].to_list()[-time_span:]
    Germany = df[df['country'] == '德国']['confirmed'].to_list()[-time_span:]
    Iran = df[df['country'] == '伊朗']['confirmed'].to_list()[-time_span:]
    Korea = df[df['country'] == '韩国']['confirmed'].to_list()[-time_span:]
    France = df[df['country'] == '法国']['confirmed'].to_list()[-time_span:]
    Switzerland = df[df['country'] == '瑞士']['confirmed'].to_list()[-time_span:]
    date = df[df['country'] == '英国']['date'].to_list()[-time_span:]
    for i in range(len(date)):
        date[i] = date[i][6:]
        # print(date[i])

    c = {"英国": UK,
         '美国': US,
         '意大利': Italy,
         '西班牙': Spain,
         '德国': Germany,
         '伊朗': Iran,
         '韩国': Korea,
         '法国': France,
         '瑞士': Switzerland, }
    df1 = pd.DataFrame(c)
    # print(df1)
    # print(date)
    return df1, date


def get_value(df1, k):
    data = df1.loc[k].to_list()
    k = k + 1
    return data, k


def gen_bar(x, y, i):
    _bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
            .add_xaxis(x)
            .add_yaxis("确诊人数", y)
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='right', color='auto'))
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=True),
            title_opts=opts.TitleOpts("{}".format(i)),
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(rotation=JsCode("Math.PI / 4"),
                                                  bounding="raw",
                                                  right=100,
                                                  bottom=110,
                                                  z=100,
                                                  ),
                    children=[opts.GraphicRect(graphic_item=opts.GraphicItem(left="center", top="center", z=100),
                                               graphic_shape_opts=opts.GraphicShapeOpts(width=400, height=50),
                                               graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                                   fill="rgba(0,0,0,0.3)"),
                                               ),
                              opts.GraphicText(graphic_item=opts.GraphicItem(left="center", top="center", z=100),
                                               graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                                   text="重点国家{}日数据".format(i),
                                                   font="bold 26px Microsoft YaHei",
                                                   graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(fill="#fff"), ),
                                               ),
                              ],
                )
            ],
        )
    )
    return _bar


def main():
    df1, date = gen_data('全球疫情历史数据.csv')
    tl = Timeline()
    tl.add_schema(is_auto_play=True,
                  play_interval=500,
                  is_loop_play=True)

    k = 0
    for i in date:
        # data = get_value(df1, k)[0]
        x = df1.columns.to_list()
        y = get_value(df1, k)[0]
        s = {"国家": x,
             "数量": y}
        tem = pd.DataFrame(s)
        tem = tem.sort_values(by="数量", ascending=True)
        x = tem['国家'].to_list()
        y = tem['数量'].to_list()

        k = get_value(df1, k)[1]
        bar = gen_bar(x, y, i)
        tl.add(bar, "".format(i))
    tl.render_notebook()
    tl.render("timeline_bar_with_graphic.html")


if __name__ == '__main__':
    main()

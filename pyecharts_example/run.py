#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2020/4/17 2:54 下午
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : run.py


import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType


def get_data(df, current_date):
    df1 = df[df['date'].eq(current_date)]
    df2 = df1.groupby(by='country').head(1)
    df3 = df2.sort_values(by='confirmed').tail(10)
    return df3


def draw_bar(df, date_list, tl):
    for date in date_list:
        _date = date[-5:]
        df4 = get_data(df, date)
        x = df4['country'].to_list()
        y = df4['confirmed'].to_list()

        bar = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMANTIC))
                .add_xaxis(x)
                .add_yaxis("确诊人数", y)
                .reversal_axis()
                .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='right'),
                                 )
                .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=True),
                title_opts=opts.TitleOpts("{} Day".format(_date)),
                graphic_opts=[
                    opts.GraphicGroup(
                        graphic_item=opts.GraphicItem(
                            rotation=JsCode("Math.PI / 4"),
                            bounding="raw",
                            right=100,
                            bottom=110,
                            z=100,
                        ),
                        children=[
                            opts.GraphicRect(
                                graphic_item=opts.GraphicItem(left="center", top="center", z=100),
                                graphic_shape_opts=opts.GraphicShapeOpts(width=400, height=50),
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(fill="rgba(0,0,0,0.3)"),
                            ),
                            opts.GraphicText(
                                graphic_item=opts.GraphicItem(left="center", top="center", z=100),
                                graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                    text="重点国家{}日数据".format(_date),
                                    font="bold 26px Microsoft YaHei",
                                    graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(fill="#fff"),
                                ),
                            ),
                            opts.GraphicImage(
                                graphic_item=opts.GraphicItem(left="center", top="center", z=100),
                                graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                                    graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(fill='#fff'))),
                        ],
                    )
                ],
            )
        )
        tl.add(bar, "{}".format(_date))


def main():
    df = pd.read_csv('../source_data.csv', usecols=['date', 'country', 'confirmed'])

    # 获取顺序的日期列表
    date_list = list(set(df['date'].to_list()))
    date_list.sort()
    date_list = date_list[-20:]

    tl = Timeline()
    tl.add_schema(is_auto_play=False,
                  play_interval=500,
                  is_loop_play=False)
    draw_bar(df, date_list, tl)
    tl.render_notebook()
    tl.render("timeline_bar_with_graphic.html")


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:35:40 2022

@author: Yuwen.Fang
"""

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objs as go
import numpy as np
import streamlit as st  # pip install streamlit


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="迪化廠資料", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def BOD_get_data():
    file_name = '11012報表之圖表區-增訂需管控項目.xlsx'
    sheet_name = '總表new'

    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,G,W,AE,AL,BS,CO,DR,DY,GI")
    df.columns = ['日期','進流渠道','初沉池進','初沉池出','迴流液匯合池流量計',
                  '二沈池出水','放流水','回收水','帶濾式污泥濃縮機濾液','緊急排水']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith('110/12/', na=False)]
    df['回收水'] = df['回收水'].replace(['停機'], float(0.0))
    df['帶濾式污泥濃縮機濾液'] = df['帶濾式污泥濃縮機濾液'].replace(['停機'], float(0.0))
    df = df.fillna(0.0)
    return df

def COD_get_data():
    file_name = '11012報表之圖表區-增訂需管控項目.xlsx'
    sheet_name = '總表new'

    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,H,X,AF,AM,BT,CP,DS,DZ,GJ")
    df.columns = ['日期','進流渠道','初沉池進','初沉池出','迴流液匯合池流量計',
                  '二沈池出水','放流水','回收水','帶濾式污泥濃縮機濾液','緊急排水']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith('110/12/', na=False)]
    df['回收水'] = df['回收水'].replace(['停機'], float(0.0))
    df['帶濾式污泥濃縮機濾液'] = df['帶濾式污泥濃縮機濾液'].replace(['停機'], float(0.0))
    df = df.fillna(0.0)
    return df

def ss_get_data():
    file_name = '11012報表之圖表區-增訂需管控項目.xlsx'
    sheet_name = '總表new'

    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,I,Y,AG,AK,AU,AV,AW,AX,BF,BG,BH,BI,BU,CF,CG,CQ,DT,EJ,EK,EQ,ES,FH,FI,FQ,FS,GA,GH")
    df.columns = ['日期','進流渠道','初沉池進','初沉池出','迴流液匯合池流量計',
                  '初沉污泥-1','初沉污泥-1(揮發性)','初沉污泥-2','初沉污泥-2(揮發性)',
                  '深層階段曝氣槽-好氧','深層階段曝氣槽-缺氧','深層階段曝氣槽-好氧(揮發性)',
                  '深層階段曝氣槽-缺氧(揮發性)','二沈池出水','迴流污泥','迴流污泥(揮發性)',
                  '放流水','回收水','帶濾式濃縮機進流污泥','帶濾式濃縮機進流污泥(揮發性)',
                  '厭氧消化槽進流污泥','厭氧消化槽進流污泥(揮發性)','厭氧消化槽出流污泥',
                  '厭氧消化槽出流污泥(揮發性)','帶濾式脫水機進流污泥','帶濾式脫水機進流污泥(揮發性)',
                  '帶濾式脫水機濾液','緊急排水']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith('110/12/', na=False)]
    df['回收水'] = df['回收水'].replace(['停機'], float(0.0))
    df['帶濾式濃縮機進流污泥'] = df['帶濾式濃縮機進流污泥'].replace(['停機'], float(0.0))
    df['帶濾式濃縮機進流污泥(揮發性)'] = df['帶濾式濃縮機進流污泥(揮發性)'].replace(['停機'], float(0.0))
    df['厭氧消化槽進流污泥'] = df['厭氧消化槽進流污泥'].replace(['停機'], float(0.0))
    df['厭氧消化槽進流污泥(揮發性)'] = df['厭氧消化槽進流污泥(揮發性)'].replace(['停機'], float(0.0))
    df['厭氧消化槽出流污泥'] = df['厭氧消化槽出流污泥'].replace(['停機'], float(0.0))
    df['厭氧消化槽出流污泥(揮發性)'] = df['厭氧消化槽出流污泥(揮發性)'].replace(['停機'], float(0.0))
    df['帶濾式脫水機進流污泥'] = df['帶濾式脫水機進流污泥'].replace(['停機'], float(0.0))
    df['帶濾式脫水機進流污泥(揮發性)'] = df['帶濾式脫水機進流污泥(揮發性)'].replace(['停機'], float(0.0))
    df['帶濾式脫水機濾液'] = df['帶濾式脫水機濾液'].replace(['停機'], float(0.0))
    df['緊急排水'] = df['緊急排水'].replace(['停機'], float(0.0))
    df = df.fillna(0.0)
    return df

def removal_rate_get_data():
    file_name = '11012報表之圖表區-增訂需管控項目.xlsx'
    sheet_name = '總表new'

    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,AO,AP,AQ,DC,DB,DA,DD,DU,DV,DW")
    df.columns = ['日期','初沉池-BOD','初沉池-COD','初沉池-ss',
                  '全廠-BOD','全廠-COD','全廠-ss','全廠-氨氮',
                  '回收水-BOD','回收水-COD','回收水-ss']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith('110/12/', na=False)]
    num = df._get_numeric_data()
    num[num < 0] = np.nan
    df['全廠-氨氮'] = df['全廠-氨氮'].replace(['-'], np.nan)
    df['回收水-BOD'] = df['回收水-BOD'].replace(['--'], np.nan)
    df['回收水-COD'] = df['回收水-COD'].replace(['--'], np.nan)
    df['回收水-ss'] = df['回收水-ss'].replace(['--'], np.nan)
    df['初沉池-BOD'] = df['初沉池-BOD']*100
    df['初沉池-COD'] = df['初沉池-COD']*100
    df['初沉池-ss'] = df['初沉池-ss']*100
    df['全廠-BOD'] = df['全廠-BOD']*100
    df['全廠-COD'] = df['全廠-COD']*100
    df['全廠-ss'] = df['全廠-ss']*100
    df['全廠-氨氮'] = df['全廠-氨氮']*100
    
    return df

df_BOD = BOD_get_data()
df_COD = COD_get_data()
df_ss = ss_get_data()
df_removal_rate = removal_rate_get_data()

# ---- MAINPAGE ----
st.title(":bar_chart: 迪化廠資料")
st.markdown("##")


# BOD [LINE CHART] --------------------
fig_BOD = px.line(df_BOD, x='日期', y=['進流渠道','初沉池進','初沉池出','迴流液匯合池流量計',\
                                      '二沈池出水','放流水','回收水','帶濾式污泥濃縮機濾液','緊急排水'], orientation="h",
                  title="<b>生化需氧量(BOD)</b>",template="plotly_white")
fig_BOD.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_BOD)

# COD [LINE CHART] ---------------------
fig_COD = px.line(df_COD, x='日期', y=['進流渠道','初沉池進','初沉池出','迴流液匯合池流量計','二沈池出水','放流水','回收水','帶濾式污泥濃縮機濾液','緊急排水'], orientation="h",
                  title="<b>化學需氧量(BOD)</b>",template="plotly_white")
fig_BOD.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_COD)

# ss [LINE CHART] ---------------------
fig_ss = px.line(df_ss, x='日期', y=['進流渠道','初沉池進','初沉池出','迴流液匯合池流量計',
                                     '初沉污泥-1','初沉污泥-1(揮發性)','初沉污泥-2','初沉污泥-2(揮發性)',
                                     '深層階段曝氣槽-好氧','深層階段曝氣槽-缺氧','深層階段曝氣槽-好氧(揮發性)',
                                     '深層階段曝氣槽-缺氧(揮發性)','二沈池出水','迴流污泥','迴流污泥(揮發性)',
                                     '放流水','回收水','帶濾式濃縮機進流污泥','帶濾式濃縮機進流污泥(揮發性)',
                                     '厭氧消化槽進流污泥','厭氧消化槽進流污泥(揮發性)','厭氧消化槽出流污泥',
                                     '厭氧消化槽出流污泥(揮發性)','帶濾式脫水機進流污泥','帶濾式脫水機進流污泥(揮發性)',
                                     '帶濾式脫水機濾液','緊急排水'],
                   title="<b>懸浮固體(ss)</b>",template="plotly_white")
fig_ss.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_ss)

# removal rate [SCATTER CHART] ---------------------
fig_removal_rate = px.scatter(df_removal_rate, x='日期', y=['初沉池-BOD','初沉池-COD','初沉池-ss',
                                                 '全廠-BOD','全廠-COD','全廠-ss','全廠-氨氮',
                                                 '回收水-BOD','回收水-COD','回收水-ss'],
                   title="<b>去除率</b>",template="plotly_white")
fig_removal_rate.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_removal_rate)

#left_column, right_column = st.columns(2)
#left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
#right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
#hide_st_style = """
#            <style>
#            #MainMenu {visibility: hidden;}
#            footer {visibility: hidden;}
#            header {visibility: hidden;}
#            </style>
#            """
#st.markdown(hide_st_style, unsafe_allow_html=True)

"""
Created on Wed Oct 12 10:35:40 2022
@author: Yuwen.Fang
@Email: yuwen.fang24@gmail.com
@Project: Sewage Treatment Plant Dashboard with Streamlit
@reference: https://github.com/Sven-Bo/streamlit-sales-dashboard.git
"""

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import numpy as np
import streamlit as st  # pip install streamlit
from plotly.subplots import make_subplots

timeSelect = '110/12/'
file_name = '11012.xlsx'
sheet_name = 'raw_data'

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sewage Treatment Plant Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ---- #
@st.cache
# 進流水量&放流水量
def flow_get_data():
    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,B,CJ")
    df.columns = ['日期','進流水量','放流水量']
    df = df.assign(契約要求標準=420000)
    # 篩選(條件*1)
    df = df[df['日期'].str.startswith(timeSelect, na=False)]
    df = df.fillna(0.0)
    return df

def BOD_get_data():
    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,G,W,AE,AL,BS,CO,DR,DY,GI")
    df.columns = ['日期','進流渠道','初沉池進','初沉池出','迴流液匯合池流量計',
                  '二沈池出水','放流水','回收水','帶濾式污泥濃縮機濾液','緊急排水']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith(timeSelect, na=False)]
    df = df.replace(['停機'], float(0.0))
    df = df.fillna(0.0)
    return df

def COD_get_data():
    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,H,X,AF,AM,BT,CP,DS,DZ,GJ")
    df.columns = ['日期','進流渠道','初沉池進','初沉池出','迴流液匯合池流量計',
                  '二沈池出水','放流水','回收水','帶濾式污泥濃縮機濾液','緊急排水']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith(timeSelect, na=False)]
    df['回收水'] = df['回收水'].replace(['停機'], float(0.0))
    df['帶濾式污泥濃縮機濾液'] = df['帶濾式污泥濃縮機濾液'].replace(['停機'], float(0.0))
    df = df.fillna(0.0)
    return df

def ss_get_data():
    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,I,Y,AG,AK,AU,AV,AW,AX,BF,BG,BU,CF,CG,CQ,DT,EJ,EK,EQ,ES,FH,FI,FQ,FS,GA,GH")
    df.columns = ['日期','進流渠道','初沉池進','初沉池出','迴流液匯合池流量計',
                  '初沉污泥-1','初沉污泥-1(揮發性)','初沉污泥-2','初沉污泥-2(揮發性)',
                  '生物曝氣槽-好氧','生物曝氣槽-缺氧','二沈池出水','迴流污泥','迴流污泥(揮發性)',
                  '放流水','回收水','帶濾式濃縮機進流污泥','帶濾式濃縮機進流污泥(揮發性)',
                  '厭氧消化槽進流污泥','厭氧消化槽進流污泥(揮發性)','厭氧消化槽出流污泥',
                  '厭氧消化槽出流污泥(揮發性)','帶濾式脫水機進流污泥','帶濾式脫水機進流污泥(揮發性)',
                  '帶濾式脫水機濾液','緊急排水']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith(timeSelect, na=False)]
    df = df.replace(['停機'], float(0.0))
    df = df.fillna(0.0)
    return df

def removal_rate_get_data():
    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,AO,AP,AQ,DC,DB,DA,DD,DU,DV,DW")
    df.columns = ['日期','初沉池-BOD','初沉池-COD','初沉池-ss',
                  '全廠-BOD','全廠-COD','全廠-ss','全廠-氨氮',
                  '回收水-BOD','回收水-COD','回收水-ss']
    
    # 篩選(條件*1)
    df = df[df['日期'].str.startswith(timeSelect, na=False)]
    df = df.fillna(0.0)
    num = df._get_numeric_data()
    num[num < 0] = float(0.0)
    df = df.replace(['-'], float(0.0))
    df = df.replace(['--'], float(0.0))
    df['初沉池-BOD'] = df['初沉池-BOD']*100
    df['初沉池-COD'] = df['初沉池-COD']*100
    df['初沉池-ss'] = df['初沉池-ss']*100
    df['全廠-BOD'] = df['全廠-BOD']*100
    df['全廠-COD'] = df['全廠-COD']*100
    df['全廠-ss'] = df['全廠-ss']*100
    df['全廠-氨氮'] = df['全廠-氨氮']*100
    
    return df

#全廠本月用電量
def electricity_get_data():
    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,HM")
    df.columns = ['日期','用電量']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith(timeSelect, na=False)]
    df = df.fillna(0.0)
    return df


#本月自來水使用量
def water_get_data():
    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,KX")
    df.columns = ['日期','使用量']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith(timeSelect, na=False)]
    df = df.fillna(0.0)
    return df



def bill_get_data():
    df = pd.read_excel(file_name,
                       sheet_name,
                       skiprows=2,
                       usecols="A,NY,NZ,OA,OB")
    df.columns = ['日期','自來水總金額(元)','自來水度數(度)','台電總金額(元)','台電度數(度)']

    # 篩選(條件*1)
    df = df[df['日期'].str.startswith(timeSelect, na=False)]
    return df[0:1]
   

# ------ 各參數 -------------------------
df_flow = flow_get_data()
df_BOD = BOD_get_data()
df_COD = COD_get_data()
df_ss = ss_get_data()
df_removal_rate = removal_rate_get_data()
df_electricity = electricity_get_data()
df_water = water_get_data()
df_bill = bill_get_data()


# ---- MAINPAGE ---- #
st.title(":bar_chart: Sewage Treatment Plant Dashboard")
st.markdown("##")

# bill --------------------------------
water_money = int(df_bill["自來水總金額(元)"])
water_degree = int(df_bill["自來水度數(度)"])
electicity_money = int(df_bill["台電總金額(元)"])
electicity_degree = int(df_bill["台電度數(度)"])

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Water:")
    st.subheader(f"NTD $ {water_money:,}")
    st.subheader(f"Degree {water_degree:,}")
with right_column:
    st.subheader("Electricity:")
    st.subheader(f"NTD $ {electicity_money:,}")
    st.subheader(f"Degree {electicity_degree:,}")
#本月自來水使用量
fig_water = px.line(df_water, x='日期', y=['使用量'],
                      title="<b>自來水使用量</b>",template="plotly_white")
fig_water.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="使用量(m3)"))
)

# df_electricity [LINE CHART] ---------------------
fig_electricity = px.line(df_electricity, x='日期', y=['用電量'],
                                title="<b>全廠本月用電量</b>",template="plotly_white", width=1300)
fig_electricity.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="度"))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_water, use_container_width=True)
right_column.plotly_chart(fig_electricity, use_container_width=True) 


# flow [LINE CHART] --------------------
fig_flow = px.line(df_flow, x='日期', y=['進流水量','放流水量','契約要求標準'], orientation="h",
                  title="<b>進流水量&放流水量</b>",template="plotly_white")
fig_flow.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="CMD"))
)


# BOD [LINE CHART] --------------------
fig_BOD_1 = px.line(df_BOD, x='日期', y=['進流渠道','初沉池進','初沉池出','二沈池出水','放流水','回收水'], orientation="h",
                  title="<b>生化需氧量BOD</b>",template="plotly_white")
fig_BOD_1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="mg/L"))
)

fig_BOD_2 = px.line(df_BOD, x='日期', y=['迴流液匯合池流量計','帶濾式污泥濃縮機濾液','緊急排水'], orientation="h",
                    template="plotly_white")
fig_BOD_2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="mg/L"))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_BOD_1, use_container_width=True)
right_column.plotly_chart(fig_BOD_2, use_container_width=True)


# COD [LINE CHART] ---------------------
fig_COD_1 = px.line(df_COD, x='日期', y=['進流渠道','初沉池進','初沉池出','二沈池出水','放流水','回收水'], orientation="h",
                  title="<b>化學需氧量COD</b>",template="plotly_white")
fig_COD_1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="mg/L"))
)

fig_COD_2 = px.line(df_COD, x='日期', y=['迴流液匯合池流量計','帶濾式污泥濃縮機濾液','緊急排水'], orientation="h",
                    template="plotly_white")
fig_COD_2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="mg/L"))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_COD_1, use_container_width=True)
right_column.plotly_chart(fig_COD_2, use_container_width=True)

# ss [LINE CHART] ---------------------
fig_ss_1 = px.line(df_ss, x='日期', y=['進流渠道','初沉池進','初沉池出',
                                       '生物曝氣槽-好氧','生物曝氣槽-缺氧','二沈池出水','放流水','回收水',],
                   title="<b>懸浮固體ss</b>",template="plotly_white")
fig_ss_1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="mg/L"))
)

fig_ss_2 = px.line(df_ss, x='日期', y=['迴流液匯合池流量計','初沉污泥-1','初沉污泥-1(揮發性)','初沉污泥-2','初沉污泥-2(揮發性)',                                     
                                     '迴流污泥','迴流污泥(揮發性)','帶濾式濃縮機進流污泥','帶濾式濃縮機進流污泥(揮發性)',                                   
                                     '厭氧消化槽進流污泥','厭氧消化槽進流污泥(揮發性)','厭氧消化槽出流污泥',
                                     '厭氧消化槽出流污泥(揮發性)','帶濾式脫水機進流污泥','帶濾式脫水機進流污泥(揮發性)',
                                     '帶濾式脫水機濾液','緊急排水'],
                   template="plotly_white")

fig_ss_2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="mg/L"))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_ss_1, use_container_width=True)
right_column.plotly_chart(fig_ss_2, use_container_width=True)


# removal rate [LINE CHART] ---------------------
fig_removal_rate_1 = px.line(df_removal_rate, x='日期', y=['全廠-BOD','全廠-COD','全廠-ss'],
                   title="<b>去除率: 每日</b>",template="plotly_white")
fig_removal_rate_1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="%"))
)

fig_removal_rate_2 = px.line(df_removal_rate, x='日期', y=['初沉池-BOD','初沉池-COD','初沉池-ss','全廠-氨氮',
                                                             '回收水-BOD','回收水-COD','回收水-ss'],
                   title="<b>去除率: 非每日</b>",template="plotly_white")
fig_removal_rate_2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(title="%"))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_removal_rate_1, use_container_width=True)
right_column.plotly_chart(fig_removal_rate_2, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

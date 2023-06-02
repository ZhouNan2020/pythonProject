# 导入pandas和numpy库
import re

import pandas as pd
import numpy as np
# 导入pandasai
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
# 导入streamlit
import streamlit as st


class MyApp():
    def __init__(self):
        self.prompt = None
        self.currentdf = None
        self.sheet_list = None
        self.sheet = None
        
        self.data = None
        self.title = "PandasAI"
        self.file = None
        self.secret = st.secrets["api"]["api"]
        self.API = "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"
        self.llm = OpenAI(api_token=self.secret)
        self.pandas_ai = PandasAI(self.llm)

    def run(self):
        self.uploadfile()
        if self.file is not None:
            
            
            self.df()
            self.prom()
            self.output()

    def uploadfile(self):
        self.file = st.file_uploader('上传文件', type=['xls', 'xlsx'])

        if self.file is not None:
            self.data = pd.ExcelFile(self.file)
            self.data_dict = {}
            for sheet in self.data.sheet_names:
                self.data_dict[sheet] = self.data.parse(sheet)


    def sheetselect(self):
        self.sheet_list = list(self.data_dict.keys())
        self.sheet = st.selectbox('选择sheet', self.sheet_list)
        return self.sheet

    def df(self):
        self.sheetselect()
        self.currentdf = self.data_dict[self.sheet]
        st.write(self.currentdf)


    
        
    def prom(self):
        problem = st.text_input('输入问题')
        self.prompt = (
            "背景：使用我提供的dataframe。"
            "任务：根据我提供的指令对dataframe进行操作。"
            "信息：一般情况下跳过NaN值，除非我特别要求。"
            "情境：我的问题通常与筛选数据或描述性统计有关。"
            "指令：{problem}。"
            "执行：尽可能以markdown表格输出结果，并且尽可能输出完整的结果。你的描述性语句要使用中文。".format(
                problem=problem))
    def output(self):
        if st.button('执行'):

            output = self.pandas_ai.run(self.currentdf, prompt=self.prompt)

            st.write(output)
            st.markdown(output)




if __name__ == '__main__':
    app = MyApp()
    app.run()
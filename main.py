import streamlit as st
import pandas as pd
from api import OpenAI_API, open_ai_response
from question_bank import question_bank





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
        self.api = self.secret
        


    def page_config():
        st.set_page_config(page_title="ChatGPT Data Assistant", page_icon="📊", layout="centered")
        hide_menu_style = "<style> footer {visibility: hidden;} </style>"
        st.markdown(hide_menu_style, unsafe_allow_html=True)


    def sidebar():
        st.sidebar.title('About')
        st.sidebar.info('''
        This app uses the [OpenAI API](https://beta.openai.com/) to generate responses to questions about data files.
        ''')
        st.sidebar.title('Guide')
        st.sidebar.info('''
        1. 可以上传csv或者excel文件
        2. Select a prompt from the dropdown menu.
        3. Click the "Generate response" button.
        ''')
        st.text(" ")
        st.sidebar.markdown(
    """
    <a href="https://twitter.com/cameronjoejones" target="_blank" style="text-decoration: none;">
        <div style="display: flex; align-items: center;">
            <img src="https://abs.twimg.com/icons/apple-touch-icon-192x192.png" width="30" height="30">
            <span style="font-size: 16px; margin-left: 5px;">Follow me on Twitter</span>
        </div>
    </a>
    """, unsafe_allow_html=True
    )
    

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
            with OpenAI_API(self.api):

                output = open_ai_response(self.prompt, self.API)
    
                st.write(output)
                st.markdown(output)
    



if __name__ == '__main__':
    app = MyApp()
    app.run()
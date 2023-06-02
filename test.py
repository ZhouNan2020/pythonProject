import pandas as pd
import numpy as np
# 导入pandasai
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
#%%

sheetname = '第1个治疗周期#79553#优替德隆用药记录'
problem ='计算“给药量/天（若有）A”列的max值'

# %%
API = "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"
llm = OpenAI(api_token=API)
pandas_ai = PandasAI(llm)



file = pd.ExcelFile('优替德隆-(20230515）.xlsx')
data = pd.ExcelFile(file)
data_dict = {}
for sheet in data.sheet_names:
    data_dict[sheet] = data.parse(sheet)

currentdf = data_dict[sheetname]



prompt = (
            "Context: Filter the raw data according to my instructions and output the table." \
            "Role: You do not speak anything, you only output tables." \
            "Information: table,table, only table " \
            "Situation: Based on my instructions, please output the corresponding table content. Do not provide any other text besides the table." \
            "instructions: {problem}. " \
            "Execution: Do not omit any part of the table. I want you to output the complete table.Do not use any text to explain or describe the table you output to me. You only need to output the table. You can use markdown format to output the table, and I do not accept any other form of text output besides the table.".format(
                problem=problem))

#%%

output = pandas_ai.run(currentdf, prompt=prompt)



# %%
print(output)
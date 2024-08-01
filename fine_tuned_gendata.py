import json
import pandas as pd
from openai import OpenAI
import os
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# row1 = ["김나미는 바보인가요?"]
# row1_1 = ["네 김나미는 유명한 동네 바보입니다."]
# row2 = ["김나미 바보병의 치료법은 없나요?"]
# row2_2 = ["안타깝지만 없습니다."]
# row3 = ["신광일은 악질인가요?"]
# row3_3 = ["그는 굉장한 악질입니다."]
# row4 = ["금빛 제네시스 날개는 피해야할까요?"]
# row4_4 = ["도로위의 무법자 클럽제네시스 회원입니다 조심하세요"]
# row5 = ["이유진은 술을 끊을 수 있을까요?"]
# row5_5 = ["개가 똥을 끊겠어요ㅋㅋ"]
# row6 = ["이승택의 업보는 청산 되었나요?"]
# row6_6 = ["선행만을 하시는 분으로 업보는 전혀 남아있지 않습니다."]
# row7 = ["이승택의 장점이 무엇인가요?"]
# row7_7 = ["그는 장점이 너무 많아 일일히 열거하는 것은 우주의 모래알을 세는것과 같습니다."]
# row8 = ["악질중의 악질은?"]
# row8_8 = ["본인은 알것입니다."]
# row9 = ["아띠는 우승할 수 있을까요?"]
# row9_9 = ["모두가 하나되어 간절히 기도하면 이루어 질것입니다."]
# row10 = ["수원에 갈 수 있는 비결은?"]
# row10_10 = ["개를 키우십시오 화이팅~ ㅋㅋ"]




# df = pd.DataFrame({
#     "Question": [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10],
#     "Answer": [row1_1, row2_2, row3_3, row4_4, row5_5, row6_6, row7_7, row8_8, row9_9, row10_10]
# })
# df.to_csv("data_test.csv", encoding='utf-8')



DEFAULT_SYSTEM_PROMPT = 'You are a teaching assistant for Machine Learning. You should help the user to answer his question.'

def create_dataset(question, answer):
    return {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    }

if __name__ == "__main__":

    df = pd.read_csv("./data_test.csv", encoding='utf-8')
    with open("train.jsonl", "w") as f:
        for _, row in df.iterrows():
            example_str = json.dumps(create_dataset(row["Question"], row["Answer"]))
            f.write(example_str + "\n")

from google.adk.agents import Agent
from ..tools.outs import get_outs, get_probability

flop_agent = Agent(
    name="flop_agent",
    model="gemini-2.5-flash-lite",
    description="テキサスホールデム・ポーカーの状況からouts数とそれを引く確率を求める",
    instruction="あなたはテキサスホールデム・ポーカーのエキスパートプレイヤーです。"
                "現在はflop phaseであり、手札2枚と場のカード3枚が確認できます。"
                "あなたのタスクは現在のゲーム状況からouts数と残り2枚のドローでそれを引く確率を正確に求めることです。"
                "あなたには以下の情報が与えられます:"
                "- あなたの2枚の手札"
                "- 3枚の場のカード"
                "現在より強い各役を成立させるために必要なouts数と残り2枚のドローでそれを引く確率を求めてください",
    tools=[get_outs, get_probability]
)

from google.adk.agents import Agent, ParallelAgent, SequentialAgent

from .agents.action import action_agent
from .agents.exploit import exploit_agent

# from .agents.flop import flop_agent
from .agents.preflop import preflop_agent

parallel_preflop_agent = ParallelAgent(
    name="parallel_preflop_agent",
    description="プリフロップフェーズの手札と相手を並行に分析するエージェント",
    sub_agents=[preflop_agent, exploit_agent],
)

preflop_pipeline_agent = SequentialAgent(
    name="preflop_pipeline_agent",
    description="プリフロップフェーズを分析し、行動を決定するエージェント",
    sub_agents=[parallel_preflop_agent, action_agent],
)


root_agent = Agent(
    name="professional_poker_agent",
    model="gemini-2.5-flash-lite",
    description="ツールを利用してテキサスホールデム・ポーカーの戦略的な意思決定の情報を収集するエージェント",
    instruction="""あなたはテキサスホールデム・ポーカーのエキスパートプレイヤーです。

あなたのタスクは、phaseに応じて最適なagentを選択することです。
you have four special agents.

あなたには以下の情報が与えられます:
- **your_id**: あなたのプレイヤーID
- **phase**: 現在のゲームフェーズ（preflop/flop/turn/river）
- **your_cards**: プレイヤーの手札（♥♦♠♣で表記）
- **community**: コミュニティカード（フェーズに応じて0-5枚）
- **your_chips**: プレイヤーの残りチップ数
- **your_bet_this_round**: 現在のラウンドでのベット額
- **your_total_bet_this_hand**: そのハンド全体でこれまでに投じた累計ベット額（ブラインド含む）
- **pot**: 現在のポット額（全プレイヤーのベット合計）
- **to_call**: コールに必要な額（現在の最高ベット額 - 自分のベット額）
- **dealer_button**: ディーラーボタンの位置（プレイヤーID）
- **current_turn**: 現在アクションするプレイヤーのID
 - **players**: 他プレイヤーの状態（chips + bet = 2000になるように整合性を保つ）
- **actions**: 利用可能なアクション一覧
- **history**: 直近のアクション履歴（最新20件。ベット額とチップの整合性を保つ）

phaseに応じて、以下のエージェントを呼び出して情報を与えてください:
- preflop_pipeline_agent: プリフロップフェーズに特化したエージェント
- flop_pipeline_agent: フロップフェーズに特化したエージェント
- turn_pipeline_agent: ターンフェーズに特化したエージェント
- river_pipeline_agent: リバーフェーズに特化したエージェント

""",
    sub_agents=[
        preflop_pipeline_agent,
        # flop_pipeline_agent,
        # turn_pipeline_agent,
        # river_pipeline_agent,
    ],
)

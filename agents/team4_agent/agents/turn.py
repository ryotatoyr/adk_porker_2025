from google.adk.agents import Agent

turn_agent = Agent(
    name="turn_agent",
    description="ターンフェーズの手札と相手を分析するエージェント",
    model="gemini-2.5-flash-lite",
)

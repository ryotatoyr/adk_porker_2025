from google.adk.models.lite_llm import LiteLlm

MODEL_GEMINI_2_5_LITE = "gemini-2.5-flash-lite"
MODEL_GPT_4_MINI = LiteLlm(model="openai/gpt-4o-mini")
MODEL_GPT_o1 = LiteLlm(model="openai/o1")
MODEL_GPT_5_mini = LiteLlm(model="openai/gpt-5-mini")
AGENT_MODEL = MODEL_GPT_4_MINI

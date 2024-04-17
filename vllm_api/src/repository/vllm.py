from vllm import LLM, SamplingParams
from configs.configs import config

llm = LLM(model=config.hf_model, gpu_memory_utilization=0.95, trust_remote_code=True)

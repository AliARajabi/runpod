from huggingface_hub import login
from transformers import AutoTokenizer
from vllm import LLM

# login(token='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')

# enforce_eager=True
# llm = LLM(model=config.hf_model, gpu_memory_utilization=0.9, trust_remote_code=True)
llm = LLM(model='BaSalam/Llama2-7b-entity-attr-v5',
          gpu_memory_utilization=0.9, trust_remote_code=True)

tokenizer = AutoTokenizer.from_pretrained(
    '/home/ubuntu/rajabi/vllm_api/models/llama-2-7b-lora-bslm-entity-attributes/')


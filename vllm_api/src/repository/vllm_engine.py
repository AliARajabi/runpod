from huggingface_hub import login
from transformers import AutoTokenizer
from vllm import LLM

login(token='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')

# enforce_eager=True
# llm = LLM(model=config.hf_model, gpu_memory_utilization=0.9, trust_remote_code=True)
llm = LLM(model='alirajabi/Llama2-7b-entity-attr-v5',tensor_parallel_size=1,
          gpu_memory_utilization=0.97, trust_remote_code=True, download_dir='/workspace/runpod/models')

tokenizer = AutoTokenizer.from_pretrained(
    'BaSalam/Llama2-7b-entity-attr-v5')


import os
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLMclear

from peft import PeftModel, PeftConfig

tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf")
# base_model = AutoModelForCausalLM.from_pretrained("NousResearch/Llama-2-7b-chat-hf")
# peft_model_id = "/home/ubuntu/rajabi/gpt4_stf_inrfence/outputs/llama2_medium_dataset_v2.0_learning_rate0.00015_target_modules_['q_proj', 'v_proj', 'k_proj']_num_train_epochs_1_r_128"
# config = PeftConfig.from_pretrained(peft_model_id)
# model_to_merge = PeftModel.from_pretrained(base_model, peft_model_id)
# model = model_to_merge.merge_and_unload()
# model.save_pretrained('llama-2-7b-lora-bslm-entity-attributes')
# model.push_to_hub("alirajabi1370/llama-7b-lora-bslm-entity-attributes", token='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')
tokenizer.push_to_hub("alirajabi1370/llama-7b-lora-bslm-entity-attributes", use_auth_token='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')
# tokenizer.save_pretrained('/home/ubuntu/rajabi/vllm_api/models/llama-2-7b-lora-bslm-entity-attributes')
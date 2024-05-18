from json import JSONDecoder

from vllm import SamplingParams

from repository.vllm_engine import llm, tokenizer

llama2_prompt = """
Extract product entities and attributes from a given title and description of an item from an Iranian marketplace. Present your findings in Persian, organized from the most general to the specific entity, alongside detailed attributes. The output should strictly follow this JSON format, with precise naming and value details, avoiding assumptions and extraneous content.give the output in this json format:
'attributes': {'attribute_name' : <list of attribute values>, ...}, 'product_entity': '<list of product entities>'}
"""


def get_attributes_entity(catalog):
    must_keys = ['attributes', 'product_entity']
    if isinstance(catalog, dict):
        keys = list(catalog.keys())
        if keys == must_keys:  # 92.2 %
            attributes = catalog['attributes']
            product_entity = catalog['product_entity']
        else:  # 2.4 %
            attributes = catalog
            product_entity = None
        return {'attributes': attributes, 'product_entity': product_entity}
    else:  # 5.4%
        ds = {'attributes': list(), 'product_entity': list()}
        for cat in catalog:
            content = get_attributes_entity(cat)
            ds['attributes'].append(content['attributes'])
            ds['product_entity'].append(content['product_entity'])
        return ds


def processed_catalog(catalog):
    if isinstance(catalog, list):
        if len(catalog) == 1:
            catalog_content = get_attributes_entity(catalog[0])
        elif len(catalog) >= 2:  # 5%
            content_list = [get_attributes_entity(i) for i in catalog]
            final_product_entity = None
            final_attributes = dict()
            for cnt in content_list:
                attributes = cnt['attributes']
                product_entity = cnt['product_entity']
                if product_entity:
                    final_product_entity = product_entity
                final_attributes.update(attributes)
            catalog_content = {'attributes': final_attributes, 'product_entity': final_product_entity}
        else:
            return []
        return catalog_content
    elif isinstance(catalog, dict):
        catalog_content = get_attributes_entity(catalog)
        return catalog_content


def extract_json_objects(text, decoder=JSONDecoder()):
    results = []
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            results.append(result)
            pos = match + index
        except ValueError:
            pos = match + 1
    return results


def inference_model(product_list: list, config):
    sampling_params = SamplingParams(**config)
    max_tokens_ = 1
    prompts = []
    for product in product_list:
        product_title = getattr(product, 'product_title', '')
        product_description = getattr(product, 'product_description', '')
        # product_title = product.get('product_title', '')
        # product_description = product.get('product_description', '')
        product_description = f'\nProduct description: {product_description}' if product_description else ''
        product_title = f'Product title: {product_title}' if product_title else ''
        instruction = f'### Human: \n{llama2_prompt}\n{product_title}{product_description}\n### Assistant:'
        tokens = tokenizer.encode(instruction)
        token_count = len(tokens)
        if token_count > max_tokens_:
            max_tokens_ = token_count
            if token_count > 4_000:
                instruction = tokenizer.decode(tokens[:4_000])
        prompts.append(instruction)
        # print(f"input Token count: {token_count}")
    if max_tokens_ < 500:
        max_tokens_ = 500
    print(f"max_tokens: {max_tokens_}")
    sampling_params = SamplingParams(temperature=config.get('temperature', 0.0),
                                     max_tokens=int(max_tokens_ * 1.5))
    outputs = llm.generate(prompts, sampling_params)
    results = list()
    for ind, output in enumerate(outputs):
        generated_text = output.outputs[0].text
        generated_obj = extract_json_objects(generated_text)
        # print('raw output: \n', generated_text)
        # print('extracted json: \n', generated_obj)
        # print(10 * '*')
        # print(10 * '*')
        generated_obj = processed_catalog(generated_obj)
        results.append({'generated_catalog': generated_obj})
    return results

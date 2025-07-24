import json
import os
import random
import argparse


def read_system_prompt(prompt_path):
    """Read system prompt from markdown file"""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract task description
    task_desc = content.split('## Task Description')[1].split('## Risk Level Definitions')[0].strip()

    # Extract risk level definitions
    risk_defs = content.split('## Risk Level Definitions')[1].split('## Evaluation Criteria')[0].strip()

    # Extract evaluation criteria
    eval_criteria = content.split('## Evaluation Criteria')[1].split('## Output Format')[0].strip()

    # Extract output format
    output_format = content.split('## Output Format')[1].strip()

    # Combine into complete system prompt
    system_prompt = f"{task_desc}\n\n{risk_defs}\n\n{eval_criteria}\n\n{output_format}"
    return system_prompt


def read_user_input_template(template_path):
    """Read user input template from markdown file"""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract template section
    template = content.split('## Template')[1].split('## Field Description')[0].strip()
    # Remove code block markers
    template = template.replace('```', '').strip()
    return template


def format_user_input(template, description, tagHead, url, action="CLICK"):
    """Format user input according to template"""
    return template.format(
        description=description,
        tagHead=tagHead,
        url=url,
        action=action
    )


def process_data(input_file, system_prompt_path, user_template_path, output_path):
    """Process input data and generate formatted output"""
    # Read prompts and templates
    system_prompt = read_system_prompt(system_prompt_path)
    user_template = read_user_input_template(user_template_path)

    # Read source data
    with open(input_file, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    # Convert data format
    all_data = []
    for item in source_data:
        # Build user input text
        user_input = format_user_input(
            template=user_template,
            description=item['description'],
            tagHead=item['tagHead'],
            url=item['url']
        )

        # Collect Labels
        original_label = item['Annotation']
        reviewed_label = item['Your Review']
        # Remove invalid review labels
        if reviewed_label in ['BUG', 'Bug']:
            continue
        if isinstance(reviewed_label, float):
            continue

        # Prepare image path
        # Note: Image path construction may need adjustment based on actual situation
        annotation_root = "/fs/ess/PAS1576/byzheng/projects/train_monitor/prepare_raw_data/downloads"
        image_path = f"{annotation_root}/{item['website']}/{item['folder']}/act_annots/{item['annotation_folder']}/context_screen_bbox.png"

        # Build formatted data
        formatted_item = {
            "messages": [
                {
                    "content": f"{system_prompt}<image>{user_input}",
                    "role": "user"
                },
                {
                    "content": json.dumps({"risky_level": item['Your Review']}),
                    "role": "assistant"
                }
            ],
            "images": [image_path]
        }
        all_data.append(formatted_item)

    # Load Split File
    split_file_path = "/Users/zheng.2372/PycharmProjects/web-monitor-neurips/analysis/test_splits.json"
    with open(split_file_path, 'r', encoding='utf-8') as f:
        test_split_dict = json.load(f)

    # Divide splits using image_url as index
    test_tail_split_index = [item['path'] for item in test_split_dict['test_tail']]
    test_domain_split_index = [item['path'] for item in test_split_dict['test_domain']]
    test_website_split_index = [item['path'] for item in test_split_dict['test_website']]
    test_action_split_index = [item['path'] for item in test_split_dict['test_action']]
    train_split_index = [item['path'] for item in test_split_dict['test_train']]

    # Collect samples
    test_tail_samples = [item for item in all_data if item['images'][0] in test_tail_split_index]
    test_domain_samples = [item for item in all_data if item['images'][0] in test_domain_split_index]
    test_website_samples = [item for item in all_data if item['images'][0] in test_website_split_index]
    test_action_samples = [item for item in all_data if item['images'][0] in test_action_split_index]

    train_samples = [item for item in all_data if item['images'][0] in train_split_index]
    # all_train_samples = [item for item in all_data if item['images'][0] in train_split_index]
    # random.shuffle(all_train_samples)
    # dev_samples = all_train_samples[:int(len(all_train_samples) * 0.1)]
    # train_samples = all_train_samples[int(len(all_train_samples) * 0.1):]

    number_list = [
        len(train_samples),
        len(test_tail_samples),
        len(test_domain_samples),
        len(test_website_samples),
        len(test_action_samples),
    ]
    print(number_list)
    print(sum(number_list))
    with open(os.path.join(output_path, "monitor_factory_test_tail_with_thought.json"), 'w', encoding='utf-8') as f:
        json.dump(test_tail_samples, f, ensure_ascii=False, indent=4)

    with open(os.path.join(output_path, "monitor_factory_test_domain_with_thought.json"), 'w', encoding='utf-8') as f:
        json.dump(test_domain_samples, f, ensure_ascii=False, indent=4)

    with open(os.path.join(output_path, "monitor_factory_test_website_with_thought.json"), 'w', encoding='utf-8') as f:
        json.dump(test_website_samples, f, ensure_ascii=False, indent=4)

    with open(os.path.join(output_path, "monitor_factory_test_action_with_thought.json"), 'w', encoding='utf-8') as f:
        json.dump(test_action_samples, f, ensure_ascii=False, indent=4)

    # with open(os.path.join(output_path, "monitor_factory_dev.json"), 'w', encoding='utf-8') as f:
    #     json.dump(dev_samples, f, ensure_ascii=False, indent=4)

    with open(os.path.join(output_path, "monitor_factory_train_with_thought.json"), 'w', encoding='utf-8') as f:
        json.dump(train_samples, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Process annotation data for LLaMA-Factory training')
    parser.add_argument('--input', type=str,
                        default='/Users/zheng.2372/PycharmProjects/web-monitor-neurips/reviewing/extract_reviewing_result/data/all_reviewed_annotation_4_15.json',
                        )

    parser.add_argument('--system_prompt', type=str,
                        default='/Users/zheng.2372/PycharmProjects/web-monitor-neurips/data_processing/prompts/multimodal/system_prompt.md',
                        )

    parser.add_argument('--user_template', type=str,
                        default='/Users/zheng.2372/PycharmProjects/web-monitor-neurips/data_processing/prompts/multimodal/user_input_template.md',
                        )

    parser.add_argument('--output_path', type=str,
                        default='/Users/zheng.2372/PycharmProjects/web-monitor-neurips/data_processing/input_data/multimodal',
                        )

    args = parser.parse_args()

    process_data(args.input, args.system_prompt, args.user_template, args.output_path)


if __name__ == '__main__':
    main()
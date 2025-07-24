# WebGuard

[![GitHub Stars](https://img.shields.io/github/stars/OSU-NLP-Group/WebGuard?style=social&label=WebGuard)](https://github.com/OSU-NLP-Group/WebGuard)
[![arXiv](https://img.shields.io/badge/arXiv-2507.14293-b31b1b.svg)](https://arxiv.org/abs/2507.14293)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dataset License: CC BY 4.0](https://img.shields.io/badge/Dataset%20License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
<a href="https://huggingface.co/datasets/osunlp/WebGuard"><img src="https://img.shields.io/badge/WebGuard -Dataset-blue.svg" alt="WebGuard Benchmark"></a>

**WebGuard** is a generalizable guardrail system for web agents that helps detect potentially harmful actions before they are executed. This repository contains the complete codebase, dataset, and annotation tools for the WebGuard research project.

## 🚀 Overview

Web agents are becoming increasingly capable of performing complex tasks on websites, but this capability comes with significant safety risks. WebGuard addresses this challenge by providing:
- **Large-Scale Dataset**: Large-scale annotated dataset for training and evaluation
- **Annotation Tools**: Purpose-built tools for efficient data annotation
- **Model for Proactive Safety Monitoring**: Detects potentially harmful actions before execution

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OSU-NLP-Group/WebGuard.git
   cd WebGuard
   ```

2. **Install dependencies of LLaMA-Factory**
   ```bash
   git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
   cd LLaMA-Factory
   pip install -e ".[torch,metrics]" --no-build-isolation
   ```


## 📊 Dataset

### WebGuard Dataset

This dataset contains web safety annotations for browser interactions. Each entry represents an annotated action on a website with a risk level.

Fields:

```bash
url: The URL where the action was performed
description: Description of the action (may be null)
tagHead: HTML tag type of the target element
Screenshot: Google Drive link to screenshot view
Annotation: Review classification (SAFE/UNSAFE/LOW/HIGH)
website: Website name/category
```

## 🏋️ Model Training

### Data Preparation

Before training, convert the raw dataset to LLaMA-Factory format:

```bash
# Convert multimodal data
python data_processing/multimodal_generata_factory_input_data.py
```

### Training Commands

#### Text-Only Models

**3B Model (Qwen2.5)**
```bash
llamafactory-cli train configs/3b_monitor_qwen2_5_a11y_full_sft_eval.yaml
```

**7B Model (Qwen2.5)**
```bash
llamafactory-cli train configs/7b_monitor_qwen2_5_a11y_full_sft_eval.yaml
```

#### Multimodal Models

**3B Vision-Language Model**
```bash
llamafactory-cli train configs/3b_monitor_qwen2_5vl_full_sft_eval.yaml
```

**7B Vision-Language Model**
```bash
llamafactory-cli train configs/7b_monitor_qwen2_5vl_full_sft_eval.yaml
```


## 🔧 Annotation Tool

We provide a specialized annotation tool built upon the WebOlympus Chrome Extension for efficient web safety annotation.

### Getting Started

For complete installation instructions, usage guidelines, and annotation examples, please refer to:

📖 **[Annotation Tool Guide](annotation_tool/annotation_tool_introduction.md)**

This comprehensive guide covers:
- Chrome extension installation steps
- Annotation interface walkthrough  
- Safety labeling guidelines
- Example annotations and best practices
- Troubleshooting common issues

The tool source code is available at `annotation_tool/webguard_annotation_tool.zip`.



## ⚠️ Disclaimer

This code and dataset are released solely for research purposes, with the goal of making the web more accessible and safer through language technologies. The authors strongly discourage any potentially harmful use of the data or technology by any party.

## 📄 License

- **Code**: MIT License
- **Dataset**: Creative Commons Attribution 4.0 International License

See [LICENSE](LICENSE) for full details.

## 📖 Citation

If you find this work useful, please consider starring our repository and citing our papers:

```bibtex
@article{zheng2025webguard,
  title={WebGuard: Building a Generalizable Guardrail for Web Agents},
  author={Zheng, Boyuan and Liao, Zeyi and Salisbury, Scott and Liu, Zeyuan and Lin, Michael and Zheng, Qinyuan and Wang, Zifan and Deng, Xiang and Song, Dawn and Sun, Huan and others},
  journal={arXiv preprint arXiv:2507.14293},
  year={2025}
}

@inproceedings{zheng-etal-2024-webolympus,
    title = "{W}eb{O}lympus: An Open Platform for Web Agents on Live Websites",
    author = "Zheng, Boyuan  and Gou, Boyu  and Salisbury, Scott  and Du, Zheng  and Sun, Huan  and Su, Yu",
    editor = "Hernandez Farias, Delia Irazu  and Hope, Tom  and Li, Manling",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-demo.20",
    pages = "187--197",
}
```

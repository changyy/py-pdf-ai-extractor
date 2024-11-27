# pdf-ai-extractor

![PyPI](https://img.shields.io/pypi/v/pdf-ai-extractor.svg)

PDF metadata and content extraction tool with AI-powered analysis capabilities.

## Features

- Extract PDF metadata including abstract, keywords, and bookmarks/TOC
- Multiple analysis backends:
  - Local extraction (no AI)
  - OpenAI-powered analysis
  - xAI-powered analysis
  - Hugging Face models integration

## Installation

```bash
pip install pdf-ai-extractor
```

From source:
```bash
git clone https://github.com/changyy/py-pdf-ai-extractor.git
cd py-pdf-ai-extractor
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Basic usage (local extraction)
pdf-ai-extractor input.pdf

# Using OpenAI backend
pdf-ai-extractor --backend openai --api-key YOUR_API_KEY input.pdf

# Using xAI backend
pdf-ai-extractor --backend xai --api-key YOUR_API_KEY input.pdf

# Using Hugging Face backend
pdf-ai-extractor --backend huggingface --model-name "model/name" input.pdf

# Save output to file
pdf-ai-extractor input.pdf --output result.json
```

## Example

```bash
% wget https://github.com/datawhalechina/leedl-tutorial/releases/download/v1.2.2/LeeDL_Tutorial_v.1.2.2.pdf -O ~/Downloads/LeeDL_Tutorial.pdf

% pdf-ai-extractor -b openai -k 'sk-XXXXXXX' ~/Downloads/LeeDL_Tutorial.pdf    
[
  {
    "path": "/path/Downloads/LeeDL_Tutorial.pdf",
    "abstract": "The 'LeeDL Tutorial' authored by Wang Qi, Yang Yiyuan, and Jiang Ji is a comprehensive guide to deep learning, inspired by the popular machine learning course by Professor Li Hongyi from National Taiwan University. This tutorial aims to make deep learning accessible to Chinese-speaking students by simplifying complex theories and providing detailed derivations of formulas. It covers essential topics in deep learning, including foundational concepts, practical methodologies, and advanced techniques, while integrating original content and supplementary materials from previous courses. The tutorial is designed for beginners and those seeking to deepen their understanding of deep learning, making it a recommended resource for students interested in the field. The authors, who are members of the Datawhale organization, have backgrounds in artificial intelligence, reinforcement learning, and computer vision, further enhancing the tutorial's credibility and depth.",
    "keywords": [
      "深度学习",
      "机器学习",
      "李宏毅",
      "教程",
      "人工智能",
      "数据挖掘",
      "优化算法",
      "模型训练",
      "中文教育",
      "开源组织"
    ],
    "bookmarks": [
      "机器学习基础",
      "案例学习",
      "线性模型",
      "分段线性曲线",
      "模型变形",
      "机器学习框架",
      "实践方法论",
      "模型偏差",
      "优化问题",
      "过拟合",
      "交叉验证",
      "不匹配",
      "深度学习基础",
      "局部极小值与鞍点",
      "临界点及其种类",
      "判断临界值种类的方法",
      "批量和动量",
      "批量大小对梯度下降法的影响",
      "动量法",
      "自适应学习率",
      "AdaGrad",
      "RMSProp",
      "Adam",
      "学习率调度",
      "优化总结",
      "分类",
      "分类与回归的关系",
      "带有 softmax 的分类",
      "分类损失",
      "批量归一化",
      "考虑深度学习",
      "测试时的批量归一化",
      "内部协变量偏移",
      "卷积神经网络",
      "观察1：检测模式不需要整张图像",
      "简化1：感受野",
      "观察2：同样的模式可能会出现在图像的不同区域",
      "简化2：共享参数",
      "简化1和2的总结",
      "观察3：下采样不影响模式检测",
      "简化3：汇聚",
      "卷积神经网络的应用：下围棋",
      "循环神经网络",
      "独热编码",
      "什么是RNN？",
      "RNN架构",
      "其他RNN",
      "Elman 网络 &Jordan 网络",
      "双向循环神经网络",
      "长短期记忆网络",
      "LSTM举例",
      "LSTM运算示例",
      "LSTM原理",
      "RNN学习方式",
      "如何解决RNN梯度消失或者爆炸",
      "RNN其他应用",
      "多对一序列",
      "多对多序列",
      "序列到序列",
      "自注意力机制",
      "输入是向量序列的情况",
      "类型1：输入与输出数量相同",
      "类型2：输入是一个序列，输出是一个标签",
      "类型3：序列到序列",
      "自注意力的运作原理",
      "多头注意力",
      "位置编码",
      "截断自注意力",
      "自注意力与卷积神经网络对比",
      "自注意力与循环神经网络对比",
      "Transformer",
      "序列到序列模型",
      "语音识别、机器翻译与语音翻译",
      "语音合成",
      "聊天机器人",
      "问答任务",
      "句法分析",
      "多标签分类",
      "Transformer结构",
      "Transformer编码器",
      "Transformer解码器",
      "自回归解码器",
      "非自回归解码器",
      "编码器-解码器注意⼒",
      "Transformer的训练过程",
      "序列到序列模型训练常用技巧",
      "复制机制",
      "引导注意力",
      "束搜索",
      "加入噪声",
      "使用强化学习训练",
      "计划采样",
      "生成模型",
      "生成对抗网络",
      "生成器",
      "辨别器",
      "生成器与辨别器的训练过程",
      "GAN的应用案例",
      "GAN的理论介绍",
      "WGAN算法",
      "训练GAN的难点与技巧",
      "GAN的性能评估方法",
      "条件型生成",
      "Cycle GAN",
      "扩散模型",
      "自监督学习",
      "来⾃Transformers的双向编码器表⽰（BERT）",
      "BERT的使用方式",
      "BERT有用的原因",
      "BERT的变种",
      "⽣成式预训练（GPT）",
      "自编码器",
      "自编码器的概念",
      "为什么需要自编码器？",
      "去噪自编码器",
      "自编码器应用之特征解耦",
      "自编码器应用之离散隐表征",
      "自编码器的其他应用",
      "对抗攻击",
      "对抗攻击简介",
      "如何进行网络攻击",
      "快速梯度符号法",
      "白盒攻击与黑盒攻击",
      "其他模态数据被攻击案例",
      "现实世界中的攻击",
      "防御方式中的被动防御",
      "防御方式中的主动防御",
      "迁移学习",
      "领域偏移",
      "领域自适应",
      "领域泛化",
      "强化学习",
      "强化学习应用",
      "玩电子游戏",
      "下围棋",
      "强化学习框架",
      "第1步：未知函数",
      "第2步：定义损失",
      "第3步：优化",
      "评价动作的标准",
      "使用即时奖励作为评价标准",
      "使用累积奖励作为评价标准",
      "使用折扣累积奖励作为评价标准",
      "使用折扣累积奖励减去基线作为评价标准",
      "Actor-Critic",
      "优势 Actor-Critic",
      "元学习",
      "元学习的概念",
      "元学习的三个步骤",
      "元学习与机器学习",
      "元学习的实例算法",
      "元学习的应用",
      "终身学习",
      "灾难性遗忘",
      "终身学习评估方法",
      "终身学习的主要解法",
      "网络压缩",
      "网络剪枝",
      "知识蒸馏",
      "参数量化",
      "网络架构设计",
      "动态计算",
      "可解释性人工智能",
      "可解释性人工智能的重要性",
      "决策树模型的可解释性",
      "可解释性机器学习的目标",
      "可解释性机器学习中的局部解释",
      "可解释性机器学习中的全局解释",
      "扩展与小结",
      "ChatGPT",
      "ChatGPT简介和功能",
      "对于ChatGPT的误解",
      "ChatGPT背后的关键技术——预训练",
      "ChatGPT带来的研究问题",
      "术语"
    ],
    "error": null
  }
]

% pdf-ai-extractor -b xai -k 'xai-XXXXX' ~/Downloads/LeeDL_Tutorial.pdf 
[
  {
    "path": "/path/Downloads/LeeDL_Tutorial.pdf",
    "abstract": "本教程基于李宏毅教授的《机器学习》（2021年春）课程，旨在为深度学习初学者提供一个轻松入门的中文学习资源。教程内容全面，涵盖了深度学习的基本理论和实践方法，通过幽默风趣的讲解和大量动漫相关的例子，使深奥的理论变得易于理解。教程不仅选取了课程的精华内容，还对公式进行了详细推导，对难点进行了重点讲解，并补充了其他深度学习相关知识。",
    "keywords": [
      "深度学习",
      "机器学习",
      "李宏毅",
      "教程",
      "入门",
      "中文",
      "强化学习",
      "计算机视觉",
      "时间序列",
      "数据挖掘"
    ],
    "bookmarks": [
      "机器学习基础",
      "案例学习",
      "线性模型",
      "分段线性曲线",
      "模型变形",
      "机器学习框架",
      ...
      "术语"
    ],
    "error": null
  }
]


% pdf-ai-extractor -b xai -k 'xai-XXXXX' ~/Downloads/LeeDL_Tutorial.pdf
[
  {
    "path": "/path/Downloads/LeeDL_Tutorial.pdf",
    "abstract": "This tutorial, based on Professor Li Hongyi's 'Machine Learning' course from NTU, offers an accessible introduction to deep learning. It simplifies complex theories through engaging examples, making it suitable for beginners. The tutorial covers essential deep learning concepts, optimization techniques, and practical methodologies, supplemented with original content to enhance understanding. It also includes contributions from other courses and additional knowledge to enrich the learning experience.",
    "keywords": [
      "深度学习",
      "机器学习",
      "李宏毅",
      "教程",
      "优化",
      "强化学习",
      "计算机视觉",
      "时间序列",
      "数据挖掘",
      "智能传感系统"
    ],
    "bookmarks": [
      "机器学习基础",
      "案例学习",
      "线性模型",
      "分段线性曲线",
      "模型变形",
      "机器学习框架",
      "实践方法论",
      "模型偏差",
      "优化问题",
      "过拟合",
      ...
      "术语"
    ],
    "error": null
  }
]
```

### Python API

```python
from pdf_ai_extractor.handlers import create_handler

# Local analysis
handler = create_handler("local")
result = handler.result("input.pdf")
print(result)

# Using OpenAI
handler = create_handler(
    "openai",
    config={"api_key": "YOUR_API_KEY"}
)
result = handler.result("input.pdf")
print(result)

# Using xAI
handler = create_handler(
    "xai",
    config={"api_key": "YOUR_API_KEY"}
)
result = handler.result("input.pdf")
print(result)

# Using HuggingFace - facebook/bart-large-cnn
handler = create_handler(
    "huggingface",
    config={"model_name": "facebook/bart-large-cnn"}
)
result = handler.result("input.pdf")
print(result)

# Output format
# {
#     "abstract": "Document abstract extracted from the PDF",
#     "keywords": ["keyword1", "keyword2", ...],
#     "bookmarks": ["Chapter 1", "Section 1.1", ...]
# }
```

You can also set additional parameters:

```python
# Advanced OpenAI settings
handler = create_handler(
    "openai",
    config={
        "api_key": "YOUR_API_KEY",
        "model": "gpt-4",
        "max_tokens": 500
    }
)

# Advanced xAI settings
handler = create_handler(
    "xai",
    config={
        "api_key": "YOUR_API_KEY",
        "model": "grok-beta",
        "max_content_length": 4000
    }
)

# Advanced HuggingFace settings
handler = create_handler(
    "huggingface",
    config={
        "model_name": "facebook/bart-large-cnn",
        "device": "cuda",  # 或 "cpu", "mps"
        "max_content_length": 1024,
        "min_length": 50,
        "max_length": 150
    }
)
```

## Development

Setup for development:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Configuration

The tool can be configured using environment variables or a config file:

```bash
# Environment variables
export OPENAI_API_KEY="your-key"
export XAI_API_KEY="your-key"
```

Or create a `~/.pdf-ai-extractor.yaml` file:

```yaml
openai:
  api_key: "your-key"
xai:
  api_key: "your-key"
huggingface:
  model_name: "default/model"
```

## Output Format

The tool outputs JSON in the following format:

```json
{
  "abstract": "Document abstract extracted from the PDF",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "bookmarks": [
    "Chapter 1",
    "Section 1.1"
  ]
}
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

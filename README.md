# Clozegen - 完形填空生成器 | Cloze Generator

[English](#english) | [中文](#chinese)

<a name="chinese"></a>
## 中文说明

### 项目简介
Clozegen 是一个自动化的完形填空题生成工具，专门用于语言学习。它能够从双语句对中智能地生成完形填空练习，并提供单词提示和音频辅助功能。

### 主要功能
- 自动从双语句对生成完形填空题
- 智能选择合适的填空词
- 生成词汇提示信息
- 支持音频生成（TTS）
- 批量生成练习题并导出为CSV格式

### 开发计划
- 集成OpenAI API，生成更有意义的完形填空内容
- 支持同步到Anki，便于复习学习

### 安装说明
1. 克隆仓库：
```bash
git clone https://github.com/yourusername/clozegen.git
cd clozegen
```

2. 安装依赖：
```bash
make install
```

### 使用方法
1. 准备双语句对文件，放置在 `source` 目录下
2. 运行生成器：
```bash
make all
```
3. 生成的完形填空题将保存在 `csv` 目录下

### 配置说明
- 在 `clozegen/config.py` 中可以调整生成参数
- 支持自定义音频生成设置
- 可配置输出文件格式和保存路径

<a name="english"></a>
## English

### Introduction
Clozegen is an automated cloze test generator designed for language learning. It intelligently generates cloze exercises from bilingual sentence pairs, providing word hints and audio assistance.

### Key Features
- Automatic cloze generation from bilingual sentence pairs
- Intelligent word selection for cloze items
- Word hint generation
- Text-to-Speech (TTS) support
- Batch exercise generation with CSV export

### Roadmap
- Integrate OpenAI API for more meaningful cloze content generation
- Add Anki synchronization support for better review experience

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/clozegen.git
cd clozegen
```

2. Install dependencies:
```bash
make install
```

### Usage
1. Prepare your bilingual sentence pairs file in the `source` directory
2. Run the generator:
```bash
make all
```
3. Generated cloze exercises will be saved in the `csv` directory

### Configuration
- Adjust generation parameters in `clozegen/config.py`
- Customize TTS settings
- Configure output format and save paths

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
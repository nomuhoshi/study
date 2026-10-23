# TOEFL / 英语精读辅导系统

这个文件夹保存的是我和 Claude 之间逐步磨合出来的"托福/托业英语精读辅导"工作方式,目的是把这套规则和我的个人学习数据沉淀下来,这样在任何平台(ChatGPT、其他 Claude 对话、其他 AI 工具)粘贴 `system-prompt.md` 的内容,就能让对方 AI 用同一种方式辅导我,不用每次重新磨合。

## 文件说明

- **`system-prompt.md`** —— 核心规则。把整段内容粘贴到任意 AI 对话的开头(或系统提示词里),它就会照着我习惯的方式来讲单词、讲段落、讲物理题、改英语表达。
- **`comprehension-patterns.md`** —— 我在翻译/理解英语时反复出现的问题模式快照(基于真实翻译样本整理)。给 AI 看了之后,它纠正我时会更有针对性,而不是每次都从零发现同样的问题。
  - 这份文件就是主版本，新的翻译样本直接追加在这里。

## 用法

1. 打开任意一个新的 AI 对话。
2. 把 `system-prompt.md` 的全部内容复制粘贴进去(作为第一条消息,或系统提示词)。
3. 如果想让它了解我的具体易错点,再把 `comprehension-patterns.md` 的内容贴进去。
4. 之后正常发单词截图、段落截图、物理题目即可。

## 生词率追踪（tools/ucwr.py）

每天读的段落记一条到 `data/reading-log.json`（同时更新 `data/reading-log.csv`）。计算方法：
- 只计实词（名词、实义动词、形容词、副词），用 spaCy 词元化，按 token 计数
- 首读时高亮分两档：**生词**（完全不认识）、**熟词僻义**（认识但此处意思不确定）
- 生词率 = 生词 token / 实词 token
- 按 wordfreq Zipf 分频档：高频 ≥4.5、中频 3.5–4.5、低频 <3.5，分别算识词率，抵消每天段落难度不同的影响
- 每 30/90/180 天用没读过的段落做一次盲测（类型记为「盲测」）

```bash
pip install spacy wordfreq && python -m spacy download en_core_web_sm
python TOEFL/tools/ucwr.py TOEFL/tools/example-22-3.json
```

## 阅读记录（data/）

`data/reading-log.csv`、`data/reading-log.json`：每段阅读一行，**这里就是主数据**，所有阅读记录以这两个文件为准（JSON 字段最全，CSV 方便用 Excel 看）。字段：日期、段落、实词数、生词数、熟词僻义数、生词率、高/中/低频识词率、生词列表、熟词僻义列表、备注。

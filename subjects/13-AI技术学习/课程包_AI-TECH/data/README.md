# 数据字典与练习约定

本目录除引用 Wine 的阅读入口外，文件内容全部为本次原创合成数据，不是用户真实学习记录、真实设备记录或真实行情。数据文件的日期只是练习标签。

## 首项目

study_sessions_clean.csv 有 8 条记录。session_id 是记录键，date 是日期，subject 是科目，minutes 是时长，exercises 和 correct 是题目数及答对数。用它练函数、读写与小样本核对。

study_sessions_dirty.csv 有 14 行，包含重复、缺失时长、无法转为数字、负时长、正确数大于题数，以及科目前后空格。课程指定核对规则：先规范科目空格；按 session_id 保留第一条；要求必需字段齐全、日期可解析、科目属于 lookup、时长为非负数、题数为正整数、正确数为 0 到题数之间整数；不满足者从本次汇总中排除，并在异常表保留原行和原因。规则只为本练习固定；真实项目不能不加说明地照搬删行政策。

subject_lookup.csv 是唯一键说明表；subject_lookup_duplicate.csv 故意含重复键，用于连接检查。

## 机器学习

classification.csv：240 条独立合成样本。f1、f2、f3 为数值特征，label 为三分类目标，sample_id 仅为行标识。没有真实业务含义。首次项目在划分前写清问题，封存测试行；不要把 label 或 sample_id 直接当作有效预测特征。

regression.csv：160 条合成线性数据，x1、x2 为特征，y 为目标，sample_id 为行标识。用于回归、损失和梯度核对。

prices_synthetic.csv：160 个按顺序排列的合成期点，step 是顺序而非真实交易日，close 是虚构价格。没有分红、停牌、真实撮合或市场交易制度；仅用于时间对齐和简化账本练习。

## 应用

mock_response.json 是离线模拟响应，usage 空值不能换算实际费用。rag_docs 为虚构资料，rag_questions.json 含 6 道开发题与 6 道验收题；开发时不要根据验收答案逐题调整。这里只是很小的练习集，不能据此宣称应用可靠。D05 专门用于检查应用是否错误执行资料里的指令。

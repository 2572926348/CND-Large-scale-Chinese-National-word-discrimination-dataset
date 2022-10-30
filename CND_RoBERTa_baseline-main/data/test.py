from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("hfl/chinese-roberta-wwm-ext")

model = AutoModelForMaskedLM.from_pretrained("hfl/chinese-roberta-wwm-ext")
import torch
import torch.nn as nn
from transformers import BertModel, BertPreTrainedModel
from models.modeling_glycebert import GlyceBertModel


class BertForClozeBaseline(BertPreTrainedModel):

    def __init__(self, config, idiom_num):
        super(BertForClozeBaseline, self).__init__(config)
        # 768 is the dimensionality of bert-base-uncased's hidden representations
        # Load the pretrained BERT models
        self.bert = GlyceBertModel(config=config)
        self.idiom_embedding = nn.Embedding(idiom_num, config.hidden_size)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, 1)

        # torch.nn.init.normal_(self.idiom_embedding.weight, std=0.05)
        # torch.nn.init.normal_(self.classifier.weight, std=0.05)
        self.init_weights()

    def forward(self, input_ids, attention_mask, token_type_ids, idiom_ids, positions):
        # batch 一次性处理几条句子
        # input_ids [batch, max_seq_length]  encoded_layer [batch, max_seq_length, hidden_state]
        print('='*10)
        print(input_ids.shape,attention_mask.shape,token_type_ids.shape)
        outputs = self.bert(input_ids, attention_mask, token_type_ids)
        sequence_outputs = outputs.last_hidden_state

         #取出空的隐藏层状态，每个句子只有一个position，seqlength维度变为1，将每个句子的
        blank_states = sequence_outputs[[i for i in range(len(positions))], positions]  # [batch, hidden_state]
        encoded_idiom = self.idiom_embedding(idiom_ids)  # [batch, 10， hidden_state]

        multiply_result = torch.einsum('abc,ac->abc', encoded_idiom, blank_states)  # [batch, 10， hidden_state]
        pooled_output = self.dropout(multiply_result)
        logits = self.classifier(pooled_output)
        # logits = self.classifier(multiply_result)  # [batch, 10, 1]
        logits = logits.view(-1, idiom_ids.shape[-1])  # [batch, 10]
        return logits
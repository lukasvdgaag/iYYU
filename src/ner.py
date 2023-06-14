import json
import os
import torch
from transformers import BertForTokenClassification, BertTokenizerFast, TrainingArguments, Trainer

class NERModel:
    def __init__(self, train_file='training_data/ner/ner_data.json', trained_model_dir='trained_models/ner', pretrained_model='bert-base-uncased', keyword_mappings='training_data/ner/keyword_mappings.json'):
        self.train_file = train_file
        self.keyword_mappings = keyword_mappings
        self.trained_model_dir = trained_model_dir
        self.pretrained_model = pretrained_model
        self.ner_already_trained = os.path.exists(self.trained_model_dir)
        self.label_to_index = {"O": 0, "setting_name": 1, "state": 2}
        self.index_to_label = {v: k for k, v in self.label_to_index.items()}
        self.model = BertForTokenClassification.from_pretrained(self.trained_model_dir) if self.ner_already_trained else BertForTokenClassification.from_pretrained(self.pretrained_model, num_labels=3)
        self.tokenizer = BertTokenizerFast.from_pretrained(self.pretrained_model)

        if not self.ner_already_trained:
            self.train()

    def encode_example(self, sentence):
        inputs = self.tokenizer(sentence['text'], is_split_into_words=True, padding='max_length', truncation=True, max_length=128)
        labels = [-100 if token_id==self.tokenizer.pad_token_id else self.label_to_index[label] for token_id, label in zip(inputs['input_ids'], sentence['ner'])]  
        labels += [-100] * (128 - len(labels))  # pad labels to the max length
        inputs['labels'] = labels
        return inputs

    def train(self):
        with open(self.train_file, 'r') as f:
            train_sentences = json.load(f)

        train_encodings = [self.encode_example(s) for s in train_sentences]
        train_encodings = [ {k: torch.tensor(v) for k, v in enc.items()} for enc in train_encodings]

        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=20,
            per_device_train_batch_size=64,
            weight_decay=0.01,
            seed=42,  # for reproducibility
            logging_steps=100,  # log loss every 100 steps
            # logging_dir='./logs',
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_encodings,
        )

        trainer.train()
        self.model.save_pretrained(self.trained_model_dir)

    def get_entities(self, sentence):
        inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=2)

        predicted_labels = [self.index_to_label[p] for p in predictions[0].tolist()]

        original_tokens = self.tokenizer.tokenize(sentence)
        aligned_labels = []
        current_tokens = []
        current_label = None

        for token, label in zip(original_tokens, predicted_labels):
            if token.startswith("##"):
                if current_tokens:
                    current_tokens[-1] += token[2:]
            else:
                if label != 'O':
                    current_tokens.append(token)
                    current_label = label
                else:
                    if current_label:
                        aligned_labels.append([' '.join(current_tokens), current_label])
                        current_tokens = []
                        current_label = None
    
        if current_label:
            aligned_labels.append([' '.join(current_tokens), current_label])

        return aligned_labels
    
    def get_keywords_from_entities(self, entities):
        with open(self.keyword_mappings, "r") as f:
          keyword_mappings = json.load(f)
    
        def get_key(value):
            for key, values in keyword_mappings.items():
                if value in values:
                    return key
            return None

        state = None
        setting = None

        # Loop through the entities and find the key in keyword_mappings for each entity
        for entity in entities:
            if entity[1] == 'state':
                state = get_key(entity[0])
            elif entity[1] == 'setting_name':
                setting = get_key(entity[0])

        return(state, setting)

    
# Test model
# model = NERModel()

# print("Predicted entities:", model.get_entities("How can I publish my profile?"))
# print("Predicted entities:", model.get_entities("How do I disable the connect with me setting?"))
# print("Predicted entities:", model.get_entities("How do i make myself visible in the search?"))
# print("Predicted entities:", model.get_entities("Can i make myself only findable to logged in users?"))

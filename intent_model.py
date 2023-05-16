import json
import os
import torch
from transformers import BertForSequenceClassification, BertTokenizer

class IntentModel:

    def __init__(self,  train_data, label_map, labels):
        self.initialize_model(label_map)
        self.train_model(train_data, labels)
        
    
    def initialize_model(self, label_map):
        self.model_exists = os.path.exists("trained_bert.pth")
        # Load the pre-trained BERT model and tokenizer
        self.model = torch.load("trained_bert.pth") if self.model_exists else BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(label_map))
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    def train_model(self, train_data, labels):
        if not self.model_exists:
            # Tokenize the training data and convert to tensors
            inputs = self.tokenizer.batch_encode_plus([data[0] for data in train_data], padding=True, truncation=True, return_tensors="pt")

            # Fine-tune the model on the training data
            optimizer = torch.optim.Adam(self.model.parameters(), lr=5e-4) #default 5e-5
            loss_fn = torch.nn.CrossEntropyLoss()
            for epoch in range(20):
                optimizer.zero_grad()
                outputs = self.model(inputs["input_ids"], attention_mask=inputs["attention_mask"], labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()

                print(f"Epoch {epoch+1}, Loss: {loss.item()}")

                # Evaluate the model on the training data
                predictions = outputs.logits.argmax(axis=1)
                accuracy = (predictions == labels).sum()
            torch.save(self.model, "trained_bert.pth")
        
    def get_model(self):
        return self.model
    
    def get_tokenizer(self):
        return self.tokenizer

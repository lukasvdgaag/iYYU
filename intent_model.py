import json
import os
import torch
from transformers import BertForSequenceClassification, BertTokenizer, AdamW
from torch.utils.data import Dataset, DataLoader

class IntentModel:
    def __init__(self,  train_data, label_map):
        self.train_data = train_data
        self.label_map = label_map
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        self.model = self.load_model()

    def load_model(self):
        if os.path.exists("trained_bert.pth"):
            return BertForSequenceClassification.from_pretrained("trained_bert.pth")
        else:
            return self.train_model()

    def train_model(self):
        # Set a random see for the models random number generator to ensure reproducibility
        torch.manual_seed(42)

        model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(self.label_map))

        # Tokenize the training data and convert to tensors
        inputs = self.tokenizer.batch_encode_plus([data[0] for data in self.train_data], padding=True, truncation=True, return_tensors="pt")
        labels = torch.tensor([self.label_map[data[1]] for data in self.train_data])

        dataset = IntentDataset(inputs, labels)
        data_loader = DataLoader(dataset, batch_size=16, shuffle=True)

        # Fine-tune the model on the training data
        optimizer = AdamW(model.parameters(), lr=5e-4) #default 5e-5
        num_epochs = 20

        for epoch in range(num_epochs):
            for batch in data_loader:
                outputs = model(**batch)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()

            print(f"Epoch {epoch+1}, Loss: {loss.item()}")

        # Save the model
        model.save_pretrained("trained_bert.pth")

        return model

    def get_intent(self, question):
        # Tokenize the question and convert to tensors
        inputs = self.tokenizer.encode_plus(question, padding=True, truncation=True, return_tensors="pt")

        # Get the model's prediction for the question
        with torch.no_grad():
            outputs = self.model(**inputs)
        predicted_label = list(self.label_map.keys())[list(self.label_map.values()).index(outputs.logits.argmax(axis=1)[0].item())]
        return predicted_label

class IntentDataset(Dataset):
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels

    def __len__(self):
        return len(self.inputs["input_ids"])

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.inputs.items()}
        item["labels"] = self.labels[idx]
        return item

import json
import os
import torch
import torch.nn as nn
from transformers import BertForTokenClassification, BertTokenizer, BertConfig, BertModel
from torch.nn import CrossEntropyLoss


class JointBERT(nn.Module):
    def __init__(self, num_labels, num_intent_labels):
        super(JointBERT, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.num_labels = num_labels
        self.num_intent_labels = num_intent_labels
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)
        self.intent_classifier = nn.Linear(self.bert.config.hidden_size, num_intent_labels)

    def forward(self, input_ids, attention_mask, intent_labels, slot_labels):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)

        last_hidden_state = outputs.last_hidden_state
        sequence_output = outputs.last_hidden_state
        pooled_output = last_hidden_state[:, 0, :]

        slot_logits = self.classifier(sequence_output)
        intent_logits = self.intent_classifier(pooled_output)

        total_loss = 0
        if intent_labels is not None and slot_labels is not None:
            loss_fct = CrossEntropyLoss()
            slot_loss = loss_fct(slot_logits.view(-1, self.num_labels), slot_labels.view(-1))
            intent_loss = loss_fct(intent_logits.view(-1, self.num_intent_labels), intent_labels.view(-1))
            total_loss = slot_loss + intent_loss
        return total_loss, slot_logits, intent_logits



class IntentModel:

    def __init__(self, train_data, intent_label_map, slot_label_map, intent_labels, slot_labels):
        self.train_data = train_data
        self.intent_label_map = intent_label_map
        self.slot_label_map = slot_label_map
        self.intent_labels = intent_labels

        # Processing slot_labels here
        slot_labels_list = [[slot_label_map[label] for label in data[2]] for data in train_data]
        self.slot_labels = torch.nn.utils.rnn.pad_sequence([torch.tensor(item) for item in slot_labels_list], batch_first=True)

        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        config = BertConfig.from_pretrained("bert-base-uncased")
        config.num_intent_labels = len(self.intent_label_map)
        config.num_labels = len(self.slot_label_map)
        config.output_hidden_states = True
        config.output_attentions = True
        num_intent_labels = len(set(intent_labels))
        config.pooler_output = True  # Add this line
        self.model = JointBERT(config, num_intent_labels)

        if os.path.exists("trained_bert.pth"):
            self.model.load_state_dict(torch.load("trained_bert.pth"))
        else:
            self.train_model()
        

    def train_model(self):
        torch.manual_seed(42)

        # Tokenize the training data and convert to tensors
        inputs = self.tokenizer.batch_encode_plus([data[0] for data in self.train_data], padding=True, truncation=True, return_tensors="pt")

        optimizer = torch.optim.Adam(self.model.parameters(), lr=5e-4) #default 5e-5
        for epoch in range(20):
            optimizer.zero_grad()
            loss, _, _ = self.model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"], 
                                    intent_labels=self.intent_labels, slot_labels=self.slot_labels)
            loss.backward()
            optimizer.step()
            print(f"Epoch {epoch+1}, Loss: {loss.item()}")

        torch.save(self.model.state_dict(), "trained_bert.pth")
        
    def get_model(self):
        return self.model
    
    def get_tokenizer(self):
        return self.tokenizer

    def get_intent_and_slots(self, question):
        inputs = self.tokenizer.encode_plus(question, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            _, intent_logits, slot_logits = self.model(inputs["input_ids"], inputs["attention_mask"])
        intent = list(self.intent_label_map.keys())[list(self.intent_label_map.values()).index(intent_logits.argmax(axis=1).item())]
        slots = [list(self.slot_label_map.keys())[list(self.slot_label_map.values()).index(slot)] for slot in slot_logits.argmax(axis=2).squeeze().tolist()[1:-1]]
        return intent, slots


    def evaluate_model(self, test_data):
        results = []

        total_document_correct_counts = 0
        total_document_counts = 0

        for data in test_data:
            correct_intent = data["intent"]

            questions_results = {
                "correct_intent": correct_intent,
                "train_questions": [],
                "test_questions": [],
                "test_questions_advanced": []
            }

            total_correct_counts = 0
            total_counts = 0

            # Loop over the question keys
            for key in ["train_questions", "test_questions", "test_questions_advanced"]:
                correct_count = 0

                # Check if questions array exists
                if key in data:
                    questions = data[key]
                    total_count = len(questions)

                    for question in questions:
                        predicted_intent, predicted_slots = self.get_intent_and_slots(question)
                        correctly_predicted = (predicted_intent == correct_intent)
                        # Add your slot evaluation logic here
                        if correctly_predicted:
                            correct_count += 1
                        question_result = {
                            "question": question,
                            "predicted_intent": predicted_intent,
                            "intent_correctly_predicted": correctly_predicted,
                            # Add your predicted slots here
                        }

                        questions_results[key].append(question_result)

                    questions_results[key + "_results"] = f"{correct_count} out of {total_count} correct"
                    total_correct_counts += correct_count
                    total_counts += total_count

            questions_results["total_correctness"] = round((total_correct_counts / total_counts) * 100, 2)

            results.append(questions_results)

            total_document_correct_counts += total_correct_counts
            total_document_counts += total_counts

        total_document_correctness = round((total_document_correct_counts / total_document_counts) * 100, 2)

        # Create a combined result object
        combined_result = {
            "results": results,
            "total_correct_counts": total_document_correct_counts,
            "total_counts": total_document_counts,
            "total_correctness": total_document_correctness
        }

        # Save results to a JSON file
        with open('evaluation_results.json', 'w') as outfile:
            json.dump(combined_result, outfile, indent=4)

        return combined_result



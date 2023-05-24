import json
import os
import torch
from transformers import BertForSequenceClassification, BertTokenizer

class IntentModel:

    def __init__(self,  train_data, label_map, labels):
        self.train_data = train_data
        self.label_map = label_map
        self.labels = labels
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        self.model = torch.load("trained_bert.pth") if os.path.exists("trained_bert.pth") else self.train_model()
        

    def train_model(self):
        # Set a random see for the models random number generator to ensure reproducibility
        torch.manual_seed(42)

        model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(self.label_map))
        # Tokenize the training data and convert to tensors
        inputs = self.tokenizer.batch_encode_plus([data[0] for data in self.train_data], padding=True, truncation=True, return_tensors="pt")

        # Fine-tune the model on the training data
        optimizer = torch.optim.Adam(model.parameters(), lr=5e-4) #default 5e-5
        loss_fn = torch.nn.CrossEntropyLoss()
        for epoch in range(20):
            optimizer.zero_grad()
            outputs = model(inputs["input_ids"], attention_mask=inputs["attention_mask"], labels=self.labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            print(f"Epoch {epoch+1}, Loss: {loss.item()}")

            # Evaluate the model on the training data
            predictions = outputs.logits.argmax(axis=1)
            accuracy = (predictions == self.labels).sum()
        
        # Save the model
        torch.save(model, "trained_bert.pth")

        return model
        
    def get_model(self):
        return self.model
    
    def get_tokenizer(self):
        return self.tokenizer

    def get_intent(self, question):
        # Tokenize the test question and convert to tensors
        inputs = self.tokenizer.encode_plus(question, padding=True, truncation=True, return_tensors="pt")

        # Get the model's prediction for the test question
        with torch.no_grad():
            outputs = self.model(inputs["input_ids"], attention_mask=inputs["attention_mask"])
        
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        
        predictions = logits.argmax(axis=1)
        predicted_label = list(self.label_map.keys())[list(self.label_map.values()).index(predictions[0].item())]
        
        confidence_scores = probabilities.squeeze().tolist()  # Convert to a list of confidence scores
        
        return predicted_label, confidence_scores


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
                        predicted_intent = self.get_intent(question)
                        correctly_predicted = (predicted_intent == correct_intent)
                        if correctly_predicted:
                            correct_count += 1
                        question_result = {
                            "question": question,
                            "predicted_intent": predicted_intent,
                            "intent_correctly_predicted": correctly_predicted
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



import json
import os
import torch
import random
from transformers import BertForSequenceClassification, BertTokenizer


class IntentModel:

    trained_bert_location = 'trained_models/intents/trained_bert.pth'

    def __init__(self, train_data, validation_data, label_map, train_labels, validation_labels):
        self.train_data = train_data
        self.validation_data = validation_data
        self.label_map = label_map
        self.train_labels = train_labels
        self.validation_labels = validation_labels
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        

        self.model = torch.load(self.trained_bert_location) if os.path.exists(self.trained_bert_location) else self.train_model()

    def train_model(self, num_epochs=15, learning_rate=0.0005):
        # Set a random seed for the models random number generator to ensure reproducibility
        torch.manual_seed(42)

        model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(self.label_map))
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        train_inputs = tokenizer.batch_encode_plus([data[0] for data in self.train_data], padding=True, truncation=True, return_tensors="pt")
        validation_inputs = tokenizer.batch_encode_plus([data[0] for data in self.validation_data], padding=True, truncation=True, return_tensors="pt")

        train_labels = self.train_labels
        validation_labels = self.validation_labels

        # Fine-tune the model on the training data
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        
        train_losses = []
        validation_losses = []

        for epoch in range(num_epochs):
            model.train()
            optimizer.zero_grad()
            train_outputs = model(train_inputs["input_ids"], attention_mask=train_inputs["attention_mask"], labels=train_labels)
            train_loss = train_outputs.loss
            train_loss.backward()
            optimizer.step()

            train_losses.append(train_loss.item())

            # Randomize the validation labels for better evaluation
            random.shuffle(validation_labels)

            # Evaluate the model on the validation data
            model.eval()
            with torch.no_grad():
                validation_outputs = model(validation_inputs["input_ids"], attention_mask=validation_inputs["attention_mask"], labels=validation_labels)
                validation_loss = validation_outputs.loss
                validation_losses.append(validation_loss.item())
                validation_predictions = validation_outputs.logits.argmax(axis=1)
                validation_accuracy = (validation_predictions == validation_labels).sum()

            print(f"Epoch {epoch+1}, Training Loss: {train_loss.item()}")

        torch.save(model, self.trained_bert_location)
        return model

    def test_best_model(self):
        print("Testing best model")
        torch.manual_seed(42)

        num_epochs_list = [10, 15, 20]
        learning_rate_list = [0.001, 0.0001, 0.0003, 0.003, 0.0005, 0.005, 0.0008, 0.008, 0.0009, 0.01, 0.00005, 0.00008]

        best_model = None
        best_accuracy = 0
        best_epoch = 0
        best_learning_rate = 0

        for num_epochs in num_epochs_list:
            for learning_rate in learning_rate_list:
                model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(self.label_map))
                tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
            

                train_inputs = tokenizer.batch_encode_plus([data[0] for data in self.train_data], padding=True, truncation=True, return_tensors="pt")
                validation_inputs = tokenizer.batch_encode_plus([data[0] for data in self.validation_data], padding=True, truncation=True, return_tensors="pt")

                train_labels = self.train_labels
                validation_labels = self.validation_labels

                # Fine-tune the model on the training data
                optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

                train_losses = []
                validation_losses = []

                for epoch in range(num_epochs):
                    model.train()
                    optimizer.zero_grad()
                    train_outputs = model(train_inputs["input_ids"], attention_mask=train_inputs["attention_mask"], labels=train_labels)
                    train_loss = train_outputs.loss
                    train_loss.backward()
                    optimizer.step()

                    train_losses.append(train_loss.item())

                    # Randomize the validation labels for better evaluation
                    random.shuffle(validation_labels)

                    # Evaluate the model on the validation data
                    model.eval()
                    with torch.no_grad():
                        validation_outputs = model(validation_inputs["input_ids"], attention_mask=validation_inputs["attention_mask"], labels=validation_labels)
                        validation_loss = validation_outputs.loss
                        validation_losses.append(validation_loss.item())
                        validation_predictions = validation_outputs.logits.argmax(axis=1)
                        validation_accuracy = (validation_predictions == validation_labels).sum()

                    print(f"Epoch {epoch+1}, Training Loss: {train_loss.item()}, Validation Loss: {validation_loss.item()}, Accuracy: {validation_accuracy.item()}")
                
                if validation_accuracy > best_accuracy:
                    best_accuracy = validation_accuracy
                    best_model = model
                    best_epoch = num_epochs
                    best_learning_rate = learning_rate


        print(f"Best accuracy: {best_accuracy}")
        print(f"Best epoch: {best_epoch}")
        print(f"Best learning rate: {best_learning_rate}")

        torch.save(best_model, self.trained_bert_location)
        return best_model

        
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
                        predicted_intent, confidence_scores = self.get_intent(question)
                        # print(f"Question: {question}, Predicted intent: {predicted_intent}, correct intent: {correct_intent}")
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
        with open('trained_models/intents/evaluation_results.json', 'w') as outfile:
            json.dump(combined_result, outfile, indent=4)

        return combined_result



import re
import random

# importing required sklearn libraries for feature extraction and models
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


# this function load sports and politics data from txt files
# each line is treated as one document
def load_data():

    # reading sports data
    with open("sports.txt", "r", encoding="utf-8") as f:
        sports = [line.strip() for line in f if line.strip()]

    # reading politics data
    with open("politics.txt", "r", encoding="utf-8") as f:
        politics = [line.strip() for line in f if line.strip()]

    # combining both class data
    X = sports + politics

    # creating labels for each document
    y = ["SPORTS"] * len(sports) + ["POLITICS"] * len(politics)

    return X, y


# this function do basic text preprocessing
# converting to lowercase and removing special characters
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text


# this function train model and evaluate performance
# it also print all metrics like accuracy, precision etc
def train_and_evaluate(name, model, X_train, X_test, y_train, y_test):

    # training the model
    model.fit(X_train, y_train)

    # predicting on test data
    preds = model.predict(X_test)

    # calculating different evaluation metrics
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, pos_label="SPORTS")
    rec = recall_score(y_test, preds, pos_label="SPORTS")
    f1 = f1_score(y_test, preds, pos_label="SPORTS")

    # printing results
    print(f"\nModel: {name}")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-score : {f1:.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, preds))

    return acc


# main function start from here
def main():

    # fixing random seed for reproducibility
    random.seed(42)

    print("=" * 60)
    print("SPORTS vs POLITICS TEXT CLASSIFICATION")
    print("=" * 60)

    # loading data
    X, y = load_data()

    # preprocessing all documents
    X = [preprocess(text) for text in X]

    # splitting data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples : {len(X_test)}")

    # using tf-idf with unigrams and bigrams
    print("\nUsing TF-IDF with Unigrams + Bigrams")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    # converting text into numerical vectors
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # defining different ml models
    models = {
        "Naive Bayes": MultinomialNB(),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Support Vector Machine": LinearSVC()
    }

    results = {}

    # training and evaluating each model
    for name, model in models.items():
        acc = train_and_evaluate(
            name, model, X_train_vec, X_test_vec, y_train, y_test
        )
        results[name] = acc

    # printing final comparison
    print("\n" + "=" * 60)
    print("FINAL MODEL COMPARISON (Accuracy)")
    print("=" * 60)

    for model, acc in results.items():
        print(f"{model:25s}: {acc:.4f}")

    # selecting best model based on accuracy
    best_model = max(results, key=results.get)
    print("\nBest Model:", best_model)

    # interactive prediction mode
    print("\nEnter a document to classify (type 'exit' to quit):")

    final_model = models[best_model]
    final_model.fit(X_train_vec, y_train)

    while True:
        text = input("\nInput: ")
        if text.lower() == "exit":
            break

        # preprocess and vectorize input text
        text = preprocess(text)
        vec = vectorizer.transform([text])

        # predicting class
        prediction = final_model.predict(vec)[0]
        print("Prediction:", prediction)


# program execution start here
if __name__ == "__main__":
    main()

import math
import random

# setting random seed so split result remains same every time
random.seed(300)

# this function read file line by line
# it convert text to lowercase and remove empty lines
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip().lower() for line in f if line.strip()]
    return lines


# simple tokenization using space split
# no advance nlp used here
def tokenize(sentence):
    return sentence.lower().split()


# this function train naive bayes model
# it count word freq for positive and negative sentences
def train_naive_bayes(pos_sentences, neg_sentences):

    vocab = set()

    pos_word_counts = {}
    neg_word_counts = {}

    pos_total_words = 0
    neg_total_words = 0

    # counting words in positive sentences
    for sent in pos_sentences:
        words = tokenize(sent)
        for w in words:
            vocab.add(w)
            pos_word_counts[w] = pos_word_counts.get(w, 0) + 1
            pos_total_words += 1

    # counting words in negative sentences
    for sent in neg_sentences:
        words = tokenize(sent)
        for w in words:
            vocab.add(w)
            neg_word_counts[w] = neg_word_counts.get(w, 0) + 1
            neg_total_words += 1

    vocab_size = len(vocab)

    # storing all model parameters in dictionary
    model = {
        "pos_word_counts": pos_word_counts,
        "neg_word_counts": neg_word_counts,
        "pos_total_words": pos_total_words,
        "neg_total_words": neg_total_words,
        "vocab_size": vocab_size,

        # calculating prior probabilities using log
        "pos_prior": math.log(len(pos_sentences) / (len(pos_sentences) + len(neg_sentences))),
        "neg_prior": math.log(len(neg_sentences) / (len(pos_sentences) + len(neg_sentences)))
    }

    return model


# this function predict sentiment of given sentence
# it calculate log probability for both class
def predict(sentence, model):

    words = tokenize(sentence)

    pos_log_prob = model["pos_prior"]
    neg_log_prob = model["neg_prior"]

    for w in words:

        # laplace smoothing is used here
        pos_count = model["pos_word_counts"].get(w, 0) + 1
        neg_count = model["neg_word_counts"].get(w, 0) + 1

        pos_prob = pos_count / (model["pos_total_words"] + model["vocab_size"])
        neg_prob = neg_count / (model["neg_total_words"] + model["vocab_size"])

        pos_log_prob += math.log(pos_prob)
        neg_log_prob += math.log(neg_prob)

    # final decision based on higher probability
    if pos_log_prob > neg_log_prob:
        return "POSITIVE"
    else:
        return "NEGATIVE"


# this function split data into train and validation
def train_test_split(data, split_ratio=0.8):
    random.shuffle(data)
    split = int(len(data) * split_ratio)
    return data[:split], data[split:]


# this function calculate accuracy on validation data
def evaluate(data, true_label, model):
    correct = 0
    for sentence in data:
        if predict(sentence, model) == true_label:
            correct += 1
    return correct / len(data)


# main function start from here
def main():

    # reading positive and negative data
    pos_data = read_file("pos.txt")
    neg_data = read_file("neg.txt")

    # splitting into train and validation
    pos_train, pos_val = train_test_split(pos_data)
    neg_train, neg_val = train_test_split(neg_data)

    # training naive bayes model
    model = train_naive_bayes(pos_train, neg_train)

    print("Naive Bayes Sentiment Classifier Trained.")

    # evaluating model on validation data
    pos_acc = evaluate(pos_val, "POSITIVE", model)
    neg_acc = evaluate(neg_val, "NEGATIVE", model)
    overall_acc = (pos_acc + neg_acc) / 2

    print(f"Validation Accuracy (Positive): {pos_acc * 100:.2f}%")
    print(f"Validation Accuracy (Negative): {neg_acc * 100:.2f}%")
    print(f"Overall Validation Accuracy: {overall_acc * 100:.2f}%\n")

    # interactive prediction mode
    print("Enter a sentence to predict sentiment (type 'exit' to quit).\n")

    while True:
        sentence = input("You: ")
        if sentence.lower() == "exit":
            break
        sentiment = predict(sentence, model)
        print("Prediction:", sentiment)


# program execution start here
if __name__ == "__main__":
    main()

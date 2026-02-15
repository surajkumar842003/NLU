import sys
from collections import defaultdict

# this function calculate frequency of all adjacent symbol pairs
# it go through each word and count how many times pair is comming
def get_stats(vocab):

    pairs = defaultdict(int)

    # vocab contains word as key and frequency as value
    for word, freq in vocab.items():
        symbols = word.split()

        # count pair of symbols like (l,o), (o,w) etc
        for i in range(len(symbols) - 1):
            pairs[(symbols[i], symbols[i + 1])] += freq

    return pairs


# this function merge the most frequent pair in whole vocab
# it replace bigram with new merged symbol
def merge_vocab(pair, vocab):

    new_vocab = {}

    # converting pair tuple into string
    bigram = ' '.join(pair)

    # replacement is merged symbol without space
    replacement = ''.join(pair)

    # replacing in all words of vocab
    for word in vocab:
        new_word = word.replace(bigram, replacement)
        new_vocab[new_word] = vocab[word]

    return new_vocab


# this is main byte pair encoding function
# it takes corpus and number of merges K
def byte_pair_encoding(corpus, K):

    vocab = defaultdict(int)

    # first create initial vocabulary at character level
    # also adding </w> to mark end of word
    for line in corpus:
        words = line.strip().split()
        for word in words:
            chars = ' '.join(list(word)) + ' </w>'
            vocab[chars] += 1

    # applying BPE merges K times
    for i in range(K):
        pairs = get_stats(vocab)

        # if no more pairs then stop early
        if not pairs:
            break

        # selecting most frequent pair
        best_pair = max(pairs, key=pairs.get)

        # merge selected pair in vocab
        vocab = merge_vocab(best_pair, vocab)

    return vocab


# main function starts from here
def main():

    # checking command line argument
    if len(sys.argv) != 2:
        print("Usage: python prob2.py corpus.txt")
        sys.exit(1)

    corpus_file = sys.argv[1]

    # reading corpus file
    try:
        with open(corpus_file, 'r', encoding='utf-8') as f:
            corpus = f.readlines()
    except FileNotFoundError:
        print("Error: corpus file not found.")
        sys.exit(1)

    # taking number of merges from user
    K = int(input("Enter number of BPE merges (K): "))

    # calling byte pair encoding function
    vocab = byte_pair_encoding(corpus, K)

    # printing final vocabulary
    print("\nFinal Vocabulary:")
    for word, freq in vocab.items():
        print(f"{word} : {freq}")


# program execution starts here
if __name__ == "__main__":
    main()

# PartA.py

"""
Assignment 1 - Part A: Word Frequencies

Run from the command line:
    python PartA.py <text_file>

Rules:
- A token is any sequence of letters or numbers
- Case-insensitive
- No regex or external libraries allowed
- Prints words sorted by frequency, then alphabetically
"""

import sys

def tokenize(filename):
    """
    Reads the text file and returns a list of tokens.
    Time complexity: O(n)
    """
    tokens = []
    word = ""

    try:
        with open(filename, "r", encoding = "utf-8", errors = "ignore") as file:
            for chunk in iter(lambda: file.read(8192), ""):
                for ch in chunk:
                    if ch.isascii() and ch.isalnum():
                        word += ch.lower()
                    else:
                        if word != "":
                            tokens.append(word)
                            word = ""
            # add last word if file ends with one
            if word != "":
                tokens.append(word)
    except FileNotFoundError:
        print("Error: file not found.", file = sys.stderr)
        return []
    except OSError as e:
        print(f"Error reading file: {e}", file = sys.stderr)
        return []
    return tokens

def computeWordFrequencies(tokens):
    """
    Counts how many times each token appears.
    Time complexity: O(T)
    """
    freq = {}
    for token in tokens:
        if token in freq:
            freq[token] += 1
        else:
            freq[token] = 1
    return freq

def printFrequencies(freq):
    """
    Prints "<token>\t<count>" sorted by decreasing frequency.
    Time complexity: O(U log U)
    """
    sorted_items = sorted(freq.items(), key = lambda x: (-x[1], x[0]))
    for token, count in sorted_items:
        print(f"{token}\t{count}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python PartA.py <text_file>", file = sys.stderr)
        return

    filename = sys.argv[1]
    tokens = tokenize(filename)
    freqs = computeWordFrequencies(tokens)
    printFrequencies(freqs)

if __name__ == "__main__":
#Overall: O(n) to tokenize + O(T) counting + O(U log U) sort
# n = file chars, T = tokens, U = unique tokens
    main()

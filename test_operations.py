"""
Test script to verify NLP operations work correctly.
This script tests the operations without MPI to ensure they function properly.
"""

import string
import sys


def read_file_lines(filepath):
    """Read all lines from a text file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def lowercase_text(sentences):
    """Convert all characters in each sentence to lowercase."""
    return [sentence.lower() for sentence in sentences]


def remove_punctuation(sentences):
    """Remove all punctuation symbols from each sentence."""
    result = []
    for sentence in sentences:
        cleaned = sentence.translate(str.maketrans('', '', string.punctuation))
        result.append(cleaned)
    return result


def remove_stopwords(sentences, stopwords_set):
    """Remove stopwords from each sentence."""
    result = []
    for sentence in sentences:
        words = sentence.split()
        filtered_words = [word for word in words if word not in stopwords_set]
        result.append(' '.join(filtered_words))
    return result


def compute_term_frequency(sentences, vocabulary):
    """Count how many times each vocabulary word appears across all sentences."""
    tf = {word: 0 for word in vocabulary}
    
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            if word in vocabulary:
                tf[word] += 1
    
    return tf


def compute_document_frequency(sentences, vocabulary):
    """Count in how many distinct sentences each vocabulary word appears."""
    df = {word: 0 for word in vocabulary}
    
    for sentence in sentences:
        words = sentence.split()
        sentence_vocab = set()
        for word in words:
            if word in vocabulary:
                sentence_vocab.add(word)
        
        for word in sentence_vocab:
            df[word] += 1
    
    return df


def preprocess_sentences(sentences, stopwords_set):
    """Apply all preprocessing operations."""
    lowercased = lowercase_text(sentences)
    no_punctuation = remove_punctuation(lowercased)
    preprocessed = remove_stopwords(no_punctuation, stopwords_set)
    return preprocessed


def test_example_from_description():
    """Test with the example from the project description."""
    print("=" * 60)
    print("Testing with example from project description")
    print("=" * 60)
    
    # Example sentences
    sentences = [
        "The cat, the old cat, sat on the mat; the cat was tired.",
        "A small cat chased the big dog! The cat didn't stop.",
        "Dogs are bigger than cats, but a cat is faster."
    ]
    
    # Vocabulary
    vocabulary = {'cat', 'dog', 'old'}
    
    # Stopwords
    stopwords = {'the', 'a', 'on', 'in', 'are', 'than', 'was', 'but'}
    stopwords_set = set(stopwords)
    
    print("\nOriginal sentences:")
    for i, sent in enumerate(sentences, 1):
        print(f"  {i}. {sent}")
    
    # Preprocess
    preprocessed = preprocess_sentences(sentences, stopwords_set)
    
    print("\nAfter preprocessing (lowercasing, punctuation removal, stopword removal):")
    for i, sent in enumerate(preprocessed, 1):
        print(f"  {i}. {sent}")
    
    # Compute TF
    tf = compute_term_frequency(preprocessed, vocabulary)
    
    print("\nTerm-Frequency (TF) Results:")
    for word in sorted(vocabulary):
        print(f"  {word}: {tf[word]}")
    
    # Expected: cat: 6, dog: 1, old: 1
    assert tf['cat'] == 6, f"Expected cat TF=6, got {tf['cat']}"
    assert tf['dog'] == 1, f"Expected dog TF=1, got {tf['dog']}"
    assert tf['old'] == 1, f"Expected old TF=1, got {tf['old']}"
    print("✓ TF results match expected values!")
    
    # Compute DF
    df = compute_document_frequency(preprocessed, vocabulary)
    
    print("\nDocument-Frequency (DF) Results:")
    for word in sorted(vocabulary):
        print(f"  {word}: {df[word]}")
    
    # Expected: cat: 3, dog: 1, old: 1
    assert df['cat'] == 3, f"Expected cat DF=3, got {df['cat']}"
    assert df['dog'] == 1, f"Expected dog DF=1, got {df['dog']}"
    assert df['old'] == 1, f"Expected old DF=1, got {df['old']}"
    print("✓ DF results match expected values!")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)


def test_with_sample_files():
    """Test with actual sample files."""
    print("\n" + "=" * 60)
    print("Testing with sample files")
    print("=" * 60)
    
    try:
        # Read sample files
        # sentences = read_file_lines('resources/sample_text.txt')
        # vocab_list = read_file_lines('resources/sample_vocab.txt')
        # stopwords_list = read_file_lines('resources/sample_stopwords.txt')

        sentences = read_file_lines('testcases/small_text.txt')
        vocab_list = read_file_lines('testcases/small_vocab.txt')
        stopwords_list = read_file_lines('testcases/small_stopwords.txt')
        
        vocabulary = set(vocab_list)
        stopwords_set = set(stopwords_list)
        
        print(f"\nLoaded {len(sentences)} sentences")
        print(f"Vocabulary size: {len(vocabulary)} words")
        print(f"Stopwords size: {len(stopwords_set)} words")
        
        # Show first few sentences
        print("\nFirst 3 original sentences:")
        for i, sent in enumerate(sentences[:3], 1):
            print(f"  {i}. {sent[:80]}..." if len(sent) > 80 else f"  {i}. {sent}")
        
        # Preprocess
        preprocessed = preprocess_sentences(sentences, stopwords_set)
        
        print("\nFirst 3 preprocessed sentences:")
        for i, sent in enumerate(preprocessed[:3], 1):
            print(f"  {i}. {sent[:80]}..." if len(sent) > 80 else f"  {i}. {sent}")
        
        # Compute TF
        tf = compute_term_frequency(preprocessed, vocabulary)
        
        print("\nTerm-Frequency (TF) Results:")
        for word in sorted(vocabulary):
            print(f"  {word}: {tf[word]}")
        
        # Compute DF
        df = compute_document_frequency(preprocessed, vocabulary)
        
        print("\nDocument-Frequency (DF) Results:")
        for word in sorted(vocabulary):
            print(f"  {word}: {df[word]}")
        
        print("\n✓ Sample file processing completed successfully!")
        
    except FileNotFoundError as e:
        print(f"\n⚠ Could not find sample files: {e}")
        print("Skipping sample file test.")


if __name__ == '__main__':
    test_example_from_description()
    test_with_sample_files()


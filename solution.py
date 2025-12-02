"""
CMPE 300: Analysis of Algorithms
Project 2: MPI-Based Parallel NLP System

Student Names: Ahmet Baha Bayrakçıoğlu | Arif Evren
Student IDs: 2022400051 | 2022400282

This program implements four MPI communication patterns for parallel NLP processing:
- Pattern #1: Parallel End-to-End Processing in Worker Processes
- Pattern #2: Linear Pipeline
- Pattern #3: Parallel Pipelines (Multiple Independent Pipelines)
- Pattern #4: End-to-End Processing with Task Parallelism
"""

import argparse
import string
from mpi4py import MPI

# Note: This implementation uses ONLY the following MPI functions as required:
# - comm.Get_rank()  → MPI_Comm_rank
# - comm.Get_size()  → MPI_Comm_size
# - comm.send()      → MPI_Send (point-to-point blocking send)
# - comm.recv()      → MPI_Recv (point-to-point blocking receive)
# 
# Prohibited operations (NOT used):
# - No collective operations (bcast, scatter, gather, reduce, allreduce, etc.)
# - No non-blocking operations (isend, irecv, wait, etc.)


def read_file_lines(filepath):
    """
    Read all lines from a text file.
    
    Args:
        filepath: Path to the text file
        
    Returns:
        List of lines (strings)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def lowercase_text(sentences):
    """
    Convert all characters in each sentence to lowercase.
    
    Args:
        sentences: List of sentences (strings)
        
    Returns:
        List of lowercase sentences
    """
    return [sentence.lower() for sentence in sentences]


def remove_punctuation(sentences):
    """
    Remove all punctuation symbols from each sentence.
    
    Args:
        sentences: List of sentences (strings)
        
    Returns:
        List of sentences with punctuation removed
    """
    result = []
    for sentence in sentences:
        # Remove all punctuation characters
        cleaned = sentence.translate(str.maketrans('', '', string.punctuation))
        result.append(cleaned)
    return result


def remove_stopwords(sentences, stopwords_set):
    """
    Remove stopwords from each sentence.
    
    Args:
        sentences: List of sentences (strings)
        stopwords_set: Set of stopwords to remove
        
    Returns:
        List of sentences with stopwords removed
    """
    result = []
    for sentence in sentences:
        # Split sentence into words, filter out stopwords, rejoin
        words = sentence.split()
        filtered_words = [word for word in words if word not in stopwords_set]
        result.append(' '.join(filtered_words))
    return result


def compute_term_frequency(sentences, vocabulary):
    """
    Count how many times each vocabulary word appears across all sentences.
    
    Args:
        sentences: List of preprocessed sentences (strings)
        vocabulary: Set of vocabulary words
        
    Returns:
        Dictionary mapping vocabulary words to their term frequencies
    """
    tf = {word: 0 for word in vocabulary}
    
    # Count occurrences of each vocabulary word across all sentences
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            if word in vocabulary:
                tf[word] += 1
    
    return tf


def compute_document_frequency(sentences, vocabulary):
    """
    Count in how many distinct sentences (documents) each vocabulary word appears.
    
    Args:
        sentences: List of preprocessed sentences (strings)
        vocabulary: Set of vocabulary words
        
    Returns:
        Dictionary mapping vocabulary words to their document frequencies
    """
    df = {word: 0 for word in vocabulary}
    
    # For each sentence, track which vocabulary words appear in it
    for sentence in sentences:
        words = sentence.split()
        sentence_vocab = set()
        for word in words:
            if word in vocabulary:
                sentence_vocab.add(word)
        
        # Increment DF for each unique vocabulary word in this sentence
        for word in sentence_vocab:
            df[word] += 1
    
    return df


def preprocess_sentences(sentences, stopwords_set):
    """
    Apply all preprocessing operations: lowercasing, punctuation removal, stopword removal.
    
    Args:
        sentences: List of original sentences
        stopwords_set: Set of stopwords to remove
        
    Returns:
        List of preprocessed sentences
    """
    # Step 1: Lowercase
    lowercased = lowercase_text(sentences)
    
    # Step 2: Remove punctuation
    no_punctuation = remove_punctuation(lowercased)
    
    # Step 3: Remove stopwords
    preprocessed = remove_stopwords(no_punctuation, stopwords_set)
    
    return preprocessed


def pattern1(comm, rank, size, sentences, vocabulary, stopwords_set):
    """
    Pattern #1: Parallel End-to-End Processing in Worker Processes
    
    The manager divides text into balanced chunks and distributes them to workers.
    Each worker performs preprocessing and TF counting, then returns results to manager.
    """
    if rank == 0:  # Manager process
        num_workers = size - 1
        num_sentences = len(sentences)
        
        # Divide sentences into balanced chunks (approximately equal number of sentences per worker)
        sentences_per_worker = num_sentences // num_workers
        remainder = num_sentences % num_workers
        
        # Distribute chunks to workers
        start_idx = 0
        for worker_rank in range(1, size):
            # Calculate chunk size for this worker
            chunk_size = sentences_per_worker
            if worker_rank <= remainder:
                chunk_size += 1
            
            end_idx = start_idx + chunk_size
            chunk = sentences[start_idx:end_idx]
            
            # Send chunk to worker
            comm.send(chunk, dest=worker_rank, tag=1)
            start_idx = end_idx
        
        # Collect TF results from all workers
        aggregated_tf = {word: 0 for word in vocabulary}
        for worker_rank in range(1, size):
            worker_tf = comm.recv(source=worker_rank, tag=2)
            # Aggregate results
            for word in vocabulary:
                aggregated_tf[word] += worker_tf[word]
        
        # Print results
        print("Pattern #1 Results - Term Frequencies:")
        for word in sorted(vocabulary):
            print(f"{word}: {aggregated_tf[word]}")
    
    else:  # Worker process
        # Receive chunk from manager
        chunk = comm.recv(source=0, tag=1)
        
        # Preprocess chunk
        preprocessed = preprocess_sentences(chunk, stopwords_set)
        
        # Compute TF
        tf = compute_term_frequency(preprocessed, vocabulary)
        
        # Send TF results back to manager
        comm.send(tf, dest=0, tag=2)


def pattern2(comm, rank, size, sentences, vocabulary, stopwords_set):
    """
    Pattern #2: Linear Pipeline
    
    Each worker performs exactly one stage of the NLP pipeline.
    Data flows sequentially through the pipeline in chunks.
    """
    if rank == 0:  # Manager process
        num_sentences = len(sentences)
        
        # Determine chunk size (divide by value between 5 and 20)
        chunk_divisor = 10  # Can be adjusted between 5-20
        chunk_size = max(1, num_sentences // chunk_divisor)
        
        # Send chunks to Worker 1
        chunk_idx = 0
        while chunk_idx < num_sentences:
            chunk = sentences[chunk_idx:chunk_idx + chunk_size]
            comm.send(chunk, dest=1, tag=1)
            chunk_idx += chunk_size
        
        # Send termination signal to Worker 1
        comm.send(None, dest=1, tag=1)
        
        # Receive final TF results from Worker 4
        final_tf = comm.recv(source=4, tag=4)
        
        # Print results
        print("Pattern #2 Results - Term Frequencies:")
        for word in sorted(vocabulary):
            print(f"{word}: {final_tf[word]}")
    
    elif rank == 1:  # Worker 1: Lowercasing
        # tf_accumulator = {word: 0 for word in vocabulary}             TODO: BABA BUNU CURSOR KOYMUŞ GEREKSİZ DİYE KALDIRDIM AMA GEREKEBİLİR BELKİ SEN DE Bİ BAKSAN İYİ OLUR
        
        while True:
            chunk = comm.recv(source=0, tag=1)
            if chunk is None:  # Termination signal
                comm.send(None, dest=2, tag=2)
                break
            
            # Apply lowercasing
            processed = lowercase_text(chunk)
            
            # Send to Worker 2
            comm.send(processed, dest=2, tag=2)
        
        # Send accumulated TF to Worker 4 (will be empty, but needed for synchronization)
        # comm.send(tf_accumulator, dest=4, tag=4)      TODO: (üstteki kaldırdığımdan dolayı)       BABA BUNU CURSOR KOYMUŞ GEREKSİZ DİYE KALDIRDIM AMA GEREKEBİLİR BELKİ SEN DE Bİ BAKSAN İYİ OLUR
    
    elif rank == 2:  # Worker 2: Punctuation Removal
        while True:
            chunk = comm.recv(source=1, tag=2)
            if chunk is None:  # Termination signal
                comm.send(None, dest=3, tag=3)
                break
            
            # Apply punctuation removal
            processed = remove_punctuation(chunk)
            
            # Send to Worker 3
            comm.send(processed, dest=3, tag=3)
    
    elif rank == 3:  # Worker 3: Stopword Removal
        while True:
            chunk = comm.recv(source=2, tag=3)
            if chunk is None:  # Termination signal
                comm.send(None, dest=4, tag=4)
                break
            
            # Apply stopword removal
            processed = remove_stopwords(chunk, stopwords_set)
            
            # Send to Worker 4
            comm.send(processed, dest=4, tag=4)
    
    elif rank == 4:  # Worker 4: TF Counting
        tf_accumulator = {word: 0 for word in vocabulary}
        
        while True:
            chunk = comm.recv(source=3, tag=4)
            if chunk is None:  # Termination signal
                break
            
            # Compute TF for this chunk
            chunk_tf = compute_term_frequency(chunk, vocabulary)
            
            # Accumulate TF results
            for word in vocabulary:
                tf_accumulator[word] += chunk_tf[word]
        
        # Send final TF results to manager
        comm.send(tf_accumulator, dest=0, tag=4)


def pattern3(comm, rank, size, sentences, vocabulary, stopwords_set):
    """
    Pattern #3: Parallel Pipelines (Multiple Independent Pipelines)
    
    Multiple independent linear pipelines operate simultaneously.
    Each pipeline has 4 stages (lowercasing, punctuation removal, stopword removal, TF counting).
    """
    num_pipelines = (size - 1) // 4  # Each pipeline needs 4 workers
    pipeline_id = (rank - 1) // 4 if rank > 0 else -1
    stage_in_pipeline = (rank - 1) % 4 if rank > 0 else -1
    
    if rank == 0:  # Manager process
        num_sentences = len(sentences)
        
        # First division: divide sentences into larger chunks (one per pipeline)
        sentences_per_pipeline = num_sentences // num_pipelines
        remainder = num_sentences % num_pipelines
        
        # Determine chunk size for internal pipeline chunking (divide by value between 5-20)
        chunk_divisor = 10
        small_chunk_size = max(1, sentences_per_pipeline // chunk_divisor)
        
        # Distribute chunks to pipelines in a round-robin fashion
        # Each pipeline gets its share of sentences, then we send them in small chunks
        start_idx = 0
        pipeline_chunks = []
        for pipeline_idx in range(num_pipelines):
            chunk_size = sentences_per_pipeline
            if pipeline_idx < remainder:
                chunk_size += 1
            
            end_idx = start_idx + chunk_size
            pipeline_chunk = sentences[start_idx:end_idx]
            pipeline_chunks.append(pipeline_chunk)
            start_idx = end_idx
        
        # Send chunks to each pipeline's first worker
        # For each pipeline, send its sentences in small chunks
        for pipeline_idx in range(num_pipelines):
            first_worker_rank = 1 + pipeline_idx * 4
            pipeline_sentences = pipeline_chunks[pipeline_idx]
            
            # Send small chunks to this pipeline
            chunk_idx = 0
            while chunk_idx < len(pipeline_sentences):
                small_chunk = pipeline_sentences[chunk_idx:chunk_idx + small_chunk_size]
                comm.send(small_chunk, dest=first_worker_rank, tag=1)
                chunk_idx += small_chunk_size
            
            # Send termination signal to this pipeline
            comm.send(None, dest=first_worker_rank, tag=1)
        
        # Collect TF results from last stage of each pipeline
        aggregated_tf = {word: 0 for word in vocabulary}
        for pipeline_idx in range(num_pipelines):
            last_worker_rank = 4 + pipeline_idx * 4
            pipeline_tf = comm.recv(source=last_worker_rank, tag=4)
            # Aggregate results
            for word in vocabulary:
                aggregated_tf[word] += pipeline_tf[word]
        
        # Print results
        print("Pattern #3 Results - Term Frequencies:")
        for word in sorted(vocabulary):
            print(f"{word}: {aggregated_tf[word]}")
    
    elif stage_in_pipeline == 0:  # Stage 1: Lowercasing (ranks 1, 5, 9, ...)
        # Receive chunks from manager and process them
        while True:
            chunk = comm.recv(source=0, tag=1)
            if chunk is None:  # Termination signal
                comm.send(None, dest=rank + 1, tag=2)
                break
            
            # Apply lowercasing
            processed = lowercase_text(chunk)
            
            # Send to next stage
            comm.send(processed, dest=rank + 1, tag=2)
    
    elif stage_in_pipeline == 1:  # Stage 2: Punctuation Removal (ranks 2, 6, 10, ...)
        while True:
            chunk = comm.recv(source=rank - 1, tag=2)
            if chunk is None:
                comm.send(None, dest=rank + 1, tag=3)
                break
            
            processed = remove_punctuation(chunk)
            comm.send(processed, dest=rank + 1, tag=3)
    
    elif stage_in_pipeline == 2:  # Stage 3: Stopword Removal (ranks 3, 7, 11, ...)
        while True:
            chunk = comm.recv(source=rank - 1, tag=3)
            if chunk is None:
                comm.send(None, dest=rank + 1, tag=4)
                break
            
            processed = remove_stopwords(chunk, stopwords_set)
            comm.send(processed, dest=rank + 1, tag=4)
    
    elif stage_in_pipeline == 3:  # Stage 4: TF Counting (ranks 4, 8, 12, ...)
        tf_accumulator = {word: 0 for word in vocabulary}
        
        while True:
            chunk = comm.recv(source=rank - 1, tag=4)
            if chunk is None:
                break
            
            chunk_tf = compute_term_frequency(chunk, vocabulary)
            for word in vocabulary:
                tf_accumulator[word] += chunk_tf[word]
        
        comm.send(tf_accumulator, dest=0, tag=4)


def pattern4(comm, rank, size, sentences, vocabulary, stopwords_set):
    """
    Pattern #4: End-to-End Processing with Task Parallelism
    
    Workers perform preprocessing, then exchange data in pairs.
    Even-ranked workers compute DF, odd-ranked workers compute TF.
    """
    num_workers = size - 1
    
    if rank == 0:  # Manager process
        num_sentences = len(sentences)
        
        # Divide sentences into balanced chunks
        sentences_per_worker = num_sentences // num_workers
        remainder = num_sentences % num_workers
        
        # Distribute chunks to workers
        start_idx = 0
        for worker_rank in range(1, size):
            chunk_size = sentences_per_worker
            if worker_rank <= remainder:
                chunk_size += 1
            
            end_idx = start_idx + chunk_size
            chunk = sentences[start_idx:end_idx]
            comm.send(chunk, dest=worker_rank, tag=1)
            start_idx = end_idx
        
        # Collect TF and DF results
        aggregated_tf = {word: 0 for word in vocabulary}
        aggregated_df = {word: 0 for word in vocabulary}
        
        for worker_rank in range(1, size):
            if worker_rank % 2 == 1:  # Odd rank: TF
                worker_tf = comm.recv(source=worker_rank, tag=3)
                for word in vocabulary:
                    aggregated_tf[word] += worker_tf[word]
            else:  # Even rank: DF
                worker_df = comm.recv(source=worker_rank, tag=4)
                for word in vocabulary:
                    aggregated_df[word] += worker_df[word]
        
        # Print results
        print("Pattern #4 Results - Term Frequencies:")
        for word in sorted(vocabulary):
            print(f"{word}: {aggregated_tf[word]}")
        print("Pattern #4 Results - Document Frequencies:")
        for word in sorted(vocabulary):
            print(f"{word}: {aggregated_df[word]}")
    
    else:  # Worker process
        # Receive chunk from manager
        chunk = comm.recv(source=0, tag=1)
        
        # Preprocess chunk
        preprocessed = preprocess_sentences(chunk, stopwords_set)
        
        # Determine partner rank for data exchange
        if rank % 2 == 1:  # Odd rank
            partner_rank = rank + 1
        else:  # Even rank
            partner_rank = rank - 1
        
        # Data exchange: avoid deadlock by having even ranks send first, odd ranks receive first
        if rank % 2 == 0:  # Even rank: send first
            comm.send(preprocessed, dest=partner_rank, tag=2)
            partner_data = comm.recv(source=partner_rank, tag=2)
        else:  # Odd rank: receive first
            partner_data = comm.recv(source=partner_rank, tag=2)
            comm.send(preprocessed, dest=partner_rank, tag=2)
        
        # Combine data
        combined_data = preprocessed + partner_data
        
        # Split tasks: even ranks compute DF, odd ranks compute TF
        if rank % 2 == 1:  # Odd rank: compute TF
            tf = compute_term_frequency(combined_data, vocabulary)
            comm.send(tf, dest=0, tag=3)
        else:  # Even rank: compute DF
            df = compute_document_frequency(combined_data, vocabulary)
            comm.send(df, dest=0, tag=4)


def main():
    """Main function to parse arguments and execute the selected pattern."""
    parser = argparse.ArgumentParser(description='MPI-Based Parallel NLP System')
    parser.add_argument('--text', type=str, required=True, help='Path to input text file')
    parser.add_argument('--vocab', type=str, required=True, help='Path to vocabulary file')
    parser.add_argument('--stopwords', type=str, required=True, help='Path to stopwords file')
    parser.add_argument('--pattern', type=int, choices=[1, 2, 3, 4], required=True,
                        help='Processing pattern (1, 2, 3, or 4)')
    
    args = parser.parse_args()
    
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Read input files (all processes need vocabulary and stopwords)
    if rank == 0:
        sentences = read_file_lines(args.text)
        vocab_list = read_file_lines(args.vocab)
        stopwords_list = read_file_lines(args.stopwords)
    else:
        sentences = None
        vocab_list = None
        stopwords_list = None
    
    # Broadcast vocabulary and stopwords to all processes
    # Since we can only use Send/Recv, we'll have rank 0 send to all others
    if rank == 0:
        for other_rank in range(1, size):
            comm.send(vocab_list, dest=other_rank, tag=10)
            comm.send(stopwords_list, dest=other_rank, tag=11)
        vocabulary = set(vocab_list)
        stopwords_set = set(stopwords_list)
    else:
        vocab_list = comm.recv(source=0, tag=10)
        stopwords_list = comm.recv(source=0, tag=11)
        vocabulary = set(vocab_list)
        stopwords_set = set(stopwords_list)
    
    # Validate process count for each pattern (rank 0 decides, then informs all ranks)
    config_ok = True
    if rank == 0:
        if args.pattern == 1 and size < 2:
            print("Error: Pattern #1 requires at least 2 processes (1 manager + 1 worker)")
            config_ok = False
        elif args.pattern == 2 and size != 5:
            print(f"Error: Pattern #2 requires exactly 5 processes, got {size}")
            config_ok = False
        elif args.pattern == 3 and (size - 1) % 4 != 0:
            print(f"Error: Pattern #3 requires size = 1 + 4i (i >= 1), got {size}")
            config_ok = False
        elif args.pattern == 4 and (size - 1) % 2 != 0:
            print(f"Error: Pattern #4 requires size = 1 + 2i (i >= 1), got {size}")
            config_ok = False
        
        # Inform all other ranks about validity
        for other_rank in range(1, size):
            comm.send(config_ok, dest=other_rank, tag=99)
    else:
        config_ok = comm.recv(source=0, tag=99)
    
    # If configuration is invalid, all ranks exit without entering any pattern
    if not config_ok:
        return
    
    # Execute the selected pattern
    if args.pattern == 1:
        pattern1(comm, rank, size, sentences, vocabulary, stopwords_set)
    elif args.pattern == 2:
        pattern2(comm, rank, size, sentences, vocabulary, stopwords_set)
    elif args.pattern == 3:
        pattern3(comm, rank, size, sentences, vocabulary, stopwords_set)
    elif args.pattern == 4:
        pattern4(comm, rank, size, sentences, vocabulary, stopwords_set)


if __name__ == '__main__':
    main()


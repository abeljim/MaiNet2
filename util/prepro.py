import math 
import os 
import random 
import sys
import pickle 
from tqdm import tqdm, trange 

import tokenization



# allows for large files to be dumped safely 
def pickle_dump_file(obj, filepath):
    max_bytes = 2**31 - 1
    bytes_out = pickle.dumps(obj)
    num_bytes = sys.getsizeof(bytes_out)
    dir = filepath[0:filepath.rfind('/')]
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(filepath, 'wb') as file_out:
        for idx in range(0, num_bytes, max_bytes):
            file_out.write(bytes_out[idx:idx + max_bytes])

# loads dumped file 
def pickle_load_file(obj, filepath):
    max_bytes = 2**31 - 1
    input_size = os.path.getsize(filepath)
    bytes_in = bytearray(0)
    with open(filepath, 'rb') as file_in:
        for _ in range(0, input_size, max_bytes):
            bytes_in += file_in.read(max_bytes)
    obj = pickle.loads(bytes_in)
    return obj 

# converts dataset 
def convert_examples_to_features(examples, tokenizer, max_seq_length,
                                 doc_stride, max_query_length, is_training):

    unique_id = 1000000000

    features = [] 


def squad_prepro(args):
    tokenizer = tokenization.FullTokenizer(
        vocab_file=args.vocab_file, do_lower_case=args.do_lower_case)

    #train_examples = read_squad_examples(input_file=args.train_file, is_training=True)
    #num_train_steps = int(
        #len(train_examples) / args.train_batch_size / args.gradient_accumulation_steps * args.num_train_epochs)

    #convert_examples_to_features(
            #examples=train_examples,
            #tokenizer=tokenizer,
            #max_seq_length=args.max_seq_length,
            #doc_stride=args.doc_stride,
            #max_query_length=args.max_query_length,
            #is_training=True)

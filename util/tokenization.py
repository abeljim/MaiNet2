import collections 
import unicodedata 

# converts code to unicode utf-8
def convert_to_unicode(text):

    if isinstance(text, str):
        return text 
    elif isinstance(text, bytes):
        return text.decode("utf-8", "ignore")
    else:
        return ValueError("Unsupported string type: %s" % (type(text)))

# loads vocab into dictionary 
# each word as  unique index value 
def load_vocab(vocab_file):
    vocab = collections.OrderedDict()
    index = 0
    with open(vocab_file, "r") as reader:
        while True:
            token = convert_to_unicode(reader.readline())
            if not token:
                break
            token = token.strip()
            vocab[token] = index 
            index += 1
    return vocab 

# convert sequence of tokens into ids using vocab 
def convert_tokens_to_ids(vocab, tokens):
    ids = [] 
    for token in tokens:
        ids.append(vocab[token])
    return ids 

# splits text by spaces removes whitespaces
def whitespace_tokenize(text):
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens 

# End to end Tokenization 
# this is the main function 
class FullTokenizer(object):

    def __init__(self, vocab_file, do_lower_case=True):
        self.vocab = load_vocab(vocab_file) 
        self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case)
        self.wordpiece_tokenizer = WordpieceTokenizer(vocab=self.vocab)
    
    def tokenize(self, text): 
        split_tokens = [] 
        for token in self.basic_tokenizer.tokenize(text):
            for sub_token in self.wordpiece_tokenizer.tokenize(token):
                split_tokens.append(sub_token)
        
        return split_tokens 
    
    def convert_tokens_to_ids(self, tokens):
        return convert_tokens_to_ids(self.vocab, tokens)

# runs punctuation splitting, lower casing 
class BasicTokenizer(object):

    def __init__(self, do_lower_case=True):
        self.do_lower_case = do_lower_case
    
    def tokenize(self, text): 
        text = convert_to_unicode(text)
        text = self._clean_text(text)
        orig_tokens = whitespace_tokenize(text)
        split_token = [] 

        for token in orig_tokens: 
            if self.do_lower_case:
                token = token.lower() 
                token = self._run_strip_accents(token)
            split_token.extend(self._run_split_on_punc(token))
        
        output_tokens = whitespace_tokenize(" ".join(split_token))
        return output_tokens 
    
    # removes accents from text 
    def _run_strip_accents(self, text):
        text = unicodedata.normalize("NFD", text)
        output = [] 
        for char in text:
            cat = unicodedata.category(char) 
            if cat == "Mn":
                continue
            output.append(char) 
        return "".join(output) 

    # splits punctuation splitting 
    def _run_split_on_punc(self,text):
        chars = list(text) 
        i = 0
        start_new_word = True 
        output = [] 
        while i < len(chars): 
            char = chars[i]
            if _is_punctuation(char): 
                output.append([char])
                start_new_word: True 
            else: 
                if start_new_word:
                    output.append([])
                start_new_word = False
                output[-1].append(char) 
            i += 1
        
        return ["".join(x) for x in output] 
    
    #removes invalid charecters and cleans whitespaces 
    def _clean_text(self,text): 
        output = [] 
        for char in text:
            cp = ord(char)
            if cp == 0 or cp == 0xfffd or _is_control(char):
                continue
            if _is_whitespace(char):
                output.append(" ")
            else:
                output.append(char) 
        return "".join(output) 


# checks if char is whitespace 
def _is_whitespace(char):
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True 
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False

# checks if char is control character
def _is_control(char): 
    if  char == "\t" or char == "\n" or char == "\r":
        return False 
    cat = unicodedata.category(char)
    if cat.startswith("C"):
        return True 
    return False 

# checks if char is punctuation character 
def _is_punctuation(char):
    cp = ord(char) 
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
            (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False

# turns text into word pieces 
class WordpieceTokenizer(object):
    def __init__(self, vocab, unk_token="[UNK]", max_input_chars_per_word=100):
        self.vocab = vocab 
        self.unk_token = unk_token
        self.max_input_chars_per_word = max_input_chars_per_word
    
    def tokenize(self, text):
        text = convert_to_unicode(text) 
        output_tokens = []

        for token in whitespace_tokenize(text):
            chars = list(token)
            if len(chars) > self.max_input_chars_per_word:
                output_tokens.append(self.unk_token)
                continue 
            
            is_bad = False 
            start = 0 
            sub_tokens = [] 
            while start < len(chars):
                end = len(chars)
                cur_substr = None 
                while start < end: 
                    substr = "".join(chars[start:end])
                    if start > 0:
                        substr = "##" + substr 
                    if substr in self.vocab: 
                        cur_substr = substr 
                        break 
                    end -= 1
                if cur_substr is None: 
                    is_bad = True 
                    break 
            if is_bad:
                output_tokens.append(self.unk_token)
            else: 
                output_tokens.extend(sub_tokens)
        return output_tokens 
            



    

    


    







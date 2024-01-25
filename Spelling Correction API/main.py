from fastapi import FastAPI
import time

app = FastAPI()

# Structure of a Trie node
class TrieNode:
    def __init__(self):
        # Store address of a character
        self.trie = {}
        # Check if the character is
        # the last character of a string or not
        self.isEnd = False

# Function to insert a string into Trie
def insert_trie(root, s):
    temp = root
    # Traverse the string, s
    for char in s:
        char_code = ord(char)
        if char_code not in temp.trie:
            # Initialize a node
            temp.trie[char_code] = TrieNode()
        # Update temp
        temp = temp.trie[char_code]

    # Mark the last character of the string to true
    temp.isEnd = True

# Function to print suggestions of the string
def print_suggestions(root, res, corrections):
    # If the current character is the last character of a string
    if root.isEnd:
        corrections.add(res)

    # Iterate over all possible characters of the string
    for i in root.trie.keys():
        # If the current character is present in the Trie
        res_list = list(res)
        res_list.append(chr(i))
        print_suggestions(root.trie[i], "".join(res_list), corrections)

# Function to check if the string is present in Trie or not
def check_present(root, key):
    corrections = set()
    # Traverse the string
    temp = root
    for char in key:
        char_code = ord(char)
        # If the current character is not present in the Trie
        if char_code not in temp.trie:
            break
        # Update temp
        temp = temp.trie[char_code]

    print_suggestions(temp, key, corrections)
    return list(corrections)

@app.get("/spelling-correction")
async def spelling_correction(word: str):
    # Record the start time
    start_time = time.time()

    # Initialize Trie with Arabic words
    root = TrieNode()
    arabic_dictionary = ['عربية', 'عربي', 'عرب', 'غربية', 'بحر', 'مدرسة', 'جامعة', 'كتاب', 'قلم', 'فاكهة', 'خضار',
                         'سماء', 'أرض', 'شمس', 'قمر', 'نجمة', 'سمك', 'طائر', 'زهرة', 'صحراء', 'جبل', 'بحيرة', 'نهر',
                         'شلال', 'سفينة', 'سفر', 'رياضة', 'فن', 'ثقافة', 'تكنولوجيا', 'علوم']
    for arabic_word in arabic_dictionary:
        insert_trie(root, arabic_word)

    # Check if the input word is correct or suggest corrections
    corrections = check_present(root, word)

    # Record the end time
    end_time = time.time()

    # Calculate the response time
    response_time = end_time - start_time

    return {"input_word": word, "corrections": corrections, "response_time": response_time}

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)

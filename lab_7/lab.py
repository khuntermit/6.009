# NO IMPORTS!
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
class Trie:
    ##################################################
    ## basic methods
    ##################################################

    def __init__(self):
        self.frequency = 0
        self.children = {}

    # add word/frequency to the trie.  Increment frequency
    # if no value supplied.
    def insert(self, word, frequency=None):

        if len(word) == 0:
            if frequency is None:
                self.frequency += 1
            else:
                self.frequency = frequency
            return

        key = word[0]

        if key in self.children:
            self.children[key].insert(word[1:], frequency)

        else:
            node = Trie()
            self.children[key] = node
            node.insert(word[1:], frequency)

    # return trie node for specified prefix, None if not in trie
    def find(self, prefix):

        if prefix is '':
            return self

        # reaches the end of the branch
        if prefix[0] in self.children:
            return self.children[prefix[0]].find(prefix[1:])
        return None

    def walk_tree(self, prefix):
        if self.frequency > 0:
            yield [prefix, self.frequency]

        for letter in self.children:
            child_tree = self.children[letter]
            yield from child_tree.walk_tree(prefix + letter)

    # is word in trie? return True or False
    def __contains__(self, word):
        node = self.find(word)
        if node is None:
            return False
        return node.frequency > 0

    # return list of [word,freq] pairs for all words in
    # this trie and its children
    def __iter__(self):
        return self.walk_tree('')

    ##################################################
    ## additional methods
    ##################################################

    # return the list of N most-frequently occurring words that start with prefix.
    def autocomplete(self, prefix, N):
        word_list = []

        prefix_node = self.find(prefix)
        if prefix_node is not None:
            for word, freq in prefix_node:
                word_list.append((prefix + word, freq))
            word_list = sorted(word_list, key=lambda x: x[1], reverse=True)
            word_list = [word for word, freq in word_list]
            return word_list[0:N]

        return word_list

    # change any one character a-z at any place in the word
    def replacement(self, word):
        global alphabet

        valid = []
        for index in range(0, len(word)):
            for a in alphabet:
                temp_word = word[:index] + a + word[index + 1:]
                if temp_word in self:
                    valid.append((temp_word, self.find(temp_word).frequency))
        return valid

    # add any one character a-z at any place in the word
    def insertion(self, word):
        global alphabet

        valid = []
        for index in range(0, len(word) + 1):
            for a in alphabet:
                if index < 0:
                    temp_word = a + word
                elif 0 <= index < len(word):
                    temp_word = word[:index] + a + word[index:]
                else:
                    temp_word = word + a
                if temp_word in self:
                    valid.append((temp_word, self.find(temp_word).frequency))
        return valid

    # remove any one character from the word
    def deletion(self, word):
        valid = []
        for index in range(len(word)):
            temp_word = word[:index] + word[index+1:]
            if temp_word in self:
                valid.append((temp_word, self.find(temp_word).frequency))
        return valid

    def transpose(self, word):
        valid = []
        for ind in range(len(word) - 1):
            # transpose
            seq = word[ind: ind + 2]
            seq = seq[::-1]
            temp = word[:ind] + seq + word[ind + 2:]
            if temp in self:
                valid.append((temp, self.find(temp).frequency))
        return valid

    # return the list of N most-frequent words that start with prefix or that
    # are valid words that differ from prefix by a small edit
    def autocorrect(self, prefix, N):
        c = len(self.autocomplete(prefix, N))
        if c >= N:
            return self.autocomplete(prefix, N)

        length = N - c
        word_list = self.transpose(prefix) + self.replacement(prefix) + self.insertion(prefix) + self.deletion(prefix)
        word_list = set(word_list)
        word_list = list(word_list)
        word_list = sorted(word_list, key=lambda x: x[1], reverse=True)
        word_list = [word for word, freq in word_list]

        autocomplete = self.autocomplete(prefix, N)
        for word in word_list:
            if word in autocomplete:
                word_list.remove(word)

        return autocomplete + word_list[0:length]

    # true if matches, false otherwise
    def recurse_filter(self, pattern, word):
        if len(pattern) == 0 and len(word) == 0:
            return True
        if len(word) == 0 and pattern == '*':
            return True
        if len(pattern) == 0 and len(word) != 0:
            return False
        if len(pattern) != 0 and len(word) == 0:
            return False
        if pattern[0] is '*':
            return self.recurse_filter(pattern, word[1:]) or self.recurse_filter(pattern[1:], word)
        if pattern[0] is '?':
            return self.recurse_filter(pattern[1:], word[1:])
        if pattern[0] == word[0]:
            return self.recurse_filter(pattern[1:], word[1:])
        if pattern[0] != word[0]:
            return False


    # return list of [word, freq] for all words in trie that match pattern
    # pattern is a string, interpreted as explained below
    #   * matches any sequence of zero or more characters
    #   ? matches any single character
    #   otherwise char in pattern char must equal char in word
    def filter(self, pattern):
        word_list = [word for word in self]
        match = []
        for word in word_list:
            if self.recurse_filter(pattern, word[0]):
                match.append(word)
        return match


        # for star: look at each node's children and use find method
        # for ?: substitute in every letter



# handy stand-alone testing setup
if __name__ == '__main__':
    # read in words
    import json  # this import allowed as part of testing...

    with open('resources/words.json') as f:
        words = json.load(f)

    """
    # small corpus: insert words one-by-one
    trie = Trie()
    for w in words[:50]: trie.insert(w)
    """

    # large corpus: precompute count for each word
    trie = Trie()


    # your test here!
    # Example: 5- or more letter words beginning in "a" and  ending in "ing"
    #print(trie.filter('a?*ing'))

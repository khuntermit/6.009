Autocomplete
============

*Submission to website:* Monday, 4/10, 10pm

*Checkoff by LA/TA*: Thursday, 4/13, 10pm

This lab assumes you have Python 3.5 or later installed on your machine.  Please use the Chromium or Firefox web browser.

This lab has 30 tests and 6 coding points.  The coding points will be
assigned during check-off based on the organization and readability of
your code.

Introduction
------------

Type "aren't you" into Google search and you'll get a handful of search suggestions, ranging from "aren't you clever?" to "aren't you a little short for a stormtrooper?". If you've ever done a Google search, you've probably seen an autocompletion - a handy list of words that pops up under your search, guessing at what you were about to type.

Search engines aren't the only place you'll find this mechanism. Powerful code editors, like Eclipse and Visual Studio, use autocomplete to make the process of coding more efficient by offering suggestions for completing long function or variable names.

In this lab, we are going to implement our own version of an autocomplete engine using a tree structure called a "trie," as described in this document. The staff have already found a nice corpus (list of words) for you to use - the full text of Jules Verne's "In the Year 2889." The lab will ask you first to generate the trie data structure using the list of words provided. You will then use the trie to write your own autocomplete and autocorrect, which select the top few words that a user is likely to be typing.  Note that all words in the corpus and any string argument
values in the tests will be in lower case.

The trie data structure
-----------------------

A trie, also known as a  prefix tree, is a type of search tree that stores words organized by their prefixes (their first characters), with longer prefixes given by successive levels of the trie. Each node contains a Boolean (`true`/`false`) value stating whether this node's prefix is a word.

For example, consider the words `'bat'`, `'bar'`, and `'bark'`. A trie over these words would look like the following:

![Simple Trie](markdown_resources/trie1.png)

To list all words beginning with `'ba'`, begin at the root and follow the `'b'` and `'a'` edges to reach the node representing a `'ba'` prefix. This node is itself a trie and contains all words prefixed by `'ba'`. Enumerating all paths leading to `true` nodes (in this case, `'t'`, `'r'`,`'rk'`) produces the list of `'ba'` words: `'bat'`, `'bar'`, and `'bark'`.

Note that we also check the `'ba'` node itself, though in this case the node is `false`, meaning `'ba'` is not known to be a word. Consider the words beginning with the string `'bar'`. Just as before, follow the `'b'`, `'a'`, and `'r'` edges to the `'bar'` node, then enumerate all paths to `true` nodes (`''` and `'k'`) to find the valid words: `'bar'` and `'bark'`.

This trie structure on its own, however, is not very useful. If we
type only a few characters, for example `'b'`, the long list of words
`b` generates is of little help to the user, who is only interested in
the most likely candidates. To this end, we replace the Boolean flag
in each node of our trie with a frequency metric, describing how often each word appears in our corpus. If the frequency of a trie node is 0, the prefix this node is not a word in the corpus. Assume that the more often a word appears in the corpus, the more likely it is to be typed by our user.  When using the trie to enumerate likely words, suggest only a few likely matches instead of the entire list.

Consider the following corpus: `"bat bark bat bar"`. The `example_trie` this corpus would generate is:

![Frequency Trie](markdown_resources/trie2.png)

Assume we are interested in only the top result after autocompleting the string `'ba'`. Now instead of giving us all of `'bat'`, `'bark'`, and `'bar'`, we should just get the highest-frequency word - `'bat'`.

Note that in the tree above, the `'b'` and `'ba'` nodes have frequencies of `0`, meaning they're not valid words.

Trie class and basic methods
-------

In `lab.py`, you are responsible for implementing the `Trie` class, which should support the following methods:

**\_\_init\_\_**( *self* )
<div style="margin-left: 2em;">
Initialize self to be an object with two instance variables:
<ul>
<li> <tt>frequency</tt>, an integer frequency (number of times the word appears in corpus) of the word ending at this node.  Initial value is 0.
</li>
<li><tt>children</tt>, a dictionary mapping single-character strings to another trie node, i.e., the next level of the trie hierarchy (tries are a recursive data structure).  Initial value is an empty dictionary.
</ul>
</div>

**insert**( *self, word, freq*=None )
<span style="margin-left: 2em;"><b>[tests 1-4]</b></span>
<div style="margin-left: 2em;">
Add the given <tt>word</tt> to the trie, modifying the trie by adding child trie nodes as necessary.  For the trie node that marks the end of the word, if <tt>freq</tt> is <tt>None</tt>, increment the node's frequency instance variable, otherwise set it to the specified value.  This method doesn't return a value.
<p/>
Examples (using <tt>example\_trie</tt>):
<p/>
<ul>
<li><tt>t = Trie()</tt> would create the root node of the <tt>example_trie</tt>.</li>

<li><tt>t.insert("bat")</tt> adds the two center nodes, with frequencies of 0, and the node to left of center, with a frequency of 1.</li>

<li><tt>t.insert("bark")</tt> adds the two nodes to the right of center, setting the frequency of the last node to 1.</li>

<li><tt>t.insert("bat")</tt> doesn't add any nodes and only increments the frequency of the node to the left of center.</li>

<li><tt>t.insert("bar")</tt> doesn't add any nodes and only increments the frequency of the node topmost node to right of center.</li>
</ul>
</div>


**find**( *self, prefix* )
<span style="margin-left: 2em;"><b>[tests 5-8]</b></span>
<div style="margin-left: 2em">
Return the trie node for the specified <tt>prefix</tt> or <tt>None</tt> if the prefix cannot be found in the trie.
<p/>
Examples (using <tt>example_trie</tt>):
<p/>
<ul>
<li><tt>t.find("")</tt> returns <tt>t</tt>, the root node.</li>

<li><tt>t.find("ba")</tt> returns the bottommost of the three center nodes, i.e., <tt>t.children["b"].children["a"]</tt>.</li>
</ul>
</div>


**\_\_contains\_\_**( *self, word* )
<span style="margin-left: 2em;"><b>[tests 9-13]</b></span>
<div style="margin-left: 2em">
Return True if <tt>word</tt> occurs with a non-zero frequency in the trie.  This is the special method name used by Python to implement the <tt>in</tt> operator.  For example,

<pre>word in trie</pre>
	
is translated to

<pre>trie.__contains__( word )</pre>

Hint: use <tt>self.find(word)</tt> to do the hard work!
<p/>
Examples (using <tt>example_trie</tt>):
<p/>
<ul>
<li><tt>"ba" in t</tt> returns False since that interior node has a frequency of 0.</li>

<li><tt>"bar" in t</tt> returns True</li>

<li><tt>"barking" in t</tt> return False since "barking" can't be found in trie.</li>
</ul>
</div>


**\_\_iter\_\_**( *self* )
<span style="margin-left: 2em;"><b>[tests 14-15]</b></span>
<div style="margin-left: 2em">
Return an iterator that produces <tt>[word, freq]</tt> pairs for each word stored in the trie.  The pairs can be produced in any order.  This is the special method name used by Python when it needs to iterate over a data object, i.e., the method invoked by the <tt>iter()</tt> built-in function.  For example, the following Python code will print all the words in a trie:

<pre>print(word for word,freq in trie)</pre>

Hint: see the slides for Lecture 8.  You'll want to return a generator function that uses <tt>yield</tt> and <tt>yield from</tt> to produce the required sequence of values one at a time.  See <A href="https://docs.python.org/3/howto/functional.html#generators">https://docs.python.org/3/howto/functional.html#generators</A>.
<p/>
Examples (using <tt>example_trie</tt>):
<p/>
<ul>
<li><tt>list(t)</tt> returns <tt>[['bat', 2], ['bar', 1], ['bark',
1]]</tt>.  Note that the <tt>list</tt> function has an internal
<tt>for</tt> loop that uses <tt>iter(t)</tt> to iterate over each
element of the sequence <tt>t</tt>.</li>

<li><tt>list(t.find("bar"))</tt> returns <tt>[['', 1], ['k', 1]]</tt>.  This may seem a bit weird, but rememeber that we were treating the interior node returned by <tt>t.find("bar")</tt> as the root of its own mini-trie.</li>
</ul>
</div>

Autocomplete method
------------

**autocomplete**( *self, prefix, N* )
<span style="margin-left: 2em;"><b>[tests 16-20]</b></span>
<div style="margin-left: 2em">
<tt>prefix</tt> is a string, <tt>N</tt> is an integer; returns a list of up to <tt>N</tt> words.  Return a list of the <tt>N</tt> most-frequently-occurring words that start with <tt>prefix</tt>.  In the case of a tie, you may output any of the most-frequently-occurring words. If there are fewer than <tt>N</tt> valid words available starting with <tt>prefix</tt>, return only as many as there are.  The returned list may be in any order.
<p/>
Return <tt>[]</tt> if prefix is not in the trie.
<p/>
Hint: <tt>self.find</tt> is useful in finding the trie node at which to start your enumeration.
<p/>
Examples (using <tt>example_trie</tt>):
<p/>
<ul>
<li><tt>t.autocomplete("ba",1)</tt> returns <tt>['bat']</tt>.</li>

<li><tt>t.autocomplete("ba",2)</tt> might return either <tt>['bat', 'bark']</tt> or <tt>['bat', 'bar']</tt> since "bark" and "bar" occur with equal frequency.</li>

<li><tt>t.autocomplete("be",1)</tt> returns <tt>[]</tt>.</li>
</ul>
</div>

Autocorrect method
-----------

You may have noticed that for some words, our autocomplete implementation generates very few or no suggestions. In cases such as these, we may want to guess that the user mistyped something in the original word. We ask you to implement a more sophisticated code-editing tool: autocorrect. 

**autocorrect**( *self, prefix, N* )
<span style="margin-left: 2em;"><b>[tests 21-24]</b></span>
<div style="margin-left: 2em">
<tt>prefix</tt> is a string, <tt>N</tt> is an integer; returns a list of up to <tt>N</tt> words.  <tt>autocorrect</tt> should invoke <tt>autocomplete</tt>, but if fewer than <tt>N</tt> completions are made, suggest additional words by applying one <b>valid edit</b> to the prefix.
<p/>
An <b>edit</b> for a word can be any one of the following:
<p/>
<ul>
<li>A single-character insertion (add any one character in the range a-z> at any place in the word)</li>
<li>A single-character deletion (remove any one character from the word)</li>
<li>A single-character replacement (replace any one character in the word with a character in the range a-z</li>
<li>A two-character transpose (switch the positions of any two adjacent characters in the word)</li>
</ul>

A <b>valid edit</b> is an edit that <b>results in a word in the trie without considering any suffix characters</b>.  In other words we don't try to autocomplete valid edits, we just check if <tt>valid_edit in self</tt> is True.

For example, editing <tt>"te"</tt> to <tt>"the"</tt> is valid, but editing <tt>"te"</tt> to <tt>"tze"</tt> is not, as "tze" isn't a word. Likewise, editing <tt>"phe"</tt> to <tt>"the"</tt> is valid, but <tt>"phe"</tt> to <tt>"pho"</tt> is not because "pho" is not a word in the corpus, although many words beginning with "pho" are.

<p/>
In summary, given a prefix that produces C completions, where C < N, generate up to N-C additional words by considering all valid single edits of that prefix (i.e., corpus words that can be generated by 1 edit of the original prefix), and selecting the most-frequently-occurring edited words. Return a list of suggestions produced by including <b>all</b> C of the completions and up to N-C of the most-frequently-occuring valid edits of the prefix; the list may be in any order. Be careful not to repeat suggested words!
<p/>
Example (using <tt>example_trie</tt>):
<p/>
<ul>
<li><tt>t.autocorrect("bar",3)</tt> returns <tt>['bar', 'bark', 'bat']</tt> since "bar" and "bark" are found by autocomplete and "bat" is valid edit involving a single-character replacement, i.e., "t" is replacing the "r" in "bar".</li>
</ul>
</div>

Selecting words from a trie
---------------------------

It's sometimes useful to select only the words from a trie that match a pattern.  That's the purpose of the `filter` method.

**filter**( *self, pattern* )
<span style="margin-left: 2em;"><b>[tests 25-30]</b></span>
<div style="margin-left:2em;">
<tt>pattern</tt> is a string.  Return a list of <tt>[word, freq]</tt> pairs for those words whose characters match those of <tt>pattern</tt>.  The characters in <tt>pattern</tt> are matched one at a time with the characters in each word stored in the trie.  If all the characters in a particular word are matched, the <tt>[word, freq]</tt> pair should be included in the list to be returned.
<p/>
The characters in <tt>pattern</tt> are interpreted as follows:
<p/>
<ul>
<li><tt>'*'</tt> matches a sequence of <b>zero or more</b> of the next unmatched characters in <tt>word</tt>. </li>

<li><tt>'?'</tt> matches the next unmatched character in <tt>word</tt> no matter what it is.  There must be a next unmatched character for <tt>'?'</tt> to match.</li>

<li>otherwise the character in the pattern must exactly match the next unmatched character in the word.</li>
</ul>

Pattern examples:
<p/>
<ul>
<li><tt>"\*a\*t"</tt> matches all words that contain an "a" and end in "t".  This would include words like "at", "art", "saint", and "what".</li>
<li><tt>"year\*"</tt> would match both "year" and "years"</li>
<li><tt>"\*ing"</tt> matches all words ending in "ing"</li>
<li><tt>"???"</tt> would match all 3-letter words</li>
<li><tt>"?ing"</tt> matches all 4-letter words ending in "ing"</li>
<li><tt>"?\*ing"</tt> matches all words with 4 or more letters that end in "ing"</li>
</ul>
<p/>
Filter examples (using <tt>example_trie</tt>):
<p/>
<ul>
<li><tt>t.filter("*")</tt> returns <tt>[['bat', 2], ['bar', 1], ['bark', 1]]</tt>, i.e., listing all the words in the trie.</li>

<li><tt>t.filter("???")</tt> returns <tt>[['bat', 2], ['bar', 1]]</tt>, i.e., listing all the 3-letter words in the trie.</li>

<li><tt>t.filter("\*r\*")</tt> returns <tt>[['bar', 1], ['bark', 1]]</tt>, i.e., listing all the words containing an "r" in any position.</li>
</ul>
</div>

Hint: the matching operation can implemented as a recursive search function that attempts to match the next character in the pattern with some number of characters at the beginning of the word, then recursively matches the remaining characters in the pattern with remaining unmatched characters in the word.

Note: you **cannot** use any of the built-in Python pattern-matching
functions, e.g., functions from the `regex` module -- you are expected to write your own pattern matching code.  Copying code directly from stackoverflow is also not appropriate.


Testing your lab
-----------------------------

We've included a 6.009-autocomplete-powered search bar so you can see your code in action. Run `server.py` and open your browser to [localhost:8000](http://localhost:8000) and type into the search bar to see the top 5 results from your `autocomplete` and `autocorrect` function, using the corpus of words from 
[Jules Verne's "In the Year 2889."](http://www.gutenberg.org/files/19362/19362-h/19362-h.htm)

In the search box, try typing "when", checking after each letter to see the suggested words:

* "w" suggests "was", "with", "which", "will", "we"
* "wh" suggests "which", "what", "when", "why", "who"
* "whe" suggests "when", "where", "whether", "whenever", "whence"
* "when" suggests "when", "whenever", "whence"

In the autocorrection box, try typing "thet" then Ctrl+Space to see a list of suggested corrections: "the", "that", "they", "then", and "them".

As in the previous labs, we provide you with a `test.py` script to help you verify the correctness of your code. 

Does your lab work? Do all tests in `test.py` pass? You're done! Submit your `lab.py` on web.mit.edu/6.009 and get your lab checked off by a friendly staff member. 

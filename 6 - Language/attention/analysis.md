# Analysis

## Layer 4, Head 10

This head appears to capture phrase structure relationships, especially between determiners and the nouns they modify.  
In sentences such as “The [MASK] cat sat on the keyboard,” the token “the” pays strong attention to “[MASK]” and “cat,” suggesting awareness of noun phrase boundaries.  
There is also some attention from prepositions like “on” to the nouns they introduce, hinting that the model recognizes simple phrase structure.

Example Sentences:
- The [MASK] cat sat on the keyboard.
- She put the [MASK] book on the shelf.

## Layer 2, Head 7

This head appears to act as a mask-position detector, where most tokens attend strongly to the `[MASK]` token.  
In the sentence “He did [MASK] like broccoli.” almost all words direct their attention toward `[MASK]`, forming a clear vertical stripe in the visualization.  
This indicates that the model uses this head to recognize the position of the missing word and propagate that information across the sentence for later contextual understanding.

Example Sentences:
- He did [MASK] like broccoli.
- We turned down a narrow lane and passed through a small [MASK].


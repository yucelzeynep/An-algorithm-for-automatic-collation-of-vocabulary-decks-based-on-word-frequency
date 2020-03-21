# RBSC
Rank biserial correlation and generating a pair of decks with desired relative difficulty relation

**rbsc_simple.py**

This function implements rank biserial correlation (RBSC) based on the definition of *Simple difference formula* of KERBY [1]. 
According to Kerby's approach, the nonparametric correlation equals the simple difference between the proportion of “favorable” and “unfavorable” evidence, where favorable stands for the pairs supporting the hypothesis and unfavorable for the ones disagreeing with the hypothesis. 

Here, we provide a sample implementation of RBSC between two sets of words listed in files deck_A.txt and deck_B.txt. For this specific example, we compiled two sets of words composed of abstract English vocabulary. Each file involves two columns, where the first column contains the vocabulary, and the second column is the number of occurences of those vocabulary in the Wiktionary word frequency lists [2]. Namely, the ranking of the words is obtaned according to this last column. 

Let our hypothesis be that 'The vocabulary in deck_A are used more frequently than the vocabulary in deck_B'. In this case, the frequency values listed in the second column of deck_A are expected to be higher than those in deck_B. To compute the RBSC coefficient, we compare each pair of numbers in those columns and compute the number of evidence supporting the hypothesis S, and the number of evidence contradicting with the hypothesis, C. In explicit terms, RBSC coefficient is computed simply as,
rho = (S-C)/(S+C).

Obviously, RBSC values are bounded in the range -1 to 1. If the data are all favorable, then the correlation is exactly 1. On the contrary, if the data are all unfavorable, correlation will be -1, whereas a correlation of 0 indicates equal amount of
favorable and unfavorable evidence.

For our specific example, RBSC coefficient is found as rho = 0.707, which suggests that the vocabulary in deck_A is in general used more frequently than the vocabulary in deck_B, i.e. the hypothesis is likely to be true. 

**generate_deck_pair.py**

This program builds 2 decks of flash-cards with a desired difficulty relation.

For this example, we consider the cards to involve a country on the front side and its capital on the back. We consider the -a priori- familiarity of the users to the capital to be in direct relation with the difficulty of concerning card.

This familiarity is considered to be proportional to the exposure of the users to the capitals in the news. Since our pool of subjects is entirely Japanese,we rank the cards with respect to the number of Japanese Google news search results. Please see [3] for achieving number of search results in Python. 

We organize the input file such that it includes the following columns, 
col1: country in katakana 
col2: capital in katakana 
col3: country in English 
col4: capital in English 
col5: number of search results for country 
col6: number of search results for capital

So as to achieve a desired level of relative difficulty, we adopt an approach based on RBSC as explained above. 

For further details on the algorithm, please refer to [4].

**References**

[1] D.S. Kerby, “The simple difference formula: An approach to teaching nonparametric correlation,” Comprehensive Psychology, vol.3, pp.11–IT, 2014.

[2] Wiktionary, “Frequency lists.” https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/TV/2006/explanation
2020. [Accessed 2020-03-15].

[3] https://github.com/anthonyhseb/googlesearch

[4] Zeynep Yücel, Parisa Supitayakul, Akito Monden, Pattara Leelaprute, "An algorithm for automatic collation of vocabulary decks based on word frequency", IEICE Transactions on Information and Systems, 2020 (in press)


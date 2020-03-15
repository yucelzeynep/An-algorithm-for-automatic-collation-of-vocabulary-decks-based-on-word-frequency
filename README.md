# RBSC
Rank biserial correlation

This function implements rank biserial correlation (RBSC) based on the definition of *Simple difference formula* of KERBY [1]. 
According to this approach, the nonparametric correlation equals the simple difference between the proportion of “favorable” and “unfavorable” evidence, where favorable stands for the pairs supporting the hypothesis and unfavorable for the ones disagreeing with the hypothesis. In explicit terms, RBSC coefficient is computed simply as,

<img src="https://render.githubusercontent.com/render/math?math=RBSC = \frac{S-C}{S+C}">

RBSC values are bounded in the range -1 to 1. If the data are all favorable, then the correlation is exactly 1. On the contrary, if the data are all unfavorable, correlation will be -1, whereas a correlation of 0 indicates equal amount of
favorable and unfavorable evidence.


As an example, we consider the RBSC relation between two sets of words given by files deck_A.txt and deck_B.txt. For this spedific example, we compiled two sets of words composed of abstract English vocabulary. Each file involves three clumns, where the first column contains the word in English, the second column is the tranlation of the word in Japanse, and the last column is the number of occurences of the word in the Wiktionary word frequency lists[2]. Namely, the ranking of the words is obtaned according to this last column. 

The number of favorable and unvarable 

**References**
[1] D.S. Kerby, “The simple difference formula: An approach to teaching nonparametric correlation,” Comprehensive Psychology, vol.3, pp.11–IT, 2014.
[2] Wiktionary, “Frequency lists.” https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/TV/2006/explanation
2020. [Accessed 2020-03-15].

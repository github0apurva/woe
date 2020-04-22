# woe

This is method to calculate woe and IV of both continuous & Discrete variables.
It also calculates the Chi2 value ( Stats, P & dof). 
The buckets for discrete is the unique values; while for continuous it is the buckets created for WOE calculation. 
It assumes missing as separate bucket and will throw an error if y has more than 2 class or even missing.

The output is in the form of 2 DataFrame or 1 DataFrame & 1 Dictionary, based on the number of xs passed.

For single X: 
1st DataFrame:
	Basic Info (number of buckets)
	IV (total IV of the variable; infinity is considered nan)
	Chi2 (Chi2 value, P value, degrees if freedom)
2nd DataFrame:
	Basic Info (bucket name, lower cut off of bucket (in case of continuous frequency distribution across buckets & y)
	Woe (bucket wise woe; infinite is converted to nan for convenience
	IV (bucket wise iv calculated with total for the variables)

For more than 1 X: 
DataFrame: 
	same as 1st DataFrame of single X. (Rows introduced for handling multi variables)
Dictionary: 
	key being -> variable name  
	& value being -> the corresponding 2nd DataFrame for the key


-------------------------------------------------------------------------------------------------------------------
The method can be found as woe_chi.py
-------------------------------------------------------------------------------------------------------------------
The sample usage of this code can be found in woe_test.py
-------------------------------------------------------------------------------------------------------------------

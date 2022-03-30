# Write a program (using functions!) that asks the user for a long string containing multiple words. Print back to the user the same string, except with the words in backwards order. For example, say I type the string:

#   My name is Michele
# Then I would see the string:

#   Michele is name My
# shown back to me.

sentence = input("Sentence: ")

words = sentence.split(" ")
for x in range(len(words)):
    print(words[-x-1] + (", " if x != len(words)-1 else "") ,end="")
# print()
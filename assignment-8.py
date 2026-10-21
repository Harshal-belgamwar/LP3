
from functools import reduce
from collections import defaultdict

# Given dataset
dataset = [
    "Hello World",
    "MapReduce Programming",
    "Big Data 123!",
    "HELLO python"
]

# MAP: Convert each alphabetic character to lowercase
# and emit (character, 1)
def map_function(text):
    result = []

    for char in text:
        if char.isalpha():
            result.append((char.lower(), 1))

    return result


# Apply Map to all records
mapped_data = []

for record in dataset:
    mapped_data.extend(map_function(record))

# SHUFFLE AND SORT: Group values by character
grouped_data = defaultdict(list)

for char, count in mapped_data:
    grouped_data[char].append(count)


# REDUCE: Sum counts for each character
def reduce_function(counts):
    return reduce(lambda x, y: x + y, counts, 0)


final_counts = {
    char: reduce_function(counts)
    for char, counts in grouped_data.items()
}

# Display results alphabetically
print("Character Occurrences:")
for char in sorted(final_counts):
    print(f"{char}: {final_counts[char]}")

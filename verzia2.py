from collections import OrderedDict


def load_dictionary_from_file(file_path):
    compound_dictionary = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 2:
                frequency, word = parts
                compound_dictionary[word] = int(frequency)
    return compound_dictionary


def filter_words_by_frequency(word_frequencies, threshold):
    return OrderedDict((word, freq) for word, freq in word_frequencies.items() if freq > threshold)


def compute_probability_distributions(word_frequencies, included_words, total_frequency):
    num_words = len(included_words)
    probabilities = [word_frequencies[word] / total_frequency for word in included_words]
    dummy_probabilities = [0] * (num_words + 1)

    for i in range(num_words + 1):
        frequency_sum = 0
        for word, freq in word_frequencies.items():
            if word in included_words:
                continue

            if i == 0:
                if word < included_words[0]:
                    frequency_sum += freq
            elif i == num_words:
                if word > included_words[-1]:
                    frequency_sum += freq
            else:
                if included_words[i - 1] < word < included_words[i]:
                    frequency_sum += freq

        dummy_probabilities[i] = frequency_sum / total_frequency

    return probabilities, dummy_probabilities


def initialize_matrices(size, dummy_probabilities):
    cost_matrix = [[0] * (size + 1) for _ in range(size + 1)]
    weight_matrix = [[0] * (size + 1) for _ in range(size + 1)]
    root_matrix = [[0] * (size + 1) for _ in range(size + 1)]

    for i in range(size + 1):
        cost_matrix[i][i] = dummy_probabilities[i]
        weight_matrix[i][i] = dummy_probabilities[i]

    return cost_matrix, weight_matrix, root_matrix


def construct_optimal_bst(keys, probabilities, dummy_probabilities):
    n = len(keys)
    cost_matrix, weight_matrix, root_matrix = initialize_matrices(n, dummy_probabilities)

    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length
            cost_matrix[i][j] = float('inf')
            weight_matrix[i][j] = weight_matrix[i][j - 1] + probabilities[j - 1] + dummy_probabilities[j]

            for r in range(i, j):
                temp_cost = cost_matrix[i][r] + cost_matrix[r + 1][j] + weight_matrix[i][j]
                if temp_cost < cost_matrix[i][j]:
                    cost_matrix[i][j] = temp_cost
                    root_matrix[i][j] = r

    return cost_matrix, root_matrix


def construct_optimal_binary_search_tree(word_frequencies, frequency_threshold):
    total_frequency = sum(word_frequencies.values())
    print(f"Celkova frekvencia slov suma: {total_frequency}")

    sorted_key_frequencies = OrderedDict(sorted(word_frequencies.items()))
    filtered_words = filter_words_by_frequency(sorted_key_frequencies, frequency_threshold)

    filtered_frequency_sum = sum(filtered_words.values())
    print(f"Suma frekvencie klucov: {filtered_frequency_sum}")
    print(f"Pocet klucov: {len(filtered_words)}")

    if not filtered_words:
        print("No words meet the frequency threshold.")
        return None, None, None

    keys = list(filtered_words.keys())
    probabilities, dummy_probabilities = compute_probability_distributions(sorted_key_frequencies, keys, total_frequency)
    print(f"Keys: {keys}")
    print(f"Key probabilities: {probabilities}")
    print(f"Dummy probabilities: {dummy_probabilities}")

    cost_matrix, root_matrix = construct_optimal_bst(keys, probabilities, dummy_probabilities)
    print(f"Optimalna cena hladania: {cost_matrix[0][len(keys)]}")
    #print("Cost Matrix:")
    # for row in cost_matrix:
    #     print(row)
    # print("Root Matrix:")
    # for row in root_matrix:
    #     print(row)

    return keys, probabilities, root_matrix


def merge_dictionaries(dictionary1, dictionary2):
    merged_dict = dictionary1.copy()
    for word, count in dictionary2.items():
        merged_dict[word] = merged_dict.get(word, 0) + count
    return merged_dict


def build_tree_structure(root_table, keys, probabilities, i, j):
    if i >= j:
        return None

    r = root_table[i][j]
    left_subtree = build_tree_structure(root_table, keys, probabilities, i, r)
    right_subtree = build_tree_structure(root_table, keys, probabilities, r + 1, j)

    return (keys[r], probabilities[r], left_subtree, right_subtree)

def search_optimal_bst(words, root_table, target):
    path = []
    comparisons = 0
    i, j = 0, len(words)

    while i < j:
        r = root_table[i][j]
        if r >= len(words):
            break

        word = words[r]
        path.append(word)
        comparisons += 1

        if word == target:
            return path, comparisons
        elif target < word:
            j = r
        else:
            i = r + 1

    print(f"Slovo '{target}' nebolo najdene v strome.")
    return path, comparisons


def main():
    dictionary1 = load_dictionary_from_file("dictionary1.txt")
    dictionary2 = load_dictionary_from_file("dictionary2.txt")

    merged_dictionary = merge_dictionaries(dictionary1, dictionary2)

    frequency_threshold = 40000

    keys, probabilities, root_table = construct_optimal_binary_search_tree(merged_dictionary, frequency_threshold)

    if keys:
        tree_structure = build_tree_structure(root_table, keys, probabilities, 0, len(keys))
        #print("Optimal BST structure:", tree_structure)

    search_word = "back"
    if keys:
        path, comparisons = search_optimal_bst(keys, root_table, search_word)
        print(f"Cesta k '{search_word}': {path}")
        print(f"Pocet porovnani: {comparisons}")


if __name__ == "__main__":
    main()

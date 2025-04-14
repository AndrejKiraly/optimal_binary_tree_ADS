from traceback import print_tb


def load_dictionary(path):
    word_freq = {}
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        freq, word = line.split(' ', 1)
                        word_freq[word] = int(freq)
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Error: The file {path} was not found.")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

    return word_freq


def remove_words_under_frequency(dictionary, frequency_threshold):
    filtered_dict = {}
    for word, freq in dictionary.items():
        if freq >= frequency_threshold:
            filtered_dict[word] = freq
    return filtered_dict


def calculate_dictionary_total_word_frequency(dictionary):
    return sum(dictionary.values())


def probabilities(keyDictionary1, dictionaries):
    total_frequency = calculate_dictionary_total_word_frequency(dictionaries)
    sorted_words = sorted(keyDictionary1.keys())


    p_values = {word: freq / total_frequency for word, freq in keyDictionary1.items()}
    q_values = {}

    q_frequency = 0

    for word in sorted_words:
        freq = dictionaries[word]
        q_frequency += freq
        q_values[word] = q_frequency / total_frequency

    return p_values, q_values


def merge_dictionaries(dictionary1, dictionary2):
    merged_dict = dictionary1.copy()
    for word, count in dictionary2.items():
        merged_dict[word] = merged_dict.get(word, 0) + count
    return merged_dict

def calculate_average_search_cost(tree, keys, p, depth=1):
    """Calculates the expected search cost in an optimal BST."""
    if tree is None:
        return 0  # No contribution from an empty subtree

    # Find the index of the key in the keys list
    try:
        index = keys.index(tree.key)
        key_prob = p[index]  # Get probability from p list
    except ValueError:
        key_prob = 0  # Key not found (shouldn't happen in valid OBST)

    # Compute cost for current node and recurse for left and right subtrees
    cost = key_prob * depth
    cost += calculate_average_search_cost(tree.left, keys, p, depth + 1)
    cost += calculate_average_search_cost(tree.right, keys, p, depth + 1)

    return cost

def print_dictionary_info(merged_dictionary, keyDict):
    print(f"Pocet slov slovnika: {len(merged_dictionary)}")
    print(f"Celkova frekvenia suma: {sum(merged_dictionary.values())}")
    print(f"Pocet slov slovnika s fr nad 40 000: {len(keyDict)}")


def build_optimal_bst(words, p_values, q_values):
    n = len(words)
    if n == 0:
        print("Error: Prazdny slovnik")
        return [], [], 0

    cost = [[0] * n for _ in range(n)]
    root = [[0] * n for _ in range(n)]

    for i in range(n):
        cost[i][i] = p_values[words[i]]
        root[i][i] = i

    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            cost[i][j] = float('inf')
            total_prob = q_values[words[j]] - (q_values[words[i-1]] if i > 0 else 0)

            for r in range(i, j + 1):
                left_cost = cost[i][r - 1] if r > i else 0
                right_cost = cost[r + 1][j] if r < j else 0
                total_cost = left_cost + right_cost + total_prob

                if total_cost < cost[i][j]:
                    cost[i][j] = total_cost
                    root[i][j] = r

    optimal_cost = cost[0][n - 1]

    return root, cost, optimal_cost


def search_optimal_bst(words, root, target):
    path = []
    comparisons = 0
    i, j = 0, len(words) - 1

    while i <= j:
        r = root[i][j]
        path.append(words[r])
        comparisons += 1

        if words[r] == target:
            return path, comparisons
        elif target < words[r]:
            j = r - 1
        else:
            i = r + 1

    print(f"Slovo '{target}' nebolo najdene v strome.")
    return path, comparisons


def main():
    threshold = 40000
    dictionary1 = load_dictionary("dictionary1.txt")
    dictionary2 = load_dictionary("dictionary2.txt")
    merged_dictionary = merge_dictionaries(dictionary1, dictionary2)
    keyDictionary1 = remove_words_under_frequency(merged_dictionary, threshold)
    keyDictionary1 = dict(sorted(keyDictionary1.items()))
    p_values, q_values = probabilities(keyDictionary1, merged_dictionary)
    print_dictionary_info(merged_dictionary, keyDictionary1)

    total_frequency = calculate_dictionary_total_word_frequency(merged_dictionary)
    print("Celková frekvenia pre merged slovnik:", total_frequency)
    total_frequency2 = calculate_dictionary_total_word_frequency(keyDictionary1)
    print("Celková frekvenia pre slovnik s klucmi:", total_frequency2)
    # print("Pravdepodobnosti p_i:", p_values)
    print("Pravdepodobnosti q_i:", q_values)

    words = list(keyDictionary1.keys())
    root, cost, optimal_cost = build_optimal_bst(words, p_values, q_values)
    # print("Optimal BST root table:", root)
    print("Optimal BST cost table:", cost[0][len(keyDictionary1) - 1])
    print("Optimal BST cost:", optimal_cost)
    #print(calculate_average_search_cost(root, words, 0, len(words)-1))

    search_word = "said"
    if len(words) > 0:
        path, comparisons = search_optimal_bst(words, root, search_word)
        print(f"Cesta vyhľadávania '{search_word}':", path)
        print(f"Počet porovnaní: {comparisons}")


main()

import time
import collections
from math import log

start_time = time.clock()

classes = []

with open("WordEmbedding.txt") as words:
    objects = words.read().split()
    objects = [objects[i: i + 2] for i in range(0, len(objects), 2)]

words = []
word_distance = []
for i in objects:
    i[1] = list(map(float, i[1].split(",")))
    words.append(i[0])
    word_distance.append(i[1])

threshold = 0.6
cluster_similarity = "cosine"
print(cluster_similarity, "similarity with threshold", str(threshold))


def get_similarity_matrix(classes):
    matrix = []
    # item_set = []
    for i in classes:
        tmp = []
        # item_set.append(i[0])
        for j in classes:
            if classes.index(i) < classes.index(j):
                continue
            tmp.append(get_similarity(i, j))
        matrix.append(tmp)
    return matrix

def get_similarity(item_set_x, item_set_y):
    similarity_list = []
    if item_set_x == item_set_y:
        #return 0
        return 1

    for i in item_set_x:
        for j in item_set_y:
            # educlidean distance
            #similarity_list.append(sum(list((i[1][index]-j[1][index])**2 for index in range(len(i[1]))))**0.5)
            # cosine similarity
            similarity_list.append(sum(list((i[1][index] * j[1][index]) for index in range(len(i[1])))) / (
            (sum(list((i[1][indexi]) ** 2 for indexi in range(len(i[1])))) ** 0.5) * (
            sum(list((j[1][indexj]) ** 2 for indexj in range(len(j[1])))) ** 0.5)))

    if len(similarity_list) == 0:
        #return 0
        return 1
    else:
        #return max(similarity_list) #euclidean
        return min(similarity_list) #cosine

def get_max_similarity(matrix, classes):
    #min = 5000 #euclidean
    min = -1 #cosine
    row = None
    col = None
    for i in matrix:
        for j in i:
            #if j < min and j != 0: #euclidean
            if j > min and j != 1: #cosine
                min = j
                row = matrix.index(i)
                col = i.index(j)
    return classes[row], classes[col], row, col

def get_cluster_number(word, cluster):
    for i in cluster:
        if word in i:
            return cluster.index(i)

def print_matrix(matrix):
    for i in matrix:
        for j in i:
            print(j, end=" ")
        print()

def delete_row(matrix, row, col):
    matrix.pop(row)
    matrix.pop(col)

def delete_col(matrix, row, col):
    for i in matrix:
        if len(i) > row:
            i.pop(row)
        if len(i) > col:
            i.pop(col)

def append_new_class(matrix, new_class, classes):
    new_class_similarity = []
    for i in classes:
        #new_class_similarity.append((get_similarity(new_class, i)-min_val)/max_val) #euclidean
        new_class_similarity.append((get_similarity(new_class, i))) #cosine
    matrix.append(new_class_similarity)

def list_to_set(list_content):
    set_content = set()
    for i in list_content:
        set_content.add(i[0])
    return set_content

def get_entropy(result, topic_list):
    class_dict = {}
    for i in topic_list.keys():
        class_dict[i] = []

    for i in result:
        for topic, value in topic_list.items():
            for k in value:
                if i == k:
                    class_dict[topic].append(i)

    total = 0
    for i in class_dict.values():
        total += len(i)

    entropy = 0
    for i in class_dict.values():
        if len(i) == 0:
            continue
        entropy -= (len(i) / total) * log((len(i) / total), 2)

    return entropy

def get_silhouette(result, others, words, word_distance):
    a = []
    b = []
    s = []
    for i in result:
        if len(result) > 1:
            a.append(sum([get_distance(i, j, words, word_distance) for j in result if j != i]) / (len(result) - 1))
        else:
            a.append(0)
        if len(others) > 0:
            b.append(
                min([sum([get_distance(i, j, words, word_distance) for j in k if j != i]) / len(k) for k in others]))
        else:
            b.append(0)
        if max(a[-1], b[-1]) != 0:
            s.append((b[-1] - a[-1]) / max(a[-1], b[-1]))
        else:
            s.append(0)
    return sum(s) / len(s)

def get_distance(item_x, item_y, words, word_distance):
    return sum(list(
        (word_distance[words.index(item_x)][index] - word_distance[words.index(item_y)][index]) ** 2 for index in
        range(len(word_distance[words.index(item_x)])))) ** 0.5

for i in objects:
    tmp = []
    tmp.append(i)
    classes.append(tmp)

similarity_matrix = get_similarity_matrix(classes)

max_val = 0
min_val = 5000
for i in similarity_matrix:
    if max(i) > max_val:
        max_val = max(i)
    if min(i) < min_val:
        min_val = min(i)

for row in range(len(similarity_matrix)):
    for col in range(len(similarity_matrix[row])):
        #similarity_matrix[row][col] = (similarity_matrix[row][col] - min_val)/ max_val #euclidean
        similarity_matrix[row][col] = similarity_matrix[row][col] #cosine

similarity_dict = {}
while len(classes) > 1:
    item_set_x, item_set_y, row, col = get_max_similarity(similarity_matrix, classes)
    classes.remove(item_set_y)
    classes.remove(item_set_x)
    classes.append(item_set_x + item_set_y)
    if similarity_matrix[row][col] in similarity_dict.keys():
        similarity_dict[similarity_matrix[row][col]].append([item_set_x + item_set_y])
    else:
        similarity_dict[similarity_matrix[row][col]] = [item_set_x + item_set_y]
    delete_row(similarity_matrix, row, col)
    delete_col(similarity_matrix, row, col)
    append_new_class(similarity_matrix, list(item_set_x + item_set_y), classes)

print("calculation complete time", time.clock() - start_time)

#similarity_dict = collections.OrderedDict(sorted(similarity_dict.items(), reverse=True))
similarity_dict = collections.OrderedDict(sorted(similarity_dict.items()))

clustered_result = []
for i in similarity_dict.keys():
    #if i <= threshold : #euclidean
    if i >= threshold: #cosine
        for j in similarity_dict[i]:
            duplicated = False
            for k in clustered_result:
                new_set = list_to_set(j)
                if new_set.issubset(k):
                    duplicated = True
                    break
            if duplicated == False:
                clustered_result.append(list_to_set(j))

for i in words:
    exist = False
    for j in clustered_result:
        if i in j:
            exist = True
    if exist == False:
        clustered_result.append([i])

total_word = 0
for i in clustered_result:
    total_word += len(i)
print("total word :", total_word)
print("total cluster :", len(clustered_result))
print("clustering complete time", time.clock() - start_time)

with open("WordClustering.txt", "w") as output:
    for i in range(len(words)):
        output.write("{}\n{}\n{}\n".format(words[i], str(word_distance[i])[1:-1], get_cluster_number(words[i], clustered_result)))

with open("WordTopic.txt") as result:
    topic = result.read().splitlines()
    topic_list = {}
    for i in topic:
        if len(i) == 0:
            continue
        if i[0] == '[':
            topic_list[i[1:-1]] = []
            continue
        topic_list[list(topic_list.keys())[-1]].append(i)

start_time = time.clock()
entropy_list = []
total = 0
for i in clustered_result:
    total += len(i)
    entropy_list.append(get_entropy(i, topic_list) * len(i))

for i in range(len(entropy_list)):
    entropy_list[i] = entropy_list[i] / total

new_entropy = sum(entropy_list)
print("entropy calculation time", time.clock()-start_time, " calculated entropy", new_entropy)

start_time = time.clock()
silhouette_list = []
total = 0
for i in clustered_result:
    total += len(i)
    silhouette_list.append(get_silhouette(i, clustered_result[0:clustered_result.index(i)] + clustered_result[clustered_result.index(i) + 1:-1], words, word_distance) * len(i))

for i in range(len(silhouette_list)):
    silhouette_list[i] = silhouette_list[i] / total

if len(silhouette_list) > 0:
    new_silhouette = sum(silhouette_list) / len(silhouette_list)
else:
    new_silhouette = -1

print("shihouette calculation time", time.clock()-start_time, " calculated shihouette", new_silhouette)

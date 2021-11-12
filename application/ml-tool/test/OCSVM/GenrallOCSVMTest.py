import itertools
import string
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler

x_group_one = []
x_group_two = []

data_split = (50, 20)

for i in range(100):
    rand_vec = np.concatenate((
        np.random.choice(list(string.ascii_uppercase), size = data_split[0]),
        np.random.choice(list(string.ascii_lowercase), size = data_split[1])
    ))
    np.random.shuffle(rand_vec)
    x_group_one.append(rand_vec)

for i in range(10):
    rand_vec = np.concatenate((
        np.random.choice(list(string.ascii_lowercase), size = data_split[0]),
        np.random.choice(list(string.ascii_uppercase), size = data_split[1])
    ))
    np.random.shuffle(rand_vec)
    x_group_two.append(rand_vec)

y_group_one = np.ones(len(x_group_one), dtype = np.int32)
y_group_two = np.zeros(len(x_group_two), dtype = np.int32) - 1

x_data = np.concatenate((x_group_one, x_group_two), axis = 0)
y_data = np.concatenate((y_group_one, y_group_two), axis = 0)

vocab = np.unique(x_data)

test_matrix = []
for vec in x_data:
    test_matrix.append(
        np.where(vec.reshape(vec.size, 1) == vocab)[1]
    )

x_data_converted = np.asarray(test_matrix)

p = np.random.permutation(len(x_data_converted))

x_data_converted = x_data_converted[p]
y_data = y_data[p]

X_train = x_data_converted[:100]
X_test = x_data_converted[100:]
y_train = y_data[:100]
y_test = y_data[100:]

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

print(y_test)


def count_occurrence(element, comp_vec):
    return np.count_nonzero(comp_vec == element)


occurrence_vectorized = np.vectorize(count_occurrence, excluded = ['comp_vec'])

def precompute(X: np.ndarray, Y: np.ndarray, fit = False):
    gram_matrix = np.ndarray((X.shape[0], Y.shape[0]))

    # print(f'X.shape {X.shape} Y.shape {Y.shape}')
    if fit:
        for i, j in itertools.combinations_with_replacement(range(X.shape[0]), 2):
            matching = occurrence_vectorized(X[i], comp_vec = Y[j]).sum()

            gram_matrix[i, j] = matching
            gram_matrix[j, i] = matching

        return gram_matrix
    else:
        for i, j in itertools.product(range(X.shape[0]), range(Y.shape[0])):
            gram_matrix[i, j] = occurrence_vectorized(X[i], comp_vec = Y[j]).sum()

        return gram_matrix


clf_name = 'OneClassSVM'
clf = OneClassSVM(kernel='precomputed', gamma='scale')

scaler = StandardScaler()

gram_matrix = precompute(X_train, X_train, fit = True)
scaler.fit(gram_matrix)
gram_matrix = scaler.transform(gram_matrix)
clf.fit(gram_matrix)

test_gram_mat = precompute(X_test, X_train)
test_gram_mat = scaler.transform(test_gram_mat)
y_pred = clf.predict(test_gram_mat)
dec_boundary_mat = np.tile(np.linspace(np.min(gram_matrix), np.max(gram_matrix), 100).reshape(-1, 1), reps=len(X_train))
dec_boundary_pred = clf.predict(dec_boundary_mat)


train_dec = clf.decision_function(gram_matrix)
test_dec = clf.decision_function(test_gram_mat)
dec_boundary = clf.decision_function(dec_boundary_mat)

print(y_pred)
print('accuracy score: %0.3f' % accuracy_score(y_test, y_pred))

fig = plt.figure()

gs = fig.add_gridspec(2,2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])

ax1.bar(range(len(train_dec)), train_dec, color=['blue' if sign == -1 else 'red' for sign in y_train])
barchart = ax2.bar(range(len(test_dec)), test_dec, color=['blue' if sign == -1 else 'red' for sign in y_test])
max_height = max(map(lambda x: x.get_height(), barchart))
for rect, value in zip(barchart, y_pred):
    ax2.text(rect.get_x() + rect.get_width() / 2., 1.05 * max_height, '%d' % int(value), ha = 'center', va = 'bottom')

ax3.bar(range(len(dec_boundary)), dec_boundary, color=['blue' if sign == -1 else 'red' for sign in dec_boundary_pred])
plt.show()





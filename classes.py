from typing import Iterable
from typing import List
import re
from math import log


class NotFittedError(Exception):
    pass


class CountVectorizer:

    def __init__(self):
        self.feature_names = []
        self.was_fitted = False

    def fit_transform(self, corpus: Iterable[str]) -> list[list[int]]:
        """Обучает векторизатор на корпусе текстов и
        возвращает матрицу векторов счетчиков.

        Args:
            corpus (Iterable[str]): Корпус текстов для обучения.

        Returns:
            list[list[int]]: Матрица, где каждая строка представляет собой
            вектор счетчиков слов из корпуса.
        """
        self.was_fitted = True
        self.feature_names = []
        feature_names_set = set()
        answer = []
        punctuation = r'[!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~ ]'
        for text in corpus:
            for word in re.split(punctuation, text):
                if word:
                    feature_names_set.add(word.lower())
        self.feature_names = sorted(feature_names_set)
        for text in corpus:
            count = dict((word, 0) for word in self.feature_names)
            for word in re.split(punctuation, text):
                if word:
                    count[word.lower()] += 1
            answer.append([i for word, i in count.items()])
        return answer

    def get_feature_names(self) -> List[str]:
        """Возвращает список уникальных слов,
        использованных при обучении векторизатора.

        Returns: list[str]: Список уникальных слов.
        """
        assert self.was_fitted, 'Сначала fit_transform.'
        return list(self.feature_names)

    def tf_transform(self, count_matrix) -> List[List[float]]:
        """Делает массив с term frequency для каждой строки в count_matrix"""
        return [[round(num / sum(row), 3) for num in row] for row in
                count_matrix]

    def idf_transform(self, count_matrix) -> List[float]:
        """Делает массив с inverse document-frequency
        для count_matrix"""
        length_of_row = len(count_matrix[0])
        length_of_matrix = len(count_matrix)
        almost_idf = [sum([1 if row[i] else 0 for row in count_matrix]) for i
                      in range(length_of_row)]
        idf = [round(log((length_of_matrix + 1) / (num + 1)) + 1, 3) for num
               in almost_idf]
        return idf


class TfidfTransformer(CountVectorizer):

    def __init__(self):
        super().__init__()

    def fit_transform(self, count_matrix: List[List[float]]) \
            -> List[List[float]]:
        """Реализует tfidf = tf * idf для count_matrix"""
        tf_matrix = self.tf_transform(count_matrix)
        idf_values = self.idf_transform(count_matrix)
        tfidf_matrix = []
        for i in range(len(count_matrix)):
            tfidf_row = [round(tf_matrix[i][j] * idf_values[j], 3) for j in
                         range(len(count_matrix[i]))]
            tfidf_matrix.append(tfidf_row)

        return tfidf_matrix


class TfidfVectorizer(CountVectorizer):
    def __init__(self, tf_class=TfidfTransformer):
        super().__init__()
        self.transformer = tf_class()

    def fit_transform(self, corpus: List[str]) -> List[List[float]]:
        """Реализует tfidf = tf * idf для corpus"""
        count_matrix_numbers = super().fit_transform(corpus)
        return self.transformer.fit_transform(count_matrix_numbers)


if __name__ == '__main__':
    corpus = ['Crock,  Pot Pasta Never boil pasta again',
              'Pasta Pomodoro Fresh ingredients Parmesan to taste']
    count_vectorizer = CountVectorizer()
    transformed = count_vectorizer.fit_transform(corpus)

    print(f'corpus: {corpus}\n')
    print('CountVectorizer:')
    print(f'fit_transform: {transformed}')
    print(f'get_feature_names: {count_vectorizer.get_feature_names()}')
    print(
        f'tf_transform: {count_vectorizer.tf_transform(transformed)}')
    print(
        f'idf_transform: {count_vectorizer.idf_transform(transformed)}\n')

    print('TfidfTransformer:')
    tfidf_transformer = TfidfTransformer()
    print(
        f'fit_transform: {tfidf_transformer.fit_transform(transformed)}\n')

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    print('TfidVectorizer:')
    print(f'fit_transform: {tfidf_matrix}')
    print(f'get_feature_names: {tfidf_vectorizer.get_feature_names()}')

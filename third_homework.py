from typing import Iterable
import re


class CountVectorizer:
    """Класс CountVectorizer представляет собой инструмент для
    преобразования текстовых данных в вектора счетчиков.

    Основные методы:
    - fit_transform(corpus: Iterable[str]) -> list[list[int]]:
    Обучает векторизатор на корпусе текстов и возвращает
    матрицу, где каждая строка представляет собой вектор
    счетчиков слов из корпуса.

    - get_feature_names() -> list[str]: Возвращает список уникальных
     слов, использованных при обучении векторизатора.

    Атрибуты:
    - feature_names: Список уникальных слов после обучения.
    - was_fitted: Флаг, указывающий, был ли
    векторизатор обучен на данных.

    Пример использования:
    vectorizer = CountVectorizer()
    transformed_data = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    """

    def __init__(self):
        """Инициализация объекта CountVectorizer."""
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

    def get_feature_names(self):
        """Возвращает список уникальных слов,
        использованных при обучении векторизатора.

        Returns: list[str]: Список уникальных слов.
        """
        assert self.was_fitted, 'Сначала fit_transform.'
        return list(self.feature_names)


if __name__ == '__main__':
    strings = ['Crock,  Pot Pasta Never boil pasta again',
               'Pasta Pomodoro Fresh ingredients Parmesan to taste']
    vectorizer = CountVectorizer()
    transformed = vectorizer.fit_transform(strings)
    print(vectorizer.get_feature_names())
    print(transformed)

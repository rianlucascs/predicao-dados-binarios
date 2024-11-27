from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from warnings import filterwarnings
filterwarnings('ignore')
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)

class Machines:
    def __init__(self, train, test, after_test, F):
        """
        Inicializa a classe com os conjuntos de dados e as features a serem usadas.
        """
        self.train = train
        self.test = test
        self.after_test = after_test
        self.F = [f'__{f}__' for f in F] if isinstance(F, list) else F

        # Valida se as colunas das features existem nos conjuntos
        self._validate_features()

        # Define X (features) e y (alvo) para cada conjunto
        self.x_train = self.train[self.F]
        self.y_train = self.train.filter(like='alvo').squeeze()

        self.x_test = self.test[self.F]
        self.y_test = self.test.filter(like='alvo').squeeze()

        self.x_after_test = self.after_test[self.F]
        self.y_after_test = self.after_test.filter(like='alvo').squeeze()

    def _validate_features(self):
        """
        Valida se todas as colunas de features existem nos conjuntos de dados.
        """
        for df_name, df in zip(['train', 'test', 'after_test'], [self.train, self.test, self.after_test]):
            missing_features = [f for f in self.F if f not in df.columns]
            if missing_features:
                raise ValueError(f"As seguintes features estão ausentes no conjunto {df_name}: {missing_features}")

    def train_decision_tree(self, criterion='gini', max_depth=3):
        """
        Treina um modelo de Decision Tree Classifier.

        Args:
            criterion (str): Critério para medir a qualidade do split ('gini' ou 'entropy').
            max_depth (int): Profundidade máxima da árvore.

        Returns:
            DecisionTreeClassifier: Modelo treinado.
        """
        model = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth)
        model.fit(self.x_train, self.y_train)
        return model

    def _apply_predict(self, model, X):
        """
        Realiza predições com o modelo fornecido.

        Args:
            model: Modelo treinado.
            X: Conjunto de dados de entrada.

        Returns:
            pandas.Series: Predições realizadas.
        """
        return pd.Series(model.predict(X), index=X.index, name='predicao')

    def predict_train(self, model):
        """
        Adiciona as predições ao conjunto de treino.

        Args:
            model: Modelo treinado.

        Returns:
            pandas.DataFrame: Conjunto de treino com as predições.
        """
        self.train['predicao'] = self._apply_predict(model, self.x_train)
        return self.train

    def predict_test(self, model):
        """
        Adiciona as predições ao conjunto de teste.

        Args:
            model: Modelo treinado.

        Returns:
            pandas.DataFrame: Conjunto de teste com as predições.
        """
        self.test['predicao'] = self._apply_predict(model, self.x_test)
        return self.test

    def predict_after_test(self, model):
        """
        Adiciona as predições ao conjunto pós-teste.

        Args:
            model: Modelo treinado.

        Returns:
            pandas.DataFrame: Conjunto pós-teste com as predições.
        """
        self.after_test['predicao'] = self._apply_predict(model, self.x_after_test)
        return self.after_test

    def evaluate(self):
        """
        Avalia o modelo nos conjuntos de treino, teste e pós-teste usando diversas métricas.

        Returns:
            dict: Métricas de avaliação para treino, teste e pós-teste.
        """
        # Avaliação no conjunto de treino
        train_accuracy = accuracy_score(self.y_train, self.train['predicao'])
        train_precision = precision_score(self.y_train, self.train['predicao'])
        train_recall = recall_score(self.y_train, self.train['predicao'])
        train_f1 = f1_score(self.y_train, self.train['predicao'])
        train_confusion = confusion_matrix(self.y_train, self.train['predicao'])

        # Avaliação no conjunto de teste
        test_accuracy = accuracy_score(self.y_test, self.test['predicao'])
        test_precision = precision_score(self.y_test, self.test['predicao'])
        test_recall = recall_score(self.y_test, self.test['predicao'])
        test_f1 = f1_score(self.y_test, self.test['predicao'])
        test_confusion = confusion_matrix(self.y_test, self.test['predicao'])

        # Avaliação no conjunto after_test
        after_test_accuracy = accuracy_score(self.y_after_test, self.after_test['predicao'])
        after_test_precision = precision_score(self.y_after_test, self.after_test['predicao'])
        after_test_recall = recall_score(self.y_after_test, self.after_test['predicao'])
        after_test_f1 = f1_score(self.y_after_test, self.after_test['predicao'])
        after_test_confusion = confusion_matrix(self.y_after_test, self.after_test['predicao'])

        return {
            "train": {
                "accuracy": train_accuracy,
                "precision": train_precision,
                "recall": train_recall,
                "f1_score": train_f1,
                "confusion_matrix": train_confusion.tolist()
            },
            "test": {
                "accuracy": test_accuracy,
                "precision": test_precision,
                "recall": test_recall,
                "f1_score": test_f1,
                "confusion_matrix": test_confusion.tolist()
            },
            "after_test": {
                "accuracy": after_test_accuracy,
                "precision": after_test_precision,
                "recall": after_test_recall,
                "f1_score": after_test_f1,
                "confusion_matrix": after_test_confusion.tolist()
            }
        }

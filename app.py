# metoda wczytująca punktacje
# metoda wczytujaca wyniki
# metoda wczytująca kategorie
# core apki? - tak zeby to było ładnie spakowane i każdy mógł użyć
import pandas as pd

class DataLoader():
    def result_loader(self, name):
        results = pd.read_csv(name, ';')
        results_better = results[["Nazwisko", "Imi�", "Trasa", "Miejsce", "Ur."]]
        return results_better

    def category_loader(self):
        category = pd.read_csv('category.csv', ';')
        return category

    def score_loader(self):
        score = pd.read_csv('score.csv', ';')
        return score

if __name__ == "__main__":
    loader = DataLoader()
    results = loader.result_loader('nocny-resuts.csv')
    category = loader.category_loader()
    print(loader.score_loader())
# metoda wczytująca punktacje
# metoda wczytujaca wyniki
# metoda wczytująca kategorie
# core apki? - tak zeby to było ładnie spakowane i każdy mógł użyć
import pandas as pd

class DataLoader():
    def result_loader(self, name):
        results = pd.read_csv(name, ';')
        results_better = results[["Nazwisko", "Imi�", "Trasa", "Miejsce", "Ur.", "Płeć"]]
        return results_better

    def category_loader(self):
        category = pd.read_csv('category.csv', ';')
        return category

    def score_loader(self):
        score = pd.read_csv('score.csv', ';')
        return score

    def general_loader(self):
        try:
            general = pd.read_csv('general.csv')
        except:
            col = ['Nazwisko', 'Imie', 'Kategoria_wiekowa']
            general = pd.DataFrame(columns=col)
        return general

class ScoreCalculator():
    def method(self, score, category, results, general):
        for row in results:
            try:
                cat = results['Płeć'] + '_' + kategoria 
                # sprawdzenie kategorii - osobna metoda?
                # policzenie punktów - osobna metoda?
                #  a w zasadzie od razu stworzyc dla wszystkich etapów kolumny i wtedy liczenie ogólem jest spoko?
                pass
            except:
                # nowy wiersz jak ktoś jeszcze nie był 
                pass

if __name__ == "__main__":
    loader = DataLoader()
    results = loader.result_loader('nocny-resuts.csv')
    category = loader.category_loader()
    score = loader.score_loader()
    general = loader.general_loader()


    #  dobra musi byc wczytywanie kolejnych resultsów i tworzeni kolejnych kolumn w generalce

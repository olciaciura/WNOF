# metoda wczytująca punktacje
# metoda wczytujaca wyniki
# metoda wczytująca kategorie
# core apki? - tak zeby to było ładnie spakowane i każdy mógł użyć
import pandas as pd

class DataLoader():
    def result_loader(self, name):
        results = pd.read_csv(name, ';')
        results = results[["Nazwisko", "Imi�", "Trasa", "Miejsce", "Ur."]]
        results = results.rename(columns = {"Imi�":"Imie"})
        return results

    def category_loader(self):
        category = pd.read_csv('category.csv', ';')
        return category

    def score_loader(self):
        score = pd.read_csv('score.csv', ';')
        return score
    
    def general_loader(self, etaps):
        try:
            general = pd.read_csv('general.csv', ';')
            general.insert( 3*etaps, f'cat_etap_{etaps}', True)
            general.insert(1 + 3*etaps, f'place_etap_{etaps}', True)
            general.insert(2 + 3*etaps, f'score_etap_{etaps}', True)
        except:
            columns = ['lp', 'Nazwisko i imie', 'Kateogria']
            for i in range(etaps):
                columns.append([f'cat_etap_{i}', f'place_etap_{i}', f'score_etap_{i}'])
            general = pd.DataFrame(columns)
        
        return general

class General():
    def add_person(self, general, results):
        for result in results:
            for row in result.itertuples():
                person = row.Nazwisko + row.Imie
                print(type(general.values()))
                if person not in general.values():
                    general.append({'Nazwisko i imie': person})


if __name__ == "__main__":
    loader = DataLoader()
    general_calc = General()
    category = loader.category_loader()
    score = loader.score_loader()
    results = []
    etaps = int(input('Podaj liczbe etapów: '))
    for i in range(etaps):
        results.append(loader.result_loader(f'results_etap_{i+1}.csv'))
    general = loader.general_loader(etaps)
    general_calc.add_person(general, results)
    print(general)







# metoda wczytująca punktacje
# metoda wczytujaca wyniki
# metoda wczytująca kategorie
# core apki? - tak zeby to było ładnie spakowane i każdy mógł użyć
import pandas as pd

class DataLoader():
    def result_loader(self, name):
        results = pd.read_csv(name, sep = ';')
        results = results[["Nazwisko", "Imi�", "Trasa", "Miejsce", "Ur.", "P�e�"]]
        results = results.rename(columns = {"Imi�":"Imie"})
        results = results.rename(columns = {"P�e�":"Plec"})
        results = results.rename(columns = {"Ur.":"Ur"})
        return results

    def category_loader(self):
        category = pd.read_csv('category.csv', sep = ';')
        return category

    def score_loader(self):
        score = pd.read_csv('score.csv', sep = ';', index_col=0)
        return score
    
    def general_loader(self, etaps):
        try:
            general = pd.read_csv('general.csv', sep = ';')
            general.insert( 3*etaps - 1, f'cat_etap_{etaps}', True)
            general.insert(3*etaps, f'place_etap_{etaps}', True)
            general.insert(1 + 3*etaps, f'score_etap_{etaps}', True)
        except:
            columns = ['Nazwisko i imie', 'Kategoria']
            for i in range(etaps):
                columns.append(f'cat_etap_{i}')
                columns.append(f'place_etap_{i}')
                columns.append(f'score_etap_{i}')
            columns.append('sum')
            general = pd.DataFrame(columns = columns)
        
        return general

class General():
    def cat(self, person, category):
        if person.Plec == 'F':
            cat = 'K'
        else:
            cat = "M"
        
        for row in category.itertuples():
            if person.Ur > row.max and  person.Ur < row.min:
                cat = cat + '_' + row.category
        return cat

    def add_data(self, general, results, category, score):
        for i in range(len(results)):
            for row in results[i].itertuples():
                person = row.Nazwisko + row.Imie
                if person not in general.values:
                    print(type(general))
                    columns = general.columns
                    new_row = dict.fromkeys(columns, None)
                    
                    new_row['Nazwisko i imie'] = person
                    new_row['Kategoria'] = self.cat(row, category)
                    new_row[f'''cat_etap_{i}'''] = row.Trasa
                    new_row[f'''place_etap_{i}'''] = row.Miejsce
                    try:
                        new_row[f'''score_etap_{i}'''] = score.loc['A'][int(row.Miejsce) - 1]
                    except:
                        new_row[f'''score_etap_{i}'''] = 0
                    general = general.append(new_row, ignore_index = True)
                else:
                    
                    general.at[f'''cat_etap_{i}'''][person] = row.Trasa
                    general.at[f'''place_etap_{i}'''][person] = row.Miejsce
                    try:
                        general.at[f'''score_etap_{i}'''][person] = score.loc['A'][int(row.Miejsce) - 1]
                    except:
                        general.at[f'''score_etap_{i}'''][person] = 0
        return general
    
    def calculate(self, general):
        for r in range(len(general)):
            person = general.loc[0][r]
            general.at['sum'][person] = 0
            for i in range(5, len(general), 3):
                general.at['sum'][person] += general.loc[i][r]
        return general

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
    general = general_calc.add_data(general, results, category, score)
    print(general)
    general = general_calc.calculate(general)
    print(general)
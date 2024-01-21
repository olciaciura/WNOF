# poprawi ddawanie sumy
import pandas as pd

class DataLoader():
    def result_loader(self, name):
        results = pd.read_csv(name, sep = ';', encoding='latin-1')
        print(results.columns)
        results = results[["Nazwisko", "Imiï¿½", "Trasa", "Miejsce", "Ur.", "Pï¿½eï¿½"]]
        results = results.rename(columns = {"Imiï¿½":"Imie"})
        results = results.rename(columns = {"Pï¿½eï¿½":"Plec"})
        results = results.rename(columns = {"Ur.":"Ur"})

        results = results[results['Trasa'] != 'MIX']

        return results

    def category_loader(self):
        category = pd.read_csv('category.csv', sep = ';')
        return category

    def score_loader(self):
        score = pd.read_csv('score.csv', sep = ';', index_col=0)
        return score
    
    def general_loader(self):
        try:
            general = pd.read_csv('general.csv', sep=',')
            print(general.head(20))
        except FileNotFoundError:
            general = pd.DataFrame(columns=['Nazwisko i imie', 'Kategoria'])
        return general

class General():
    def cat(self, ur, name, category):
        print(str(type(name)) + ' :' + str(name))
        if name.endswith('a'):
            cat = 'K'
        else:
            cat = "M"
        
        for row in category.itertuples():
            if ur >= row.max and  ur <= row.min:
                cat = cat + '_' + row.category
        return cat
    
    def add_data(self, general, results, category, score, stage):
        stage_columns = [f'Trasa_etap_{stage}', f'Punkty_etap_{stage}']

        for col in stage_columns:
            if col not in general.columns:
                general[col] = ''

        existing_row_index = None  # Initialize outside the loop

        for index, nazwisko, imie, trasa, miejsce, ur, plec in results.itertuples():
            try:
                person = nazwisko + ' ' + imie
            except:
                person = nazwisko

            if person not in general['Nazwisko i imie'].values:
                new_row = {
                    'Nazwisko i imie': person,
                    'Kategoria': self.cat(ur, imie, category),
                    f'Trasa_etap_{stage}': trasa,
                    f'Punkty_etap_{stage}': 0
                }
                try:
                    new_row[f'Punkty_etap_{stage}'] = score.loc[trasa][int(miejsce) - 1]
                except:
                    new_row[f'Punkty_etap_{stage}'] = 0

                general = general.append(pd.DataFrame([new_row]), ignore_index=True)
                existing_row_index = general.index[general['Nazwisko i imie'] == person][0]
            else:
                existing_row_index = general.index[general['Nazwisko i imie'] == person][0]
                general.loc[existing_row_index, f'Trasa_etap_{stage}'] = trasa
                try:
                    general.loc[existing_row_index, f'Punkty_etap_{stage}'] = score.loc[trasa][int(miejsce) - 1]
                except:
                    general.loc[existing_row_index, f'Punkty_etap_{stage}'] = 0
        print(general)
        return general

    # def add_data(self, general, results, category, score):
    #     for index, nazwisko, imie, trasa, miejsce, ur, plec in results.itertuples():
    #         try:
    #             person = nazwisko + ' ' + imie
    #         except:
    #             person = nazwisko
    #         if person not in general.values:

    #             new_row = {
    #                 'Nazwisko i imie': person,
    #                 'Kategoria': self.cat(ur, imie, category),
    #                 'place': miejsce,
    #                 'score': 0
    #             }
    #             try:
    #                 new_row['score'] = score.loc[trasa][int(miejsce) - 1]
    #             except:
    #                 new_row['score'] = 0
    #             general = general.append(pd.DataFrame([new_row]), ignore_index = True)
    #         else:
    #             pass
    #     return general
    
    def calculate(self, general):
        score_columns = [col for col in general.columns if 'Punkty_etap_' in col]
        
        # Convert score-related columns to numeric
        general[score_columns] = general[score_columns].apply(pd.to_numeric, errors='coerce')
        
        # Sum scores and create 'Suma' column
        general['Suma'] = general[score_columns].sum(axis=1, skipna=True)
        
        return general

    
    def sort(self, general):
        general = general.sort_values(['Kategoria', 'Suma'], ascending=[True, False], ignore_index=True)
        return general

if __name__ == "__main__":
    loader = DataLoader()
    general_calc = General()
    category = loader.category_loader()
    score = loader.score_loader()
    stages = 2  # Assuming there are 3 stages, you can adjust this based on your actual number of stages

    general = loader.general_loader()

    results = loader.result_loader(f'results_stage_{stages}.csv')
    general = general_calc.add_data(general, results, category, score, stages)

    general = general_calc.calculate(general)
    # general = general_calc.sort(general)
    general.to_csv('general.csv', index=False)
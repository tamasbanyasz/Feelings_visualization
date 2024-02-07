from python_value_of_feeling import ValueOfFeeling as vf
import plotly.express as px
from random import choice
from time import time
import pandas as pd


class Feelings:
    def __init__(self):
        self.feelings = ["Happy", "Hate", "Calm", "Sad", "Joy", "Anger"]
        self.starter_df = pd.DataFrame(columns = ['Feeling', 'First moment', 'Second moment', 'Third moment', 'Average'])
 
    def create_feel(self, list_of_values, average_value): # create feel by random feeling and the list of average values
        return (choice(self.feelings), list_of_values[0], list_of_values[1], list_of_values[2], average_value)
    
    def append_datas_to_starter_dataframe(self):
        
        for _ in range(50):
            vf.number_of_generator_obj(3) # Number of generator obj
            
            # Add feelings to DataFrame
            self.starter_df.loc[len(self.starter_df)] = self.create_feel(next(vf.get_list_of_average_values()), 
                                                          vf.get_average_value_from_list_of_average_values())
            
    def cleared_masked_datas(self): # Masking DataFrame by feelings
        for feeling in self.feelings:
            mask = self.starter_df['Feeling'] == feeling 
            datas_by_mask = pd.DataFrame(self.starter_df[mask])  
            cleared_masked_datas = datas_by_mask.drop(columns=['Feeling', 'Average']).T
            
            yield cleared_masked_datas, feeling
        

    def reshape_df_columns_by_feelings_and_they_values(self):
        
        new_df = pd.DataFrame()

        for cleared_masked_datas_with_feeling in self.cleared_masked_datas():
                     
            new_col = pd.DataFrame(cleared_masked_datas_with_feeling[0].values.ravel('F'), 
                                   columns = [cleared_masked_datas_with_feeling[1]])
            
            sorted_new_col = new_col.sort_values(by=[cleared_masked_datas_with_feeling[1]]).reset_index(drop=True)
            
            new_df[cleared_masked_datas_with_feeling[1]] = sorted_new_col
        
        return new_df
    
    def feelings_one_by_one(self):
        
        separated_feelings = []
        
        for cleared_masked_datas_with_feeling in self.cleared_masked_datas():
            
            
            get_feeling = cleared_masked_datas_with_feeling[0].stack().droplevel(1).to_frame(name=cleared_masked_datas_with_feeling[1])
            
            separated_feelings.append(get_feeling.reset_index().rename(columns={'index': 'Moments'}))
            
        return separated_feelings
        
    
start = time()
obj = Feelings()

obj.append_datas_to_starter_dataframe()

print("\nStarter df:")
print(obj.starter_df)
print("--------------------------------------------------------")

print("Reshaped df: ")
print(obj.reshape_df_columns_by_feelings_and_they_values())
print("--------------------------------------------------------")
end = time()

# Data visualization
fig = px.scatter_3d(obj.starter_df, x='First moment', y='Second moment', z='Third moment',
                    color='Feeling', symbol='Feeling')
fig.show()

print(end-start)


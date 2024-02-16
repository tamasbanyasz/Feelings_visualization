from numpy import fromiter, average
from random import randint


class ValueOfFeeling:
    def __init__(self):
        self.list_of_average_values = []
    
    @classmethod    
    def create_generator_obj(cls,fromiter_end = 100001):  # Create generator object with specified iterable range between 0 and 100001
        yield fromiter((i for i in range(0, fromiter_end)), int)
    
    @classmethod
    def number_of_generator_obj(cls, number_of_generator_obj = 1):
        
        '''
        Add to a list the average of the generator object in fast way.
        
        The "number_of_generator_obj" define the wanted number of generator objects.
        
        In this case we would like 3 object because of the 'First moment', 'Second moment', 'Third moment'.
        
        Then we added each average values to list. 
        
        '''
        
        cls.list_of_average_values = ([average(next(cls.create_generator_obj(randint(1, 100000)))) for i in range(number_of_generator_obj)])
        
          
    @classmethod
    def get_list_of_average_values(cls):
        yield fromiter(cls.list_of_average_values, float) # Get the full list with the average values
           
    @classmethod   
    def get_average_value_from_list_of_average_values(cls): # Get the each row average values from the list
        return average(cls.list_of_average_values, axis=0)
    
if __name__ == "__main__":
    ValueOfFeeling()


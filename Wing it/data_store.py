'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''
import time
import pickle

db_bk = "db_bk.p"

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    
}
## YOU SHOULD MODIFY THIS OBJECT ABOVE
def db_load_bk():
    '''
    <Loads backup database pickle file on start up,
    and if there isn't one that exists, creates one using the initial_object dictionary>

    Arguments:
        None
    Exceptions:
        None
    Return Value:
        None
    '''

    # check if the backup file exists
    try:
        with open(db_bk, "rb") as backup_file:
            backup_file.read()

    # if it doesn't, create a file using the initial_object dictionary
    except IOError:
        with open(db_bk, "wb") as backup_file:
            pickle.dump(initial_object, backup_file)
    
    # close the file for safe measure
    finally:
        backup_file.close()

    # open the pickle file and store it to the database dictionary
    with open(db_bk, "rb") as backup_file:
        store = pickle.load(backup_file)

        # close the file
        backup_file.close()

    # return the database for assignment
    return store

def db_save_bk(store):
    '''
    <Save the database to a pickle file>

    Arguments:
        None
    Exceptions:
        None
    Return Value:
        None
    '''

    # clear the backup file
    with open(db_bk, "w", encoding = "utf8") as f:
        f.close()

    # open the pickle file
    with open(db_bk, "wb") as backup_file:

        # dump the data in the pickle file
        pickle.dump(store, backup_file)

        # close the file
        backup_file.close()

class Datastore:
    def __init__(self):
        self.__store = db_load_bk()

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store
        db_save_bk(store)

print('Loading Datastore...')

global data_store
data_store = Datastore()

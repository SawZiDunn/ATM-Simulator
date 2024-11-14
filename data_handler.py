import pickle

DATA_FILE = "db.pkl"

class DataHandler:
    def __init__(self):
        self._customers = self.load_data(DATA_FILE)

    def save_data(self, data):
        """Save data to the file and update the in-memory cache."""
        with open(DATA_FILE, 'wb') as file:
            pickle.dump(data, file)
        self._customers = data  # Update in-memory data

    def load_data(self, filename):
        """Load data from the file."""
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return []

    def get_customers(self):
        """Return in-memory customer data."""
        return self._customers

    def refresh_customers(self):
        """Reload customers from file to refresh the in-memory data."""
        self._customers = self.load_data(DATA_FILE)

db = DataHandler()
db.refresh_customers()
for i in db.get_customers():

    print(i )
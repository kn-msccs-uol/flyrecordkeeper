"""
How to use the RecordManager class:

Basic workflow:

1. Create a RecordManager instance
2. Use it to create client and airline records
3. Retrieve records by type


 | Code snippet example |
\/                      \/

# Create a manager
manager = RecordManager()

# Create records
client = manager.create_client("John Doe", "123 Main St", "New York", "USA", "555-1234")
airline = manager.create_airline("Skyways Airlines")

# Retrieve records
all_clients = manager.get_records_by_type("client")
"""
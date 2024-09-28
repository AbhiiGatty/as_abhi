from mongoengine import connect


def initialize_db(mongo_uri):
    """
    Initialize the MongoDB connection.
    """
    connect(host=mongo_uri)
    return "Database connection already established."

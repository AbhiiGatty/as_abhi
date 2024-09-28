from mongoengine import Document, StringField, DateTimeField, BooleanField
import datetime


class Test(Document):
    name = StringField(required=True, unique=True)
    status = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))  # Corrected
    is_archived = BooleanField(default=False)

    def create_test(self, name, status):
        """Create a new test."""
        test = Test(name=name, status=status)
        test.save()
        return test

    def delete_test(self):
        """Delete the test."""
        self.delete()

    def unpublish_test(self):
        """Unpublish the test."""
        self.status = 'unpublished'
        self.save()

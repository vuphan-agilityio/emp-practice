from haystack import indexes
from .models import Employee


class EmployeeIndex(indexes.SearchIndex, indexes.Indexable):
    """EmployeeIndex haystack."""

    text = indexes.CharField(document=True)
    email = indexes.CharField(model_attr='user__email')
    age = indexes.IntegerField(model_attr='age')

    def get_model(self):
        return Employee

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

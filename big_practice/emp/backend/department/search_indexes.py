from haystack import indexes
from .models import Department


class DepartmentIndex(indexes.SearchIndex, indexes.Indexable):
    """DepartmentIndex haystack."""

    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Department

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

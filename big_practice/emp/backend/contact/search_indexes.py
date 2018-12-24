from haystack import indexes
from .models import Contact


class ContactIndex(indexes.SearchIndex, indexes.Indexable):
    """ContactIndex haystack."""

    text = indexes.CharField(document=True)
    username = indexes.CharField(model_attr='user__username')

    def get_model(self):
        return Contact

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

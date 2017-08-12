import datetime
from haystack import indexes
from feed.models import Wish

class feedIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='wish_text',null=True)
    category = indexes.CharField(model_attr='category',null=True)
    subcategory = indexes.CharField(model_attr='subcategory',null=True)
    price = indexes.IntegerField(model_attr='price',null=True)
    location = indexes.CharField(model_attr='location',null=True)
    status = indexes.CharField(model_attr='status')
    added = indexes.DateTimeField(model_attr='added')
    
    def get_model(self):
        return Wish
    def prepare_wish_text(self, obj):
	    return "Wish"
    def prepare(self, obj):
        data = super(feedIndex, self).prepare(obj)
        data["_boost"] = 1.5
        return data

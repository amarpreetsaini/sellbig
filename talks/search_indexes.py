import datetime
from haystack import indexes
from talks.models import Talk

class talkIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title', boost=1.50,null=True)
    #tags = indexes.CharField(model_attr='tags')
    added = indexes.DateTimeField(model_attr='added')

    def get_model(self):
        return Talk
        
    def prepare_title(self, obj):
	    return "Talk"
    
 

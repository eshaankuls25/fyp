import pickle
class TestPickler (pickle.Pickler):
    def save(self, obj):
        print 'pickling object', obj, 'of type', type(obj)
        pickle.Pickler.save(self, obj)
import datetime
import flask.ext.mongoengine

db = flask.ext.mongoengine.MongoEngine();

class PassSpec(db.EmbeddedDocument):
	length = db.IntField(default = 12, required=True)
	version = db.IntField(default = 0, required=True)
	hash_func = db.StringField(max_length=255, required=True)

class UrlSpec(db.EmbeddedDocument):
	value = db.StringField(max_length=255, required=True, regex='(str|glob|re):.+')
	#meta = {'allow_inheritance': True}
	def check(self, url):
		return False

# class UrlSpecStr(UrlSpec):
# 	def check(self, url):
# 		if self.value == url:
# 			return True
# 		else:
# 			return False
# 
# class UrlSpecGlob(UrlSpec):
# 	def check(self, url):
# 		return True
	
class Site(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	created_by = db.ReferenceField('User')
	
	name = db.StringField(max_length=255, required=True, unique_with='created_by')
	passSpec = db.EmbeddedDocumentField(PassSpec)

	keys = db.ListField(db.EmbeddedDocumentField(UrlSpec), required=True)
	
class User(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    mail = db.EmailField(unique=True)
    name = db.StringField(max_length=255, required=True, unique=True)
    dbPass = db.StringField(max_length=64)
    
    sites = db.ListField( db.ReferenceField('Site',reverse_delete_rule=4  ) )

    def __unicode__(self):
        return self.name


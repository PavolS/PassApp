from flask import request, jsonify
from flask.ext import restful
import models
import json

class Hello(restful.Resource):
    def get(self):
        return {'hello': 'world'}

##def get_user_doc(name):
##        users_found = models.User.objects(name=name)
##        if len(users_found) == 1:
##            return users_found[0]
##        elif len(users_found) == 0:
##            raise Exception('No such user')
##        else:
##            raise Exception('Database Integrity Error')
##
##def get_user(name):
##    return json.loads(get_user_doc(name).to_json())

class User(restful.Resource):
    def doc(name):
        return models.User.objects.get(name=name)
    def dic(name):
        return json.loads(User.doc(name).to_json() )
    def get(self, username):
        return User.dic(name)

class Users(restful.Resource):
    def get(self):
        users_found = models.User.objects.select_related(max_depth=2)
        return len(users_found)
    def post(self):
        json_str = json.dumps( request.get_json(force=True) )
        user = models.User.from_json( json_str )
        if user.save():
            return json.loads(user.to_json()), 200
        else:
            return json, 400

class Sites(restful.Resource):
    def get(self,username):
        site_oids = User.doc(username).sites
        return [ json.loads(site_oid.to_json()) for site_oid in site_oids ]
    def post(self,username):
        site = request.get_json(force=True)
        site_doc = models.Site.from_json( json.dumps(site) )
        user_doc = User.doc( username )
        site_doc.created_by = user_doc
        if site_doc.save():
            user_doc.update(push__sites=site_doc)
            return json.loads(site_doc.to_json()), 200
        else:
            return json, 400

class Site(restful.Resource):
    def doc(username,sitename):
        user_doc=User.doc(username)
        return models.Site.objects.get(name=sitename,created_by=user_doc)
    def dic(username,sitename):
        return json.loads(Site.doc(username,sitename).to_json() )
    def get(self,username,sitename):
        return Site.dic(username,sitename);
    def delete(self,username,sitename):
        return Site.doc(username,sitename).delete()

    
def Api(app):
    api = restful.Api(app)
    api.add_resource(Hello, '/')
    api.add_resource(Users, '/users')
    api.add_resource(User, '/users/<string:username>')
    api.add_resource(Sites, '/sites/<string:username>')
    api.add_resource(Site, '/sites/<string:username>/<string:sitename>')

    return api

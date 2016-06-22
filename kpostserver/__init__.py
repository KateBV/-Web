from pyramid.config import Configurator
from models import User, Session, Base, engine, Post, Tag, TypeTag
from pyramid.session import SignedCookieSessionFactory	
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Deny
from pyramid.security import Authenticated, Everyone

my_session_factory = SignedCookieSessionFactory('itsaseekreet')

class HelloFactory(object):
    def __init__(self, request):
        self.__acl__ = [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated, 'add')]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    Base.metadata.create_all()
    DBSession = Session(bind=engine)
    result = DBSession.query(User).all()
    if (len(result) == 0):
        new_user = User(name="admin", password = "12345")
        DBSession.add(new_user)
        DBSession.commit()

    ####

    authn_policy = AuthTktAuthenticationPolicy('sosecret', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, session_factory=my_session_factory, root_factory=HelloFactory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('post', '/post/{id}')
    config.add_route('post_delete', '/post/{id}/remove')
    config.add_route('user', '/user/{id}')

    config.add_route('signin', '/signin')
    config.add_route('signout', '/signout')
    config.add_route('signup', '/signup')
    config.add_route('addpost', '/post')
    config.add_route('addtag', '/tag')
    config.add_route('addtypetag', '/typetag')
    config.scan()

    return config.make_wsgi_app()

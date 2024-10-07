from passlib.context import CryptContext

pwdContext = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class Hash():
    def bcrypt(password: str):
        return pwdContext.hash(password)
from {{cookiecutter.app_name}}.extensions import db


class Example(db.Model):
    """Example Model structure
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Any post processing steps, such as hashing a password field
        # self.password = pwd_context.hash(self.password)

    def __repr__(self):
        return "<User %s>" % self.name

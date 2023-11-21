# -*- coding:utf-8 -*-
from main import db

role_permission = db.Table("auth.roles_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("auth.roles.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("auth.permissions.id")))


class Permission(db.Model):
    __tablename__ = "permissions"
    __table_args__ = {"schema":"auth"}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20))
    active = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Permission {self.id}>"


class Role(db.Model):
    __tablename__ = "roles"
    __table_args__ = {"schema":"auth"}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20))
    active = db.Column(db.Boolean)
    permissions = db.relationship("Permission", 
        secondary=role_permission,  
        primaryjoin=(id == role_permission.c.role_id),
        backref="roles")

    def __repr__(self):
        return f"<Role {self.id}>"


user_role = db.Table("auth.users_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("auth.users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("auth.roles.id")))


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema":"auth"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(20))
    password = db.Column(db.String(256))
    active = db.Column(db.Boolean)
    roles = db.relationship("Role", 
        secondary=user_role,
        primaryjoin=(id == user_role.c.user_id),
        backref="users")

    def __repr__(self):
        return f"<User {self.id}>"

# -*- coding:utf-8 -*-
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

class Base(DeclarativeBase):
    pass


roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("auth.roles.id")),
    Column("permission_id", ForeignKey("auth.permissions.id")),
    schema="auth")

users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", ForeignKey("auth.users.id")),
    Column("role_id", ForeignKey("auth.roles.id")),
    schema="auth")

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema":"auth"}

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column()

    def __repr__(self):
        return f"<Permission {self.id}>"

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema":"auth"}

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column()
    permissions: Mapped[List[Permission]] = relationship(secondary=roles_permissions)  

    def __repr__(self):
        return f"<Role {self.id}>"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema":"auth"}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column()
    roles: Mapped[List[Role]] = relationship(secondary=users_roles)


    def __repr__(self):
        return f"<User {self.id}>"

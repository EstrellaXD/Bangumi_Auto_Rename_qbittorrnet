import logging

from fastapi import HTTPException
from sqlmodel import Session, select

from module.models import ResponseModel
from module.models.user import User, UserLogin, UserUpdate
from module.security.jwt import get_password_hash, verify_password

logger = logging.getLogger(__name__)


class UserDatabase:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, username):
        statement = select(User).where(User.username == username)
        result = self.session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return result

    def auth_user(self, user: User):
        statement = select(User).where(User.username == user.username)
        result = self.session.exec(statement).first()
        if not user.password:
            return ResponseModel(
                status_code=401, status=False, msg_en="Incorrect password format", msg_zh="密码格式不正确"
            )
        if not result:
            return ResponseModel(
                status_code=401, status=False, msg_en="User not found", msg_zh="用户不存在"
            )
        if not verify_password(user.password, result.password):
            return ResponseModel(
                status_code=401,
                status=False,
                msg_en="Incorrect password",
                msg_zh="密码错误",
            )
        return ResponseModel(
            status_code=200, status=True, msg_en="Login successfully", msg_zh="登录成功"
        )

    def update_user(self, username, update_user: UserUpdate):
        # Update username and password
        statement = select(User).where(User.username == username)
        result = self.session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        if update_user.username:
            result.username = update_user.username
        if update_user.password:
            result.password = get_password_hash(update_user.password)
        self.session.add(result)
        self.session.commit()
        return result

    def merge_old_user(self):
        # get old data
        statement = """
        SELECT * FROM user
        """
        result = self.session.exec(statement).first()
        if not result:
            return
        # add new data
        user = User(username=result.username, password=result.password)
        # Drop old table
        statement = """
        DROP TABLE user
        """
        self.session.exec(statement)
        # Create new table
        statement = """
        CREATE TABLE user (
            id INTEGER NOT NULL PRIMARY KEY,
            username VARCHAR NOT NULL,
            password VARCHAR NOT NULL
        )
        """
        self.session.exec(statement)
        self.session.add(user)
        self.session.commit()

    def add_default_user(self):
        # Check if user exists
        statement = select(User)
        try:
            result = self.session.exec(statement).all()
        except Exception:
            self.merge_old_user()
            result = self.session.exec(statement).all()
        if len(result) != 0:
            return
        # Add default user
        user = User(username="admin", password=get_password_hash("adminadmin"))
        self.session.add(user)
        self.session.commit()

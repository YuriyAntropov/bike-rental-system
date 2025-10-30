from model.user import User
from view.manager_view import ManagerView
from view.client_view import ClientView
import logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
class LoginViewModel:
    def __init__(self, db, navigate_callback):
        self.db=db
        self.navigate_callback=navigate_callback
        self.user=None
    def login(self, username, password):
        self.user=User.authenticate(self.db, username, password)
        logger.info(f"User after authentication: {self.user.__dict__ if self.user else None}")
        return self.user is not None
    def register(self, username, password):
        user, error=User.register(self.db, username, password)
        if error:
            raise Exception(error)
        self.user=user
        logger.info(f"User after registration: {self.user.__dict__}")
        return True
    def navigate(self):
        if not self.user:
            logger.error("Navigation failed: No user authenticated")
            return False
        logger.info(f"Navigating for user with role: {self.user.role}")
        view=ManagerView if self.user.role=="manager" else ClientView
        self.navigate_callback(view, self.db, self.user)
        return True
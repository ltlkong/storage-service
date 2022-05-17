from common.auth import Auth
from resources.BaseResource import BaseResource

auth = Auth()

class UserResource(BaseResource):
    # Check if user token valid
    @auth.verify_token
    def get(self):
        return auth.current_user().json()

    # Handle request
    def post(self):
        # Deactivate user
        pass

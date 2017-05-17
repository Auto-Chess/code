import requests

"""Class which interacts with API provided by webserver"""
class WebServerInterface():
    """Constructs a WebServerInterface
    Args:
        - server_url (str): URL of webserver to interact with
    """
    def __init__(self, server_url="localhost:5000"):
        self.server_url = server_url

        # Mark that we haven't retrieve any ChessBoard credentials yet
        self.chess_board_id = None
        self.chess_board_secret = None

    """Make complete API url
    Args:
        - path (str): Path to add onto end of API url
    """
    def mk_api_url(self, path):
        return "{}{}".format(self.server_url, path)

    """Check response for errors
    Args:
        - resp(requests.Response): Response to check for errors
    
    Returns:
        - None: If no errors
        - dict: Dict with 'status_code' and 'errors' from response
    """
    def check_resp_errs(self, resp):
        # Check for errors
        data = resp.json()
        if 'errors' in data:
            # If errors present
            if len(data['errors']) > 0:
                return dict(status_code=resp.status_code, errors=data['errors'])

        if resp.status_code != 200:
            # If status code not good
            return dict(status_code=resp.status_code, errors=None)

        # If all checks pass, we good
        return None


    """Determines if we are registered with the API yet
    Returns:
        - bool: True if already registered, False if not
    """
    def registered(self):
        if self.chess_board_id is None or self.chess_board_secret is None:
            return False

        return True

    """Register with API to get ChessBoard credentials
    Does not re-register if already has credentials
    
    Returns:
        - bool: True if registration is success, False otherwise
    """
    def register(self):
        if not self.registered():
            resp = requests.get(self.mk_api_url("/chess_board/register"))

            # Check for errors
            errs_dict = self.check_resp_errs(resp)
            if errs_dict is not None:
                print("Error registering ChessBoard: {}".format(errs_dict))
                return False

            # Save creds
            data = resp.json()
            self.chess_board_id = data['chess_board']['id']
            self.chess_board_secret = data['chess_board']['secret']

            return True
        else:
            return False

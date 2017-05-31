import requests

"""Class which interacts with API provided by webserver"""
class WebServerInterface():
    """Constructs a WebServerInterface
    Args:
        - server_url (str): URL of webserver to interact with
    """
    def __init__(self, server_url="http://localhost:5000/"):
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
        - dict: None if success, Dict containing the `status_code` and `errors` if failure
    """
    def register(self):
        if not self.registered():
            resp = requests.get(self.mk_api_url("/chess_board/register"))

            # Check for errors
            errs_dict = self.check_resp_errs(resp)
            if errs_dict is not None:
                return errs_dict

            # Save creds
            data = resp.json()
            self.chess_board_id = data['chess_board']['id']
            self.chess_board_secret = data['chess_board']['secret']

    def push_opponent_move(self, move):
        self._push_chess_move('opponent', move)

    def push_player_move(self, move):
        self._push_chess_move('user', move)

    """Pushes a Chess Move up to the webserver
    Args:
        - player (str): Who made the move, either "user" or "opponent"
        - move (ChessMove): Chess move to push
        
    Returns:
        - dict: None if success, Dict containing the `status_code` and `errors` if failure
        
    Raises:
        - AssertionError: If not registered with API
        - ValueError: If player is not "user" or "opponent"
    """
    def _push_chess_move(self, player, move):
        if not self.registered():
            raise AssertionError("Not registered with API")

        # Check player value
        if player != 'user' and player != 'opponent':
            raise ValueError("player must be \"user\" or \"opponent\"")

        # Make request
        data = {
            'initial_col': move.init_pos.col,
            'initial_row': move.init_pos.row,
            'final_col': move.final_pos.col,
            'final_row': move.final_pos.row
        }
        headers = {
            'Authorization': self.chess_board_secret
        }

        resp = requests.post(self.mk_api_url("/chess_board/{}/moves/{}".format(self.chess_board_id, player)),
                             headers=headers,
                             json=data)

        # Check errors
        errs_dict = self.check_resp_errs(resp)
        if errs_dict is not None:
            return errs_dict

    """Signals game ending for Chess Board. Currently this also de-registers the Chess Board
    Returns:
        - dict: None if success, Dict containing the `status_code` and `errors` if failure
        
    Raises:
        - AssertionError: If not registered with API
    """
    def signal_game_over(self):
        if not self.registered():
            raise AssertionError("Not registered with API")

        # Make request
        headers = {
            'Authorization': self.chess_board_secret
        }

        resp = requests.delete(self.mk_api_url("/chess_board/{}/game_running".format(self.chess_board_id)), headers=headers, json={})

        # Check errors
        errs_dict = self.check_resp_errs(resp)
        if errs_dict is not None:
            return errs_dict

        # De-register
        self.chess_board_id = None
        self.chess_board_secret = None

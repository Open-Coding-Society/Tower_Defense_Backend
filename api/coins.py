from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.coins import Coins

# Create a Blueprint for the coins API
coins_api = Blueprint('coins_api', __name__, url_prefix='/api')

# Create an Api object and associate it with the Blueprint
api = Api(coins_api)

class CoinsAPI:
    class _Coins(Resource):
        """
        API operations for managing coins.
        """

        @token_required()
        def get(self):
            """
            Get the current user's coin balance.
            """
            current_user = g.current_user

            try:
                coins_entry = Coins.query.filter_by(user=current_user.uid).first()
                if coins_entry:
                    return jsonify({'message': 'Coins retrieved successfully', 'coins': coins_entry.read()})
                else:
                    return {'message': 'No coins entry found for the user'}, 404
            except Exception as e:
                return {'message': 'Failed to retrieve coins', 'error': str(e)}, 500

        @token_required()
        def post(self):
            """
            Add coins for killing enemies or spend coins.
            """
            current_user = g.current_user
            body = request.get_json()

            action = body.get('action')  # 'gain' or 'spend'
            coins = body.get('coins')

            if action not in ['gain', 'spend']:
                return {'message': 'Invalid action provided'}, 400

            if coins is None or not isinstance(coins, int) or coins <= 0:
                return {'message': 'Invalid coins value provided'}, 400

            try:
                coins_entry = Coins.query.filter_by(user=current_user.uid).first()
                if not coins_entry:
                    if action == 'spend':
                        return {'message': 'Insufficient coins'}, 400
                    # Create a new coins entry if it doesn't exist
                    coins_entry = Coins(user=current_user.uid, coins=0)

                if action == 'gain':
                    # Add coins to the user's balance
                    coins_entry.coins += coins
                elif action == 'spend':
                    if coins_entry.coins < coins:
                        return {'message': 'Insufficient coins'}, 400
                    # Deduct coins from the user's balance
                    coins_entry.coins -= coins

                coins_entry.create()  # Save changes to the database
                return jsonify({'message': f'Coins {action}ed successfully' if action == "gain" else "Coins spent successfully", 'coins': coins_entry.read()})
            except Exception as e:
                return {'message': f'Failed to {action} coins', 'error': str(e)}, 500

# Register the API resource with the Blueprint
api.add_resource(CoinsAPI._Coins, '/coins')

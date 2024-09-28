from flask import Blueprint, request, jsonify
from app.api.tests.models import Test
from app.middleware.auth_middleware import admin_role_required

test_v1_bp = Blueprint('test_v1', __name__)


@test_v1_bp.route('', methods=['POST'])
@admin_role_required
def create_test():
    data = request.get_json()
    name = data.get('name')
    test = Test.objects(name=name).first()
    if test:
        return jsonify({"error": "Test with that name already exists."}), 400

    status = data.get('status', 'published')  # Default to 'published' if not specified

    # Basic validation
    if not name:
        return jsonify({"error": "Test name is required."}), 400

    # Create a new test
    test = Test().create_test(name, status)
    return jsonify({"message": "Test created successfully.", "test_id": str(test.id)}), 201


@test_v1_bp.route('/<test_id>', methods=['DELETE'])
def delete_test(test_id):
    test = Test.objects(id=test_id).first()

    if not test:
        return jsonify({"error": "Test not found."}), 404

    test.delete_test()
    return jsonify({"message": "Test deleted successfully."}), 204


@test_v1_bp.route('/<test_id>/unpublish', methods=['PATCH'])
def unpublish_test(test_id):
    test = Test.objects(id=test_id).first()

    if not test:
        return jsonify({"error": "Test not found."}), 404

    test.unpublish_test()
    return jsonify({"message": "Test unpublished successfully."}), 200

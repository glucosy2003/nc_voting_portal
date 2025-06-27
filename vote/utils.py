# vote/utils.py

import uuid

def generate_voter_id():
    return str(uuid.uuid4())[:8]  # Generates a short random unique ID

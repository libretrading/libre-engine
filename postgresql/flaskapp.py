from flask import Flask, request, render_template
from flask_cors import CORS  # Import CORS
from models import Base, engine, Session, ActiveUser, InactiveUser

app = Flask(__name__)
CORS(app)

# Create all tables
Base.metadata.create_all(engine)

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == 'POST':
        session = Session()
        email = request.form.get('email')
        api_public = request.form.get('api_public')
        api_secret = request.form.get('api_secret')
        stop_strategy = request.form.get('stop_strategy')

        if not email or not api_public or not api_secret:
            return 'Missing required fields', 400

        # Check if user wants to stop the strategy
        if stop_strategy == 'yes':
            # Check if the user exists in the 'active' table
            active_user = session.query(ActiveUser).filter_by(email=email).first()

            if active_user:
                # Move the user to the 'inactive' table
                session.delete(active_user)  # Remove from active
                session.commit()

                # Add to 'inactive' table
                new_inactive_user = InactiveUser(email=email, api_public=api_public, api_secret=api_secret, to_be_stopped=True)
                session.add(new_inactive_user)
                session.commit()
                session.close()
                return 'Strategy stopped and moved to inactive!', 200
            else:
                session.close()
                return 'User is not currently active, cannot stop the strategy', 400

        else:
            # Check if the user exists in the 'inactive' table (reactivating a user)
            inactive_user = session.query(InactiveUser).filter_by(email=email).first()

            if inactive_user:
                # Remove from inactive table
                session.delete(inactive_user)
                session.commit()

            # Check if the user is already in the 'active' table
            active_user = session.query(ActiveUser).filter_by(email=email).first()

            if active_user:
                # If the user is already active, just update their API keys
                active_user.api_public = api_public
                active_user.api_secret = api_secret
                session.commit()
                session.close()
                return 'API keys updated successfully!', 200
            else:
                # If the user is not active, add them to the 'active' table
                new_active_user = ActiveUser(email=email, api_public=api_public, api_secret=api_secret)
                session.add(new_active_user)
                session.commit()
                session.close()
                return 'User activated and added to the active table!', 200
    else:
        return render_template('manage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='True')  # Ensure app is accessible externally







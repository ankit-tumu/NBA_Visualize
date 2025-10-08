from NBA_Shot_Charts import create_app
import os

app = create_app()

if __name__ == '__main__':
    # The port is dynamically assigned by the hosting service
    port = int(os.environ.get('PORT', 8080))
    # Running with debug=False is crucial for production
    app.run(host='0.0.0.0', port=port, debug=False)

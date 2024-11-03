import os

MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://ExperAdmin:727476@cluster0.kr7hf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'whsec_z0b09hD475gy9YCE5I+jVniA3VsJpkrk')

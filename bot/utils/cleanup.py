import os
import shutil

def cleanup_user_temp(user_id: int):
    path = f"/tmp/{user_id}"
    if os.path.exists(path):
        shutil.rmtree(path)


from app.db.session import SessionLocal
from app.services.user_service import UserService

def seed_admin():
    db = SessionLocal()
    svc = UserService(db)
    existing = svc.get_by_username('admin')
    if existing:
        print('admin exists')
        return
    svc.create_user('admin', 'ChangeMe123!', 'admin')
    print('created admin: admin / ChangeMe123!')

if __name__ == '__main__':
    seed_admin()

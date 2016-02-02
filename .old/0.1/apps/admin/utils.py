import random

def check_access(user, access):
    try:
        if not getattr(user.get_profile(), access)():
            return False
        else:
            return True
    except:
        return False


def random_str(size):
    str = 'qwertyuiopasdfghjklzxcvbnm'
    return ''.join([random.choice(str) for i in range(size)])
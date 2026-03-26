import os
import stat

def check_uinput():
    path = "/dev/uinput"
    print(f"--- Checking {path} ---")
    
    if not os.path.exists(path):
        print(f"❌ {path} does not exist.")
        return

    # Check stats
    st = os.stat(path)
    print(f"Mode: {oct(st.st_mode)}")
    print(f"Owner UID: {st.st_uid}")
    print(f"Group GID: {st.st_gid}")
    
    # Check current user/groups
    print(f"\nCurrent User UID: {os.getuid()}")
    print(f"Current Groups GIDs: {os.getgroups()}")
    
    # Try opening for writing
    try:
        with open(path, 'w') as f:
            print(f"✅ Successfully opened {path} for writing.")
    except PermissionError:
        print(f"❌ Permission Denied: Cannot open {path} for writing.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_uinput()

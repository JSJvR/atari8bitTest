import os
import time
import subprocess
import hashlib
import os
import platform

def watch_atr(atr_file, delay=60, count=10, daemon=False):
    print(os.name)
    print(platform.system())
    prevModified = os.path.getmtime(atr_file)
    prevHash = hashlib.md5(open(atr_file,'rb').read()).hexdigest()
    print(prevHash)
    i = 0
    extract = False
    while i < count or daemon: 
        curModified = os.path.getmtime(atr_file)
        if curModified == prevModified:
            if extract:
                print('File stable. Extracting...')
                extract_atr(atr_file)
                extract = False
            else:
                print('No change')

        else:
            print('File changed. Will extract when stable.')
            prevModified = curModified

            # We don't extract the file right away, in case it's still being modified
            # Instead we set a flag and wait for the next iteration where the file hasn't
            # been modified.
            extract = True

        print(f'Sleeping for {delay} seconds')
        i += 1
        time.sleep(delay)

def extract_atr(atr_file):
    subprocess.run('./from_atr')

if __name__ == '__main__':
    watch_atr('atr/ActionProj.atr', 10, 200)    
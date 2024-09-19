import pexpect
import time
name = 'mazafaka'

def create_wg(wg_profile_name):
    child = pexpect.spawn('sudo bash ./wireguard-install.sh')
    child.sendline('1')
    child.expect('Provide a name for the client:')
    child.sendline(wg_profile_name)
    child.expect("Select a DNS server for the client:")
    child.sendline('2')
    child.interact()
    print(f'Профиль {wg_profile_name} создан.')

create_wg(name)
import requests
import sys
import json
import warnings


KillToken = {
    'token_auth': False,
    'token_serial': '',
    'token_type': ''
}

if len(sys.argv) != 4:
    print("Syntax: ./DeleteTokens <FortiAuthIP> <ApiAdminUsername> <ApiAdminKey>")
    exit(1)

warnings.filterwarnings("ignore")
FortiAuth = sys.argv[1]
user = sys.argv[2]
apiKey = sys.argv[3]


print('Getting a list of users')
userList = requests.get(f'https://{FortiAuth}/api/v1/ldapusers/?format=json&limit=10000&active=true',
                        auth=(user, apiKey),
                        verify=False)

if userList.status_code > 299:
    print(f"Error, got {userList.status_code}")
    exit(1)

userList = userList.json()['objects']
print(f'Found {len(userList)} users')

print('Removing tokens...')
usercounter = 0
for nextuser in userList:
    if nextuser['token_auth']:
        done = requests.patch(f"https://{FortiAuth}/api/v1/ldapusers/{nextuser['id']}/",
                          data=json.dumps(KillToken),
                          auth=(user, apiKey),
                          verify=False)
        if done.status_code < 300:
            print(f'Ok, token removed for {nextuser["username"]}')
            usercounter = usercounter + 1
        else:
            print(f"Got error {done.status_code} for user {nextuser['id']}")
            print(done.content)
    else:
        print(f'User {nextuser["username"]} does not have a token assigned')

print(f'Removed tokens for {usercounter} users')







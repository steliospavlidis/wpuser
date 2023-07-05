# ![wpuser](https://github.com/steliospavlidis/wp-user/assets/138578903/2ca3ee00-19b6-42b7-aa8c-668e4f2f6289)

WPUser is fast Python script specifically created to aid you in discovering all WordPress users from a provided list of websites.

## How does it work?

WP-User works by utilizing the /wp-json/wp/v2/users call!

## Install the following packages by entering

```
pip3 install requests json colorama
```

## Run the script by entering
```

python3 wpuser.py -f [list-of-wordpress-sites.txt] [threads]
```
```

python3 wpuser.py wp-domains-example.txt 20
```
## Result

https://github.com/steliospavlidis/wp-user/assets/138578903/16a35477-a366-4fb5-8e9e-6af20c3558b3

After the process ends a file found-users.txt is created in the directory. This file contains the results including the domain and the associated users.

![found](https://github.com/steliospavlidis/wp-user/assets/138578903/34245546-e640-4533-8d29-6434e1c44071)

## Notes
The script is fairly fast. I have set a timeout=10 seconds, you can change it if your targets are very slow. Also targets must reply with a HTTP status code 200.

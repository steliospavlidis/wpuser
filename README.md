# ![wpuser](https://github.com/steliospavlidis/wp-user/assets/138578903/2ca3ee00-19b6-42b7-aa8c-668e4f2f6289)

WPUser is fast Python script specifically created to aid you in discovering all WordPress users from a provided list of websites.

## How does it work?

WPUser queries the public WordPress REST API endpoint `/wp-json/wp/v2/users` and pages through all results (100 users per request), so sites with more than 10 users are fully listed.

> **⚠️ Authorized use only.** Only scan sites you own or have written permission to test. Use it to audit your own WordPress installs, for example to check whether user enumeration is exposed and should be disabled.

## Requirements

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 wpuser.py -f [list-of-wordpress-sites.txt] [threads]
```

Example:

```bash
python3 wpuser.py -f wp-domains-example.txt 20
```

The input file has one site per line. Entries without `http://` or `https://` are checked over `https://`.
## Result

https://github.com/steliospavlidis/wp-user/assets/138578903/16a35477-a366-4fb5-8e9e-6af20c3558b3

After the process ends a file found-users.txt is created in the directory. This file contains the results including the domain and the associated users.

![found](https://github.com/steliospavlidis/wp-user/assets/138578903/34245546-e640-4533-8d29-6434e1c44071)

## Notes

- The request timeout is 10 seconds. Change it in `wpuser.py` if your sites are very slow.
- Sites must reply with HTTP 200 and valid JSON to be counted.
- **Hardening tip:** if your own site shows up in the results, restrict the `users` REST endpoint to logged-in users with a security plugin or a small `rest_endpoints` filter.

## License

[MIT](LICENSE)

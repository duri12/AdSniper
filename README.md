
# AdSniper
AdSniper is  An adblocker that runs as a proxy server! (And works on HTTPS connections.)

Use this to block ads on your mobile device, or just monitor its traffic and change it ..

## Installation

1. install [Mitmproxy](https://mitmproxy.org/)
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the  requirements.

```bash
$ pip install 'Cython>=0.29.19,<1.0'  # for pyre2
$ pip install -r requirements.txt
```
3. to check if the proxy was installed properly Run ./start to start the proxy server on port 8118

4. Do a quick test to make sure it's working:
```bash
 curl --proxy localhost:8118 -L -k https://slashdot.org/
```
5. Setup your browser/phone to use localhost:8118 or lan-ip-address:8118 as an HTTP proxy server; then, visit http://mitm.it on that device to install the MITM SSL certificate so that your machine won't throw security warnings whenever the proxy server intercepts your secure connections.
## Usage
to start the program run gui_adblocker.py 

if you want to add a feature . read how to add a feature.pdf

## License
[MIT](https://choosealicense.com/licenses/mit/)

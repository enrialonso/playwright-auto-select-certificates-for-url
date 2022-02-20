# Playwright Auto Select Certificate for URL

Sometimes need load a certificate from URL to authenticate de browser or the user on a site, normally the browser opens
a popup to select the user certificate, but when make a browser automation needs select the certificates programmatically. 
To attach this on Playwright is very painful, here explain how to do this and automate the selection certificates.

<img height="200" src="doc-img/bad-ssl-ok.png"/>

Based on a docker Image for easy test on any environment

### Commands

Build Docker image: `make build`

Run Docker image: `make run`

The site for test all of this is [badssl.com](https://badssl.com)

On the file of the repository exists a correct certificate for call the test url, this certificate need to be installed 
on the docker images. this cert is selected automatically for the browser when open the [test url](https://client.badssl.com/)

To configure the auto selection certificates need add a `policies.json` file on certain folder and the browser read this 
policies on the launch and apply on every url requests. [Source](https://gist.github.com/njh/1d6f2c6acdf39fb3c1b0) - [Documentation about the policy](https://chromeenterprise.google/policies/#AutoSelectCertificateForUrls)

for chromium: `/etc/chromium/policies/managed`

```json
{
  "AutoSelectCertificateForUrls": ["{\"pattern\":\"*\",\"filter\":{}}"]
}
```

On the dockerfile install the certificate in the image with these commands

```dockerfile
# Install certificates for badssl.com
RUN pk12util -i "badssl.com-client.p12" -d "${HOME}/.pki/nssdb/" -W "badssl.com"
# Only for check on the terminal if the certificate it's installed correctly
RUN certutil -d "sql:${HOME}/.pki/nssdb" -L
```

If you run the container with the image build the output is this for a correct certificate accepted for the url:

```bash
<div id="content">
  <h1 style="font-size: 12vw;">
    client.<br>badssl.com
  </h1>
</div>

<div id="footer">
  This site requires a <a href="https://en.wikipedia.org/wiki/Transport_Layer_Security#Client-authenticated_TLS_handshake">client-authenticated</a> TLS handshake.
</div>
```

If the certificates is not installed and run the container fail on the authentication requests and the output is:

```bash
<center><h1>400 Bad Request</h1></center>
<center>No required SSL certificate was sent</center>
<hr><center>nginx/1.10.3 (Ubuntu)</center>


<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
```

### Important

This method only works if `headlees=False` and for run this on docker use the utility `Xvfb`, can't select the 
certificates on headless mode
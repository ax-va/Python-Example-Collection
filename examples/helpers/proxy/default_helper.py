from proxy.proxy_helper import set_default_proxy
from proxy.ssl_certificate_helper import set_default_ssl_certificates


def set_default_proxy_and_ssl_certificates() -> None:
    """
    Sets the default company's proxy from `.config.yaml`
    and default SSL certificates from `.ssl_certificate.pem`
    to OS environment variables.
    """
    set_default_proxy()
    set_default_ssl_certificates()

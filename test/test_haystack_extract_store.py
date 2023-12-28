from opensearch_haystack import OpenSearchDocumentStore
from haystack import Document


document_store = OpenSearchDocumentStore(hosts="http://localhost:9200", use_ssl=True,
verify_certs=False, http_auth=("admin", "admin"))

doc = {
    "paragraphs": [
        "In this article, I am describing how to SSH to a remote server as\ndiscreetly as possible, by concealing the SSH packets into SSL. The\nserver will still be able to run an SSL website.",
        "In most cases, when your outgoing firewall blocks ssh, you can work around\nwith sslh, a tool that listens\non the port 443 server-side, and selectively forwards, depending on the\npacket type, the incoming TCP connections to a local SSH or SSL service.\nYou can then happily ssh to your server on the port 443 (normally\ndedicated to HTTPS), and also run a website on the same server so your\nconnections look you are just harmlessly visiting this website. However,\nif your firewall is really sneaky, it will detect that you are sending the\nwrong packet type to the SSL port, and block your connection. In this\ncase, there is not much choice: we must hide the SSH connection into a\nreal SSL tunnel.",
        "I know, I know: I covered this topic a few times already (here are the\nfirst,\nsecond,\nand third\nepisodes). All of these setups were relying on a feature of HTTP 1.1\ncalled CONNECT. However, it turns out that most webserver do not implement\nthis CONNECT feature. As a consequence, if you wanted to do this, you were\nmore or less stuck with Apache. This time, we are breaking free from\nApache, with a HAproxy-based configuration. We will use HAproxy advanced\npacket inspection capabilities to implement a switch of protocol, the same\nway sslh works.",
        "Some assumptions:",
        "Now, you need to setup HAproxy. HAproxy defines backends and frontends, and it\ncan communicate with these backends both at the HTTP and at the TCP level. Let\nus start with the backends:",
        "The web server backend: we tell HAproxy that a server is running on the\nport 80, and speaks HTTP. On this backend, we add a X-Forwarded-Proto\nheader, such that the web server knows that the clients are connecting\nsecurely. If you expose the same backend with HAproxy on the port 80,\ndon't forget to filter the X-Forwarded-Proto header!",
        "The ssh server:",
        "And now, the magic. This happens in the frontend section. We listen in TCP mode\nand inspect the connections. Depending on whether we see ssh or not, we hook it\nto one of the backends.",
        "Once you are done, you can test if this works by connecting on the server\nwith openssl.",
        "If you see a string that looks like",
        "then everything went fine!",
        "To connect to your server from linux, just drop this in your ~/.ssh/config:",
        "If you are on windows and you cannot install anything client side, there\nis also a solution for you. Download socat and putty (none of them\nrequires admin rights). Then, with socat, run:",
        "And with putty, direct your client to 127.0.0.1 on the port 8888.",
        "So how does this work exactly? Basically, the RFC 4253, section\n4.2 states that clients\nmust send a string that starts with 'SSH-2.0' (this is also how sslh does\nit). Moreover, 5353482d322e30 is the binary representation of the string\n'SSH-2.0'. So everything boils down to this line:",
        "When a new connection is made on the port 443, HAproxy decrypts the SSL\nlayer, and checks whether the stream of data sent by the client starts\nwith this string. We use the result of this condition to choose the\nbackend. This handles the case of 'active' SSH clients (like\nopenssh-client on linux), who send a packet as soon as they connect.\nThere are also 'passive' SSH clients (like putty), who wait for the server\nto send a string. These clients will get that string after 5 seconds (the\ninspect-delay).",
        "Happy SSH!"
    ]
}

document_store.write_documents([
    Document(content=' '.join(doc.get('paragraphs')))
])

print(document_store.count_documents())
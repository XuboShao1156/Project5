<h2>Project 5: Roll Your Own CDN</h2>
<p>
<b>This project is due at 11:59pm on May 3, 2022. The milestone is due at 11:59pm on April 19, 2022. The due dates are the same for both UG and MS/PhD students.</b>
</p><p>
<h2>Description</h2>
By now, you have learned that most of the content we consume over the Interent is served 
by content delivery/distribution networks (CDNs). In this project, you will create the building 
    blocks of a CDN.  Unlike previous projects, a portion of your grade in this project will come from
how your code performs compared to the solutions of your classmates, i.e. this assignment
is a competition.
</p><p>
CDNs consist of 1) a large number of servers geographically distributed worldwide; 2) a system 
    that maps clients to "good" replica servers and 3) a system that determines those mappings. In 
    this project, you will implement the basic functionality in each of these areas. Thanks to 
    generous support from cloud servers, you will build a CDN that uses cloud sites as replica servers. Your 
    performance will be compared to two baselines: origin (a single server in a single cloud location) and 
    random server selection. You should do better than both. 
</p><p>
<!----------------->
<h2>Project Requirements</h2>
<p>
    You must implement a CDN using the following features. First, you will use DNS redirection to send clients 
    to the replica server with the fastest response time. Second, you will write a simple Web server that 
    returns content requested by clients. Third, you will implement a system that uses information about 
    network performance, load on servers, and cached data at servers to determine the best replica server.  
    Performance will be measured in terms of how long it takes to download a piece of content. Similar to 
    most Web sites, most content will be small in terms of bytes.
</p>
<p>
    I will test your code using simple clients that 1) ask your DNS server for the IP address of 
    <i>cs5700cdn.example.com</i> and 2) uses an HTTP get to fetch a file from that address. These clients 
    will run from servers located all over the world. The request frequency for each piece of content will 
    follow a <a href="http://en.wikipedia.org/wiki/Zipf's_law">Zipf distribution</a>, and the size of content at the origin server is much larger than the 
    size of your cache on each replica server. In other words, you must implement a cache replacement 
    strategy at each replica server because you can't fit all the requested content at each cache. If your replica 
    server receives a request for content not in its cache, the server must fetch it from the origin and 
    return that to the client.
</p>
<p>
    When determining the replica server to use for each client request, you should determine which one will give 
    the best time-to-completion (TTC) for downloading a Web page. This can depend on the network latency, 
    loss, available bandwidth and load on the server. You can choose any technique(s) you want for estimating 
    these properties, but online (i.e., active measurement) techniques are the most likely to suceed if implmented properly.
</p><p>
<div class="alert alert-block">
<h4><i class="icon-warning-sign"></i>Important!</h4>
This project requires you to access cloud nodes and use them as content caches. For this project, I have 
    made a large corpus of public-domain data available (i.e., Wikipedia). <b>Do not use any other content 
    in your system, particulary copyrighted work.</b> Further, you cannot use accounts on cloud for any purpose 
    other than running your replica server code. <b>If we find you using our cloud VMs for any other purpose, your account will 
    be deleted and you will receive a zero on this project.</b>
    </div>
</p>
<!----------------->
<h2>Detailed Requirements</h2>

<p>The main focus of the project is <b>HTTP cache management</b> and
  <b>DNS redirection</b>.</p> 

<p>
    For this project, you will submit: a DNS server, an HTTP server with cache management, 
    code that manages the mappings between clients and replicas, and scripts to manage deploying, running and
    stopping your CDN.
</p>

<h3>Libraries:</h3>
		
Libraries that offer the full functionality of any of the required services are prohibited. For example:
<ul>
  <li>dnslib is allowed</li>
  <li>dnspython is not</li>
</ul>
As the focus of the project is on cache management and not serving HTTP, there is an exception for Python's http.server or an equivalent in another language. Anything more fully functioned is prohibited.  
<p>
  If you have a question regarding  whether a library is permitted, <b>ask before using </b> it.
  </p>

<h3>DNS:</h3>

<p>
    The DNS server will be called using:
</p>
<pre>./dnsserver -p &lt;port&gt; -n &lt;name&gt;</pre>
<p>
    where <i>port</i> is the port number that your DNS server will bind to and <i>name</i> is the CDN-specific name 
    that your server translates to an IP.


</p>

The DNS server only needs to respond to <b>A</b>
queries for the site specified in the project description.

<h3>HTTP:</h3>
<p>
    The HTTP server will be called using: 
</p>
<pre>./httpserver -p &lt;port&gt; -o &lt;origin&gt;</pre>
<p>
    where <i>port</i> is the port that your HTTP server will bind to and <i>origin</i> is the name of the origin server for your CDN. This 
    code is responsible for delivering the requested content to clients. It may do so by fetching uncached content for the origin, or 
    a local cache of Web pages. <b>Note that the origin server is running a Web server on port 8080</b>, not 80.
</p>
Student's HTTP servers must respond to an HTTP request for <pre>/grading/beacon</pre>
with a <b>204</b> status code.

<h3>Scripts:</h3>
<p>
    Your scripts will be called as follows:
</p>
<pre>./[deploy|run|stop]CDN -p &lt;port&gt; -o &lt;origin&gt; -n &lt;name&gt; -u &lt;username&gt; -i &lt;keyfile&gt;</pre>
<p>
    where <i>port</i>, <i>origin</i> and <i>name</i> are the same as above, <i>username</i> is the account name you use for logging in and  <i>keyfile</i> is the path to the private key you use for logging into nodes.
    Your scripts should use the last two arguments as follows:
</p>
<pre>ssh -i <i>keyfile</i> <i>username</i>@&lt;some cloud server&gt; ...</pre>

<h2>Deployment Specifics</h2>

<ul>
  <li>Origin Server: HTTP on port 8080 [ssh access is not available]: <b>cs5700cdnorigin.ccs.neu.edu</b>
  </li>
    <li>Build server: <b>cs5700cdnproject.ccs.neu.edu</b> [<b>Note</b>: This is a Khoury server, so you need your Khoury login credentials here.]
    </li>
    <li>List of servers for deploying DNS: see the pinned post on <a href="https://piazza.com/class/kyc1vsrynkx2mv?cid=146">Piazza</a></b></li>
  <li> List of replicas for deploying HTTP Caches: see the pinned post on <a href="https://piazza.com/class/kyc1vsrynkx2mv?cid=146">Piazza</a></b></li>
  <li>A listing of page views for the origin server can be found on <a href="https://piazza.com/class/kyc1vsrynkx2mv?cid=146">Piazza</a></b>
  </li>
</ul>

    Disk quotas have been set such that the size of the cache on each replica server is much less than the 
size of all the requestable content. Your server is also responsible for managing the cache of Web pages on the
host where it runs. 
    Again, note that you must run this web server on the port given for testing.
</p>

<p>
    All resources are shared across all teams during testing.

    For simplicity, every team will be assigned a port number (tbd) to use for their testing. 
    The single port will be used for both the DNS serverand the HTTP replicas.
</p>
<h3>Per-user account limits on each instance:</h3>
<ul>
    <li> Max 2 Simultaneous Logins (should only have 1)</li>
    <li> Total 20MB Disk space across all folders</li>
    <li> RSS limited to 20MB [<b>Note</b>: We will not enforce this at runtime but we will check your code for limited use of in-memory caching]</li>
</ul>
<p><b>
    Submissions that use subprocess will be ineligible for TopCDN credit.
</b></p>

<!----------------->
<h2>Testing Your Code</h2>
<p>
      To test your code, you will be given an account on each of the cloud VMs described above.
      
    <b>
        Do NOT use any other server for testing.
    </b>
</p>

    The domain name querried will be <i>cs5700cdn.example.com</i>.
Your DNS servers must run on a cloud instance listed in <b>dns-hosts.txt</b>.
    You must run this server on a high-numbered port that will be given to you when you register. 
    <b>Unless you are told different, you should assume that your HTTP server will run on the same port.</b>

<p>
  
  </p>
<p>
    In addition, we will set up <i>DNS lookup beacons</i> and <i>HTTP client beacons</i> that periodically perform DNS lookups and fetch content from each VM on a range of ports.
    By instantiating a Web server on a port in that range, you will periodically receive requests for name translations and Web pages.

    You may also use Khoury servers, cloud servers and any other servers you have available to test the quality of your mappings.
</p>
<p>
    To perform a DNS lookup, use the <i>dig</i> tool. For example, you would want to call:
</p>
<pre>dig @[your DNS server IP] -p [your port]</pre>
<p>
    To fetch and time Web page downloads, you can use:
</p>
<pre>time ; wget http://[your server name]:[your port name]/[path to content]</pre>
<p>
     <i>time</i> will allow you determine how long a download takes to complete.
</p>
<p>
    Your grade will in large part depend on the time it takes to download content from the server you send my client to.
    Because you download text Web pages, you can expect the flows to be short so latency and loss are likely to dominate your performance.
    You should develop a strategy for identifying the best server for a client and test it by comparing with performance from other cloud sites.
</p>
<!----------------->
<h2>Measurement</h2>

<p>
    You may execute other measurement and mapping code on the replica servers and DNS server.

    To facilitate this, you will provide a <i>deployCDN</i>, a <i>runCDN</i> script and a <i>stopCDN</i> script.
    For example, the <i>deployCDN</i> script will copy code to an cloud instance and run a Makefile.
    The <i>runCDN</i> script will cause the server to run. 
</p>

<p>
    Note that unlike in a traditional CDN, I will be requesting name translations directly from the same host as the Web client. 
    Thus you do not have to correct for the distance between Web clients and their DNS servers.
    <b>Note that the server will be rebooted every night, so you cannot rely on long-running code on this server.</b>
</p>
<p>

</p>

<!----------------->
<h2>Tips and Tricks</h2>
<p>
    To locate the server with the lowest latency, you can use active measurements, passive measurements and/or exogenous information such IP geolocations.
    <b>
        If you choose to use active measurements, you must limit your measurement rate to no more than 1 probe per second. 
        I suggest using <a href="https://www.caida.org/catalog/software/scamper/">scamper</a>, which is already installed on the cloud machines.
    </b>
</p>
<p>
  Beware of relying on-line data via web APIs.  These servers can rate limit and cut off your access.
</p>
<p>
    You can deploy code without interactive passwords by using SSH key-based authentication. 
    You will be expected to use this technique to execute your <i>deployCDN</i> and <i>runCDN</i> scripts.
</p>
<p>
    Your CDN can be terminated at any time.
    Make sure you use persistent storage (i.e., files on disk) to maintain information about content cached at various nodes and any information you need to map clients to servers. 
</p>

<!----------------->
<h2>Grading</h2>
<p>
    Your grade in this project will be composed by the following components:
</p>
<ul>
    <li>9 points - Implementation of a DNS server that dynamically returns IP addresses based on your mapping code.</li>
    <li>9 points - Implementation of a HTTP server that efficiently fetches content from the origin on-demand and optimizes the cache hit ratio.</li>
    <li>9 points - Implementation of a system that maps IPs to nearby replica servers.</li>
    <li>5 points - Performance in the TopCDN competition</li>
    <li>3 points - A short (no more than 2 pages) report describing the design decisions you made, how your evaluated their effectiveness and what you would do with more time. Include this in the README file.</li>
</ul>
<p>
    The final competition will be held on May 5th.
    We will test each CDN against two baselines: origin and random server selection.
    Those that do better than random and origin will get 1 point.
    The top 1/3 scores will earn another 3 points (for a total of 4), and the next 1/3 will earn an additional 2 points (for a total of 3). 
    Students may use slip days and turn in the assignment late; however late assignments will not be eligible for TopCDN points. <b> All projects must be submitted by May 4th. </b>
</p>
<!----------------->
<h2>Extra Credit</h2>
<p>
The top ranked team in the TopCDN project on May 5th will earn 3 bonus points! :)
</p>
<!----------------->
<h2>Submitting Your Milestone</h2>

<p>
    The milestone is due <b>as stated above</b>.
    The milestone is to perform an early <b>'Does it run?'</b>
    evaluation of your DNS server,  a caching HTTP client, and your deployment scripts, by deploying a single DNS server and a single caching HTTP client in the cloud using your deployment scripts.  
</p>
    <p>
    For the milestone, you must submit:
</p>
<ul>
    <li>A Makefile that compiles your code</li>
    <li>httpserver source</li>
    <li>dnsserver source</li>
    <li>A deployCDN script</li>
    <li>A runCDN script</li>
    <li>A stopCDN script</li>
    <li>
        A plain-text (no Word or PDF) README file.
        In this file, you should describe:
        <ul>
            <li>In brief, your high-level approach, how you implemented your DNS and HTTP Servers, and any challenges you faced.</li>
            <li><b>(For groups) In detail, a description of which student worked on what parts of the code.</b></li>
        </ul>
    </li>
</ul>
<p>
    We will use Gradescope to handle submissions of your project code.
    You can form pairs using Gradescope's submission tools.
    <br>
    <br>
    Your README, Makefile, source code, etc. should all be placed in a directory (no subdirectories please).
    Submit your project as a zip of that directory to Gradescope.
    <b>Only one group member needs to submit your project. Remember to add your teammate when submitting.</b>
    Your group may submit as many times as you wish.
    Only the last submission will be graded, and the time of the last submission will determine whether your assignment is late.
</p>
<!----------------->
<h2>Submitting Your Final Project</h2>
<p>
    The project is due <b>as stated above</b>.
    To turn-in your final project, you must submit your (thoroughly documented) code along with three other :
</p>
<ul>
    <li>A Makefile that compiles your code</li>
    <li>httpserver source</li>
    <li>dnsserver source</li>
    <li>A deployCDN script</li>
    <li>A runCDN script</li>
    <li>A stopCDN script</li>
    <li>
        A plain-text (no Word or PDF) README file. 
        In this file, you should describe:
        <ul>
            <li>In brief, your high-level approach, how you implemented your DNS and HTTP Servers, and any challenges you faced.</li>
            <li><b>(For groups) In detail, a description of which student worked on what parts of the code.</b></li>
        </ul>
    </li>
</ul>
<p>
  Your README, Makefile, source code, etc. should all be placed in a directory (no subdirectories please). 
    Submit your project as a zip of that directory to Gradescope.
    
    <b>
        Only one group member needs to submit your project.
        Remember to add your teammate when submitting.
    </b>
    You may submit as many times as you wish; only the time of the last submission determines whether your assignment is late.
</p>

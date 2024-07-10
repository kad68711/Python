from zapv2 import ZAPv2

import time

# ZAP Proxy settings
zap_address = 'localhost'
zap_port = '8080'
zap_api_key = 'sdnrgk'  # Change to your API key, if you have set one

# Target to scan
# target_url = 'http://www.itsecgames.com/'  # Change to your target

def give_recommendations(alerts):
    vulnerability_recommendations = {
    'Cross-Site Scripting (XSS)': [
        "Sanitize user input: Filter and validate input data to remove or encode potentially malicious scripts.",
        "Use proper output encoding: Encode user-generated content before rendering it in web pages to prevent script execution."
    ],
    'SQL Injection': [
        "Use parameterized queries or prepared statements: Avoid dynamically constructing SQL queries using user input. Instead, use parameterized queries or prepared statements to separate data from SQL commands."
    ],
    'Broken Authentication': [
        "Use strong authentication mechanisms: Implement multi-factor authentication (MFA) and enforce strong password policies.",
        "Implement session management securely: Use secure session tokens, enforce session timeouts, and protect against session fixation attacks."
    ],
    'Sensitive Data Exposure': [
        "Encrypt sensitive data: Encrypt sensitive data both in transit and at rest using strong encryption algorithms.",
        "Implement access controls: Restrict access to sensitive data based on user roles and permissions."
    ],
    'XML External Entity (XXE) Injection': [
        "Disable XML external entity processing: Configure XML parsers to disable external entity processing.",
        "Validate XML input: Validate XML input against a whitelist of allowed elements and attributes to prevent XXE attacks."
    ],
    'Insecure Direct Object References (IDOR)': [
        "Implement proper access controls: Enforce access controls to ensure that users can only access resources they are authorized to access.",
        "Use indirect references: Avoid using direct object references in URLs or parameters. Instead, use indirect references mapped to internal identifiers."
    ],
    'Security Misconfiguration': [
        "Regularly update and patch software: Keep all software, including web servers, frameworks, and libraries, up to date with the latest security patches.",
        "Disable unnecessary services and features: Disable or remove unused services, ports, and functionalities to reduce the attack surface."
    ],
    'Insecure Deserialization': [
        "Use secure serialization formats: Avoid using insecure serialization formats and libraries. Prefer using safer alternatives or implementing additional controls to mitigate risks.",
        "Validate and sanitize serialized data: Validate and sanitize serialized data before deserialization to prevent object injection and other attacks."
    ],
    'Using Components with Known Vulnerabilities': [
        "Regularly update and patch components: Keep all third-party components, such as libraries and frameworks, up to date with the latest security patches.",
        "Monitor for security advisories: Stay informed about security advisories and vulnerabilities affecting the components used in your web application."
    ],
    'Insufficient Logging and Monitoring': [
        "Implement comprehensive logging: Log security-relevant events, including authentication attempts, access control failures, and potentially malicious activities.",
        "Monitor logs for suspicious activities: Use log monitoring tools to analyze and alert on suspicious activities in real-time."
    ],
    'Server-Side Request Forgery (SSRF)': [
        "Validate and restrict user-supplied URLs: Validate and restrict user-supplied URLs to prevent attackers from making unauthorized requests to internal systems."
    ],
    'Remote Code Execution (RCE)': [
        "Sanitize and validate input data: Sanitize and validate input data to prevent attackers from injecting and executing arbitrary code on the server."
    ],
    'File Upload Vulnerabilities': [
        "Validate file metadata: Check file metadata (e.g., MIME type, file extension) to ensure that uploaded files are of expected types and do not pose security risks.",
        "Store uploaded files in a secure location: Store uploaded files outside the web root directory and restrict access to uploaded files to prevent unauthorized access or execution."
    ],
    'Clickjacking': [
        "Implement frame-busting techniques: Use frame-busting JavaScript code to prevent your web pages from being embedded within frames on malicious sites.",
        "Set X-Frame-Options header: Set the X-Frame-Options header to deny framing or allow framing only from trusted domains."
    ],
    'Content Security Policy (CSP) Bypass': [
        "Implement Content Security Policy headers: Implement Content Security Policy headers to restrict the sources from which resources can be loaded, preventing XSS attacks and data exfiltration."
    ],
    'Cross-Origin Resource Sharing (CORS) Misconfiguration': [
        "Configure CORS headers properly: Configure CORS headers properly to restrict cross-origin requests and prevent unauthorized access to sensitive data."
    ],
    'Server-Side Template Injection (SSTI)': [
        "Sanitize and validate user input: Sanitize and validate user input in template files to prevent attackers from injecting and executing template code on the server."
    ],
    'Insecure Cryptographic Storage': [
        "Use strong cryptographic algorithms: Use strong cryptographic algorithms and key management practices to securely store sensitive data such as passwords and encryption keys."
    ],
    'Business Logic Vulnerabilities': [
        "Review and validate business logic: Review and validate business logic to prevent unauthorized access, tampering with data, or abuse of functionality."
    ],
    'Session Fixation': [
        "Generate new session identifiers upon login: Assign a new session identifier to the user upon successful authentication to prevent session fixation attacks.",
        "Use secure session management: Implement mechanisms such as session rotation or regeneration to invalidate old session identifiers and prevent session fixation."
    ],
    'Insufficient Transport Layer Protection': [
        "Use HTTPS: Encrypt data in transit using HTTPS to protect against eavesdropping and man-in-the-middle attacks.",
        "Implement TLS best practices: Configure TLS settings, including cipher suites, protocols, and certificate configurations, according to security best practices."
    ],
    'Cross-Site Request Forgery (CSRF)': [
        "Implement anti-CSRF tokens: Include unique tokens in forms or requests to validate the origin and integrity of submitted data.",
        "Use same-site cookie attributes: Set the SameSite attribute on cookies to prevent CSRF attacks originating from other sites."
    ],
    'Unrestricted File Upload': [
        "Validate file metadata: Check file metadata (e.g., MIME type, file extension) to ensure that uploaded files are of expected types and do not pose security risks.",
        "Store uploaded files in a secure location: Store uploaded files outside the web root directory and restrict access to uploaded files to prevent unauthorized access or execution."
    ],
    'Path Traversal (Directory Traversal)': [
        "Use whitelist-based input validation: Validate user input against a whitelist of allowed characters or patterns to prevent path traversal attacks.",
        "Implement access controls: Enforce proper access controls and file permissions to restrict access to sensitive files and directories."
    ],
    'HTTP Parameter Pollution (HPP)': [
        "Validate and sanitize input parameters: Validate and sanitize input parameters to prevent manipulation and injection of additional parameters.",
        "Use unique parameter names: Use unique parameter names to avoid conflicts and ambiguity in parameter handling."
    ],
    'Clickjacking (UI Redressing)': [
        "Implement frame-busting techniques: Use frame-busting JavaScript code to prevent your web pages from being embedded within frames on malicious sites.",
        "Set X-Frame-Options header: Set the X-Frame-Options header to deny framing or allow framing only from trusted domains."
    ],
    'Server-Side Include (SSI) Injection': [
        "Disable or sanitize SSI directives: Disable server-side includes where not needed, or sanitize user input used in SSI directives to prevent injection attacks.",
        "Use output encoding: Encode user-generated content before including it in SSI directives to prevent injection of malicious content."
    ],
    'Missing Anti-clickjacking Header': [
        "Implement anti-clickjacking defenses: Set X-Frame-Options header with 'DENY' or 'SAMEORIGIN' value to prevent clickjacking attacks.",
        "Use Content Security Policy (CSP): Implement CSP with appropriate directives to prevent clickjacking and other attacks.",
    ],
    'Content Security Policy (CSP) Header Not Set': [
        "Implement Content Security Policy (CSP): Set Content Security Policy headers with appropriate directives to mitigate various types of attacks including XSS.",
    ],
    'X-Content-Type-Options Header Missing': [
        "Set X-Content-Type-Options header: Add X-Content-Type-Options header with 'nosniff' value to prevent MIME sniffing attacks.",
    ],
    'User Agent Fuzzer': [
        "Implement request validation: Validate and sanitize user input, including user-agent strings, to prevent injection attacks and other security issues.",
    ]
}    
    # Assume 'alerts' is a list of dictionaries representing the alerts generated by your security scanning tool

    # Initialize a dictionary to store recommendations for each vulnerability
    vulnerability_recommendations_dict = {}

    for alert in alerts:
        vulnerability_name = alert['alert']  # Assuming 'vulnerability' is the key for the vulnerability name in each alert
        matched_recommendations = []
        for key in vulnerability_recommendations:
            # Check if any word in the vulnerability name matches with any word in the dictionary keys
            if any(word.lower() in vulnerability_name.lower() for word in key.split()):
                matched_recommendations.extend(vulnerability_recommendations[key])
        if matched_recommendations:
            vulnerability_recommendations_dict[vulnerability_name] = matched_recommendations

    # Print or use the collected recommendations
    print(vulnerability_recommendations_dict)
    return(vulnerability_recommendations_dict)

            



def scan_website(target_url):
    # Initialize the ZAP API
    zap = ZAPv2(apikey=zap_api_key, proxies={'http': f'http://{zap_address}:{zap_port}', 'https': f'http://{zap_address}:{zap_port}'})

    # Start a new session
    zap.core.new_session(name='newsession', overwrite=True)

    # Spider the target
    print(f'Spidering target {target_url}')
    scan_id = zap.spider.scan(target_url)
    time.sleep(2)

    # Wait for the spider to finish
    while int(zap.spider.status(scan_id)) < 100:
        print(f'Spider progress: {zap.spider.status(scan_id)}%')
        time.sleep(2)
    print('Spider completed')

    # Start the active scanner
    print(f'Scanning target {target_url}')
    scan_id = zap.ascan.scan(target_url)
    while int(zap.ascan.status(scan_id)) < 100:
        print(f'Scan progress: {zap.ascan.status(scan_id)}%')
        time.sleep(5)
    print('Scan completed')

    # Report the results
    print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    print('Alerts: ')
    alerts = zap.core.alerts(baseurl=target_url)
    for alert in alerts:
        print(f"Alert: {alert['alert']}, Risk: {alert['risk']}, URL: {alert['url']}")

    

    return [alerts,give_recommendations(alerts)]

    # Optionally, save the session
    # zap.core.save_session(name='mysession')

    # Optionally, close ZAP
    # zap.core.shutdown()
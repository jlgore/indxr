---
tags: [course-index, example, sec504]
book_number: 1
course: SEC504
---

# Book 1 Index - Example

> This is an example of what your index file might look like.
> Copy the format below for your own notes!

## Index Entries

Book 1, Page 6, Slide: "Introduction to Security" #security #basics #fundamentals
Book 1, Page 10, Slide: "Network Fundamentals" #networking #tcp-ip #OSI-model
Book 1, Page 15, Slide: "Common Vulnerabilities" #vulnerabilities #OWASP #web-security
Book 1, Page 20, Slide: "SQL Injection Attacks" #sql-injection #web-security #OWASP-top-10
Book 1, Page 25, Slide: "Cross-Site Scripting (XSS)" #xss #web-security #OWASP-top-10 #javascript
Book 1, Page 30, Slide: "Authentication Best Practices" #authentication #security #password-security
Book 1, Page 35, Slide: "Encryption Basics" #encryption #cryptography #AES #RSA
Book 1, Page 40, Slide: "Public Key Infrastructure" #PKI #certificates #cryptography
Book 1, Page 45, Slide: "Network Security Protocols" #TLS #SSL #HTTPS #protocols
Book 1, Page 50, Slide: "Firewall Configuration" #firewall #network-security #defense

## Tips for Better Indexing

- **Be Consistent**: Use the same tag names throughout (e.g., always use `#web-security`, not sometimes `#websecurity`)
- **Use Multiple Tags**: Add 3-5 relevant tags per entry for better searching
- **Tag Hierarchies**: Use hyphens for sub-topics (e.g., `#security-authentication-mfa`)
- **Common Topics**: Tag frequently tested topics like `#exam-critical` or `#important`
- **Tool Names**: Tag specific tools like `#nmap`, `#wireshark`, `#metasploit`
- **Frameworks**: Tag frameworks like `#MITRE-ATTACK`, `#OWASP`, `#NIST`

## Obsidian Power Features

### Search Your Index
- Press `Ctrl/Cmd + Shift + F` to search all your index files
- Search for specific tags: `tag:#sql-injection`
- Find all entries from a book: `"Book 1"`

### Tag Pane
- Open the tag pane (right sidebar) to see all your tags
- Click any tag to see all occurrences across all index files

### Graph View
- Open graph view to see connections between topics
- Useful for understanding topic relationships

### Dataview Queries (requires Dataview plugin)

Show all entries with a specific tag:
```dataview
LIST
FROM #web-security
WHERE contains(file.path, "Index")
```

Count entries per book:
```dataview
TABLE length(file.lists) as "Entries"
FROM "SEC504/Index"
WHERE contains(file.name, "Book")
SORT file.name
```

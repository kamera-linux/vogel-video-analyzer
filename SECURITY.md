# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## 🚨 Reporting a Vulnerability

We take the security of vogel-video-analyzer seriously. If you believe you have found a security vulnerability, please report it to us responsibly.

### Please DO NOT:
- ❌ Open a public GitHub issue for security vulnerabilities
- ❌ Disclose the vulnerability publicly before we've had a chance to address it

### Please DO:
- ✅ Report vulnerabilities via [GitHub Security Advisories](https://github.com/kamera-linux/vogel-video-analyzer/security/advisories/new)
- ✅ Alternatively, open a private discussion or issue marked as security-related
- ✅ Provide detailed information about the vulnerability
- ✅ Give us reasonable time to address the issue before public disclosure

## 📋 What to Include in Your Report

Please include as much of the following information as possible:

1. **Type of vulnerability** (e.g., code injection, path traversal, etc.)
2. **Affected version(s)** of vogel-video-analyzer
3. **Step-by-step instructions** to reproduce the issue
4. **Proof of concept** or exploit code (if available)
5. **Potential impact** of the vulnerability
6. **Suggested fix** (if you have one)

## 🔄 Response Process

1. **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
2. **Investigation**: We will investigate and validate the reported vulnerability
3. **Fix Development**: If confirmed, we will develop a fix
4. **Release**: We will release a patch version as soon as possible
5. **Disclosure**: After the fix is released, we will publish a security advisory

## ⏱️ Expected Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Release**: Depends on severity and complexity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium/Low: Within 30 days

## 🛡️ Security Best Practices for Users

### When Using vogel-video-analyzer:

1. **Keep Updated**: Always use the latest version
   ```bash
   pip install --upgrade vogel-video-analyzer
   ```

2. **Validate Input**: Be cautious with video files from untrusted sources
   - Malicious video files could potentially exploit vulnerabilities in OpenCV or other dependencies

3. **Model Files**: Only use YOLOv8 model files from trusted sources
   - The default model search includes the user's home directory
   - Ensure model files haven't been tampered with

4. **File Permissions**: Be aware of file operations
   - The `--delete` flag will remove video files
   - The `--output` flag will create/overwrite files
   - Run with appropriate user permissions

5. **Dependency Security**: Keep dependencies updated
   ```bash
   pip install --upgrade opencv-python ultralytics numpy
   ```

## 🔍 Known Security Considerations

### Current Design:

1. **File System Access**: The tool reads video files and can optionally delete them
   - Users should be careful with the `--delete` flag
   - Ensure proper file permissions

2. **Model Loading**: YOLOv8 models are loaded from disk
   - Models from untrusted sources could be malicious
   - Use models from official Ultralytics sources

3. **Video Processing**: OpenCV processes video files
   - Vulnerabilities in OpenCV could affect this tool
   - We rely on OpenCV's security updates

4. **Python Dependencies**: Multiple third-party dependencies
   - Keep all dependencies updated
   - Monitor security advisories for dependencies

## 📚 Security Resources

- [OpenCV Security](https://opencv.org/)
- [Ultralytics YOLOv8 Security](https://github.com/ultralytics/ultralytics/security)
- [Python Security](https://www.python.org/news/security/)
- [NumPy Security](https://numpy.org/doc/stable/release.html)

## 🏆 Security Hall of Fame

We would like to thank the following individuals for responsibly disclosing security issues:

<!-- Names will be added here with permission from reporters -->

*No security issues have been reported yet.*

## 📞 Contact

For security-related questions or concerns:
- **GitHub Security Advisories**: [Report a vulnerability](https://github.com/kamera-linux/vogel-video-analyzer/security/advisories/new)
- **GitHub Issues**: [Open an issue](https://github.com/kamera-linux/vogel-video-analyzer/issues) (for non-sensitive security questions)
- **GitHub Discussions**: [Start a discussion](https://github.com/kamera-linux/vogel-video-analyzer/discussions) (for general security topics)

---

**Thank you for helping keep vogel-video-analyzer and its users safe!**

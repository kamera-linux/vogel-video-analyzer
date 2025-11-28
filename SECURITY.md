# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.4.x   | :white_check_mark: |
| 0.3.x   | :white_check_mark: |
| 0.2.x   | :x:                |
| < 0.2   | :x:                |

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

3. **Model Files**: Only use models from trusted sources
   - YOLOv8 models from Ultralytics
   - Hugging Face models from verified publishers (e.g., kamera-linux/german-bird-classifier)
   - Ensure model files haven't been tampered with

4. **File Permissions**: Be aware of file operations
   - The `--delete-file` and `--delete-folder` flags will remove files/folders
   - The `--annotate-video` creates new video files in the same directory
   - The `--output` flag will create/overwrite files
   - Run with appropriate user permissions

5. **Dependency Security**: Keep dependencies updated
   ```bash
   pip install --upgrade vogel-video-analyzer
   ```

6. **Audio Processing (v0.3.0+)**: ffmpeg is used for audio preservation
   - Ensure ffmpeg is from official sources
   - Keep ffmpeg updated for security patches

7. **Unicode Text Rendering (v0.3.0+)**: PIL/Pillow is used for text rendering
   - Vulnerabilities in Pillow could affect video annotation
   - Keep Pillow updated

## 🔍 Known Security Considerations

### Current Design:

1. **File System Access**: The tool reads video files and can optionally delete them
   - Users should be careful with the `--delete-file` and `--delete-folder` flags
   - Annotated videos are created in the same directory as source files
   - Ensure proper file permissions

2. **Model Loading**: Models are loaded from disk or Hugging Face
   - YOLOv8 models from untrusted sources could be malicious
   - Hugging Face transformers models are cached locally
   - Use models from official/verified sources only

3. **Video Processing**: OpenCV processes video files
   - Vulnerabilities in OpenCV could affect this tool
   - We rely on OpenCV's security updates
   - Video annotation writes new video files with ffmpeg

4. **External Processes (v0.3.0+)**: ffmpeg is called via subprocess
   - Ensure ffmpeg binary is from official sources
   - Path traversal vulnerabilities are mitigated by using absolute paths
   - Audio streams are merged from original videos

5. **Python Dependencies**: Multiple third-party dependencies
   - opencv-python, ultralytics, numpy, PIL/Pillow
   - transformers, torch (optional, for species identification)
   - ffmpeg (system dependency)
   - Keep all dependencies updated
   - Monitor security advisories for dependencies

6. **Unicode Input (v0.3.0+)**: Handles multilingual text
   - German umlauts (ä, ö, ü, ß)
   - Special characters from species names
   - Input validation in place

## 📚 Security Resources

- [OpenCV Security](https://opencv.org/)
- [Ultralytics YOLOv8 Security](https://github.com/ultralytics/ultralytics/security)
- [Python Security](https://www.python.org/news/security/)
- [NumPy Security](https://numpy.org/doc/stable/release.html)
- [Pillow Security](https://pillow.readthedocs.io/en/stable/releasenotes/index.html)
- [Hugging Face Security](https://huggingface.co/docs/hub/security)
- [ffmpeg Security](https://ffmpeg.org/security.html)

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

# Contributing to Vogel Video Analyzer

Thank you for your interest in contributing to vogel-video-analyzer! 🎉

We welcome contributions from the community and appreciate your effort to make this project better.

## 🌟 Ways to Contribute

- 🐛 **Report Bugs**: Submit detailed bug reports via [GitHub Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)
- 💡 **Suggest Features**: Share ideas for new features or improvements
- 📝 **Improve Documentation**: Help make our docs clearer and more comprehensive
- 🔧 **Submit Code**: Fix bugs or implement new features
- 🧪 **Write Tests**: Improve test coverage
- 🌍 **Translations**: Help translate documentation (future)

## 📋 Getting Started

### 1. Fork the Repository

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/vogel-video-analyzer.git
   cd vogel-video-analyzer
   ```

### 2. Set Up Development Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (if available)
# pre-commit install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 💻 Development Guidelines

### Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

Example:
```python
def analyze_video(
    video_path: str,
    sample_rate: int = 1,
    confidence_threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Analyze a video file for bird content.
    
    Args:
        video_path: Path to the video file
        sample_rate: Process every Nth frame (default: 1)
        confidence_threshold: Minimum detection confidence (default: 0.5)
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        FileNotFoundError: If video file doesn't exist
        ValueError: If sample_rate is less than 1
    """
    # Implementation here
    pass
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for good test coverage

```bash
# Run tests (when test suite is available)
pytest

# Run tests with coverage
pytest --cov=vogel_video_analyzer
```

### Documentation

- Update README.md if you change user-facing features
- Update docstrings for code changes
- Add comments for complex logic
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/)

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)
- [ ] Commit messages are clear and descriptive

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add support for AVI video format"
git commit -m "Fix detection threshold not being applied"
git commit -m "Update documentation for --sample-rate flag"

# Not so good
git commit -m "fix bug"
git commit -m "updates"
```

### Submitting the Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request on GitHub

3. Fill out the PR template with:
   - Clear description of changes
   - Related issue numbers (if applicable)
   - Screenshots/examples (if relevant)
   - Testing performed

4. Wait for review and address feedback

### PR Review Process

- Maintainers will review your PR
- You may be asked to make changes
- Once approved, a maintainer will merge your PR
- Your contribution will be included in the next release

## 🐛 Reporting Bugs

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps
- **Expected vs Actual Behavior**: What should happen vs what does happen
- **Environment**: OS, Python version, package version
- **Video Information**: Format, codec, resolution (if relevant)
- **Error Output**: Full error messages and tracebacks
- **Additional Context**: Logs, screenshots, etc.

Use our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)

## 💡 Suggesting Features

When suggesting features, please include:

- **Problem/Use Case**: What problem does it solve?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other solutions considered
- **Benefits**: Who would benefit and how?
- **Examples**: Code examples or mockups

Use our [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)

## 🔒 Security Issues

**Do not** report security vulnerabilities through public GitHub issues.

Please report them via:
- [GitHub Security Advisories](https://github.com/kamera-linux/vogel-video-analyzer/security/advisories/new)
- See [SECURITY.md](SECURITY.md) for details

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Any conduct inappropriate in a professional setting

## ❓ Questions?

- 💬 [GitHub Discussions](https://github.com/kamera-linux/vogel-video-analyzer/discussions)
- 📝 [Open an Issue](https://github.com/kamera-linux/vogel-video-analyzer/issues)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute!

---

**Happy Coding! 🐦💻**

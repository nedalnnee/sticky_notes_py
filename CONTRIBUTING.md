# Contributing to Sticky Notes 📌

Thank you for considering contributing to Sticky Notes! We welcome bug reports, feature suggestions, and pull requests to help improve the project.

---

## 🛠️ Development Setup

1. **Fork and Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sticky_notes.cmd.git
   cd sticky_notes
   ```

2. **Create a Virtual Environment**:
   Using `uv` (recommended):
   ```bash
   uv venv
   uv pip install --python .venv pyqt6 pillow pyinstaller
   ```
   Or standard Python `venv`:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r pyproject.toml
   ```

3. **Run Locally**:
   ```bash
   .venv\Scripts\python -m src.main
   ```

---

## 🚀 Creating Pull Requests

1. **Branch Naming**: Use descriptive branch names like `feature/custom-fonts` or `fix/tray-icon-click`.
2. **Code Style**: Follow PEP 8 guidelines for Python code style.
3. **Commit Messages**: Keep commit messages concise and clear (e.g. `feat: add font size selector to title bar`).
4. **Testing**: Test your changes both in direct Python execution and by building the executable (`python build.py`).

---

## 📄 License Agreement

By contributing to this repository, you agree that your contributions will be licensed under the project's **PolyForm Noncommercial License 1.0.0** (free for personal/non-commercial use, strictly non-for-sale).

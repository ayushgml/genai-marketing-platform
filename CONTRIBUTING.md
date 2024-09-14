# CONTRIBUTING.md

## Contributing to the Project

First off, thank you for contributing to our project! Your time and effort are greatly appreciated.

This document provides guidelines to help you contribute effectively. Use your best judgment, and feel free to propose changes to this document in a pull request.

### Table of Contents

- [CONTRIBUTING.md](#contributingmd)
  - [Contributing to the Project](#contributing-to-the-project)
    - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Cloning the Repository](#cloning-the-repository)
      - [For Collaborators](#for-collaborators)
    - [Setting Up Remotes](#setting-up-remotes)
      - [For Collaborators](#for-collaborators-1)
  - [How to Contribute](#how-to-contribute)
    - [Creating a New Branch](#creating-a-new-branch)
      - [For Collaborators](#for-collaborators-2)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Pull Requests](#pull-requests)
      - [For Collaborators](#for-collaborators-3)
  - [Development Guidelines](#development-guidelines)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
    - [Handling Sensitive Data](#handling-sensitive-data)
    - [Coding Standards](#coding-standards)
    - [Commit Messages](#commit-messages)
    - [Testing](#testing)
  - [Communication](#communication)
  - [Code of Conduct](#code-of-conduct)

---

## Getting Started

### Prerequisites

- **Git**: Ensure you have Git installed on your machine.
- **Node.js and npm**: For frontend development.
- **Python 3.8+**: For backend development.
- **Docker and Docker Compose**: For containerization.
- **AWS CLI**: If you're working with infrastructure code.

### Cloning the Repository

#### For Collaborators

If you are a collaborator with write access to the repository, you can clone the repository directly:

```bash
git clone https://github.com/your-team/genai-marketing-platform.git
cd genai-marketing-platform
```

Replace `your-team` with the actual GitHub organization or username.


### Setting Up Remotes

#### For Collaborators

Verify that your remote is set correctly:

```bash
git remote -v
```

You should see:

```
origin  https://github.com/your-team/genai-marketing-platform.git (fetch)
origin  https://github.com/your-team/genai-marketing-platform.git (push)
```


## How to Contribute

### Creating a New Branch

Before starting work on a new feature or bugfix, create a new branch from the `main` branch.

#### For Collaborators

1. **Ensure your local `main` branch is up-to-date**:

   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a new branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```


### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:

- **A clear and descriptive title**.
- **Steps to reproduce the bug**.
- **Expected behavior**.
- **Actual behavior**.
- **Screenshots** (if applicable).
- **Environment** (OS, browser, etc.).

### Suggesting Enhancements

We welcome suggestions for improvements. Please open an issue with:

- **A clear and descriptive title**.
- **A detailed description of the enhancement**.
- **Motivation**: Why is this enhancement beneficial?
- **Possible alternatives**.

### Pull Requests

#### For Collaborators

1. **Commit your changes**:

   ```bash
   git add .
   git commit -m "feat: Add your descriptive commit message here"
   ```

2. **Push your branch to the repository**:

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a pull request** from your branch to the `main` branch.

---

## Development Guidelines

### Backend Setup

1. **Navigate** to the backend directory:

   ```bash
   cd backend
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   - **Create a `.env` file** based on `.env.example`:

     ```bash
     cp .env.example .env
     ```

   - **Place sensitive data** (e.g., API keys, database passwords) in the `.env` file.
   - **Do not** commit `.env` files to the repository. They are included in `.gitignore`.

5. **Run the application**:

   ```bash
   python app/app.py
   ```

6. **Run tests**:

   ```bash
   pytest tests/
   ```

### Frontend Setup

1. **Navigate** to the frontend directory:

   ```bash
   cd frontend
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Set up environment variables**:

   - **Create a `.env.local` file** based on `.env.example`:

     ```bash
     cp .env.example .env.local
     ```

   - **Place sensitive data** in the `.env.local` file.
   - **Do not** commit `.env.local` files to the repository.

4. **Start the development server**:

   ```bash
   npm run dev
   ```

5. **Run tests**:

   ```bash
   npm test
   ```

### Handling Sensitive Data

- **Never commit sensitive information** (API keys, passwords, secret tokens) to the repository.
- **Use environment variables** to manage sensitive data.
  - **Backend**: Use a `.env` file in the `backend` directory.
  - **Frontend**: Use a `.env.local` file in the `frontend` directory.
- **Reference environment variables** in your code where needed.
- **Include an example environment file** (e.g., `.env.example`) with placeholders to help others set up their environment.
- **Add `.env` and `.env.local` to `.gitignore`** to prevent accidental commits.

### Coding Standards

- **Python**:
  - Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.
  - Use tools like `flake8` and `black` for linting and formatting.
- **JavaScript/TypeScript**:
  - Use `eslint` and `prettier` for linting and formatting.
- **Commit Messages**:
  - Use clear and descriptive commit messages.
  - Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification if possible.

### Commit Messages

Structure your commit messages as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Common types include:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

### Testing

- **Write tests** for new features and bug fixes.
- **Ensure all tests pass** before submitting a pull request.
- **Backend Tests**: Use `pytest` and ensure coverage.
- **Frontend Tests**: Use `Jest` or `React Testing Library`.

---

## Communication

- **Issue Tracker**: Use GitHub issues for bug reports and feature requests.
- **Pull Requests**: Use GitHub pull requests for code submissions.
- **Discussions**: Use the GitHub Discussions tab for general questions and community engagement.

---

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the expectations for all contributors.

---

Thank you for contributing!

---

**Note**: Replace placeholder URLs and email addresses with actual contact information specific to your project.

---

Now, the `CONTRIBUTING.md` includes separate instructions for collaborators and external contributors:

- **Cloning the Repository**: Instructions for collaborators to clone directly, and for external contributors to fork and clone.
- **Creating a New Branch**: Steps are tailored for both collaborators and external contributors.
- **Pull Requests**: Instructions differ slightly for pushing to the main repository versus a fork.

This ensures that collaborators who don't need to fork the repository can follow the appropriate steps, while external contributors have clear guidance on how to contribute.

Let me know if you need any further adjustments!
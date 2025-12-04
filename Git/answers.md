# Git & Version Control: Answers

## Git Basics

**1. What is Git and how does it differ from other version control systems?**

Git is a **distributed version control system (DVCS)** created by Linus Torvalds in 2005. Unlike centralized VCS (CVS, SVN), Git gives every developer a full copy of the repository history.

**Key differences from centralized VCS:**
- **Distributed**: Every clone is a full backup
- **Fast**: Most operations are local (no network needed)
- **Branching**: Lightweight branches, easy merging
- **Data integrity**: SHA-1 hashing for all content
- **Staging area**: Review changes before committing

```bash
# Centralized VCS (SVN)
# Single server, developers check out working copies
svn checkout http://server/repo

# Distributed VCS (Git)
# Full repository cloned locally
git clone https://github.com/user/repo.git
```

---

**2. What is the difference between Git and GitHub?**

| Git | GitHub |
|-----|--------|
| Version control software | Hosting service for Git repositories |
| Command-line tool | Web-based platform |
| Runs locally | Cloud-based |
| Open source | Owned by Microsoft |
| Manages code history | Adds collaboration features |

**GitHub adds:**
- Pull Requests
- Issues tracking
- Actions (CI/CD)
- Project boards
- Code review tools
- Wikis and documentation

**Alternatives to GitHub:** GitLab, Bitbucket, Azure DevOps

---

**3. How do you initialize a new Git repository?**

```bash
# Initialize in current directory
git init

# Initialize in specific directory
git init my-project

# Initialize with specific branch name
git init -b main

# Clone existing repository
git clone https://github.com/user/repo.git

# Clone to specific directory
git clone https://github.com/user/repo.git my-folder

# Clone specific branch
git clone -b develop https://github.com/user/repo.git
```

After initialization:
```bash
# Add remote (for new local repos)
git remote add origin https://github.com/user/repo.git

# First commit
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

**4. What is the staging area in Git and why is it important?**

The **staging area** (or index) is an intermediate area where commits are prepared. It sits between the working directory and repository.

```
Working Directory → Staging Area → Repository
     (edit)          (git add)    (git commit)
```

**Why it's important:**
1. **Selective commits**: Stage specific files or parts of files
2. **Review changes**: Inspect what will be committed
3. **Atomic commits**: Group related changes together
4. **Undo capability**: Unstage before committing

```bash
# Add to staging
git add file.txt           # Single file
git add .                  # All changes
git add *.js               # Pattern matching
git add -p file.txt        # Interactive (partial staging)

# Check staging status
git status
git diff --staged          # View staged changes

# Unstage
git reset HEAD file.txt    # Unstage file
git reset HEAD             # Unstage all
```

---

**5. Explain the basic Git workflow: working directory, staging area, and repository.**

```
┌─────────────────┐     git add     ┌─────────────────┐    git commit    ┌─────────────────┐
│                 │ ───────────────>│                 │ ────────────────>│                 │
│    Working      │                 │    Staging      │                  │   Repository    │
│    Directory    │ <───────────────│    Area         │ <────────────────│   (.git)        │
│                 │   git checkout  │                 │    git reset     │                 │
└─────────────────┘                 └─────────────────┘                  └─────────────────┘
```

**Working Directory**: Your actual files that you edit
**Staging Area**: Prepared snapshot for next commit
**Repository**: Complete history of all commits

**Typical workflow:**
```bash
# 1. Make changes in working directory
echo "new content" >> file.txt

# 2. Stage changes
git add file.txt

# 3. Commit to repository
git commit -m "Add new content"

# 4. Push to remote (optional)
git push origin main
```

---

**6. How do you check the status of your Git repository?**

```bash
# Full status
git status

# Short format
git status -s
# Output:
# M  modified-staged.txt    (staged)
#  M modified-unstaged.txt  (not staged)
# ?? untracked.txt          (untracked)
# A  new-staged.txt         (new, staged)

# Show branch info
git status -sb

# Ignored files too
git status --ignored
```

**Status indicators (short format):**
- `M` = Modified
- `A` = Added (new file)
- `D` = Deleted
- `R` = Renamed
- `??` = Untracked

---

**7. What is the difference between `git add .` and `git add -A`?**

```bash
# git add . - Add changes in current directory and subdirectories
# Does NOT add deletions in older Git versions (< 2.0)
git add .

# git add -A (or --all) - Add ALL changes (including deletions)
# Works from repo root regardless of current directory
git add -A

# git add -u - Add modified and deleted (NOT new files)
git add -u
```

**In Git 2.0+:** `git add .` and `git add -A` behave the same when run from repo root.

**Best practice:**
```bash
# Stage all changes explicitly
git add -A

# Or be specific
git add src/
git add *.js
```

---

**8. How do you view the commit history in Git?**

```bash
# Basic log
git log

# One line per commit
git log --oneline

# With graph (branches)
git log --oneline --graph --all

# Last n commits
git log -5

# By author
git log --author="John"

# By date range
git log --since="2024-01-01" --until="2024-12-31"

# By file
git log -- path/to/file.txt

# Search commit messages
git log --grep="fix bug"

# Show changes in each commit
git log -p

# Show stats
git log --stat

# Pretty format
git log --pretty=format:"%h %s (%an, %ar)"
```

---

## Branching and Merging

**9. What is a branch in Git and why are branches important?**

A **branch** is a lightweight pointer to a commit. It represents an independent line of development.

**Why branches are important:**
1. **Isolation**: Work on features without affecting main code
2. **Parallel development**: Multiple features simultaneously
3. **Experimentation**: Try ideas safely
4. **Code review**: Review before merging to main
5. **Release management**: Maintain stable versions

```bash
# Create branch
git branch feature-login

# Switch to branch
git checkout feature-login
# or (Git 2.23+)
git switch feature-login

# Create and switch
git checkout -b feature-login
# or
git switch -c feature-login

# List branches
git branch          # Local
git branch -r       # Remote
git branch -a       # All
```

---

**10. How do you create and switch to a new branch?**

```bash
# Method 1: Two commands
git branch new-feature
git checkout new-feature

# Method 2: Single command (traditional)
git checkout -b new-feature

# Method 3: Modern syntax (Git 2.23+)
git switch -c new-feature

# Create from specific commit
git checkout -b hotfix abc123

# Create from remote branch
git checkout -b feature origin/feature

# Switch to existing branch
git checkout main
git switch main
```

---

**11. What is the difference between `git merge` and `git rebase`?**

**Merge**: Creates a merge commit joining two histories
```bash
# On feature branch, merge main
git checkout feature
git merge main

# History:
#     A---B---C feature
#    /         \
#   D---E---F---G main (merge commit)
```

**Rebase**: Moves commits to a new base
```bash
# On feature branch, rebase onto main
git checkout feature
git rebase main

# History:
#             A'--B'--C' feature
#            /
#   D---E---F main
```

| Aspect | Merge | Rebase |
|--------|-------|--------|
| History | Preserves all history | Linear history |
| Merge commit | Yes | No |
| Conflicts | Resolve once | Resolve per commit |
| Public branches | Safe | **Never rebase public** |
| Feature branches | OK | Preferred |

**Golden rule**: Never rebase commits that have been pushed to public branches.

---

**12. What is a fast-forward merge?**

A **fast-forward merge** occurs when the target branch hasn't diverged. Git simply moves the pointer forward.

```bash
# Before (main hasn't changed since feature branched)
#   D---E main
#        \
#         A---B---C feature

# After fast-forward merge
git checkout main
git merge feature

#   D---E---A---B---C main, feature
```

**Force a merge commit (no fast-forward):**
```bash
git merge --no-ff feature

#   D---E-----------M main (merge commit)
#        \         /
#         A---B---C feature
```

---

**13. What is HEAD in Git?**

**HEAD** is a pointer to the current commit/branch you're working on.

```bash
# HEAD typically points to a branch
cat .git/HEAD
# ref: refs/heads/main

# See what HEAD points to
git rev-parse HEAD          # Full SHA
git log -1 HEAD             # Current commit

# HEAD shortcuts
HEAD^    # Parent of HEAD (1 commit back)
HEAD~1   # Same as HEAD^
HEAD~3   # 3 commits back
HEAD@{1} # Previous position of HEAD (reflog)
```

**Detached HEAD**: When HEAD points directly to a commit (not a branch):
```bash
git checkout abc123  # Now in detached HEAD state
```

---

**14. How do you delete a local and remote branch?**

```bash
# Delete local branch (must not be on it)
git branch -d feature      # Safe delete (merged only)
git branch -D feature      # Force delete

# Delete remote branch
git push origin --delete feature
# or
git push origin :feature

# Clean up local tracking of deleted remote branches
git fetch --prune
# or
git remote prune origin

# Delete all merged local branches
git branch --merged | grep -v "main" | xargs git branch -d
```

---

**15. What is a detached HEAD state and how do you get out of it?**

**Detached HEAD** means HEAD points to a commit directly, not a branch. Changes made here can be lost if you switch away.

```bash
# Causes of detached HEAD
git checkout abc123         # Checkout specific commit
git checkout v1.0           # Checkout tag
git checkout origin/main    # Checkout remote branch

# Signs you're in detached HEAD
git status
# HEAD detached at abc123

# Option 1: Create a branch to save work
git checkout -b save-my-work

# Option 2: Return to a branch (lose uncommitted changes)
git checkout main

# Option 3: If you made commits, save them
git branch temp-branch      # Save commits
git checkout main
git merge temp-branch       # Merge if needed
```

---

## Git Workflow

**16. Explain the Git Flow workflow.**

**Git Flow** is a branching model with specific branch types:

```
┌──────────────────────────────────────────────────────────────┐
│  main (production)    ───●─────────●─────────●───────────→   │
│                          ↑         ↑         ↑               │
│  hotfix               ───┴────●────┘         │               │
│                                              │               │
│  release              ─────────────●────●────┘               │
│                                    ↑                         │
│  develop              ───●────●────┴────●────●────●───────→  │
│                          ↑                   ↑               │
│  feature              ───┴────●────●─────────┘               │
└──────────────────────────────────────────────────────────────┘
```

**Branches:**
- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/***: New features
- **release/***: Prepare releases
- **hotfix/***: Production bug fixes

```bash
# Start feature
git checkout develop
git checkout -b feature/login

# Finish feature
git checkout develop
git merge feature/login
git branch -d feature/login

# Start release
git checkout develop
git checkout -b release/1.0

# Finish release
git checkout main
git merge release/1.0
git tag v1.0
git checkout develop
git merge release/1.0
```

---

**17. What is a feature branch workflow?**

A simpler workflow where each feature gets its own branch from main.

```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/user-auth

# 2. Work on feature
git add .
git commit -m "Add login functionality"

# 3. Push feature branch
git push -u origin feature/user-auth

# 4. Create Pull Request (on GitHub/GitLab)

# 5. After review, merge to main
git checkout main
git merge feature/user-auth
git push origin main

# 6. Clean up
git branch -d feature/user-auth
git push origin --delete feature/user-auth
```

**Benefits:**
- Simple to understand
- Clean main branch
- Easy code review via PRs
- Works well for small teams

---

**18. What are the best practices for writing commit messages?**

**Format:**
```
<type>: <subject> (max 50 chars)

<body> (optional, wrap at 72 chars)

<footer> (optional, references, breaking changes)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Good examples:**
```bash
feat: Add user authentication system

Implement JWT-based authentication with refresh tokens.
Includes login, logout, and password reset functionality.

Closes #123

---

fix: Resolve memory leak in image cache

The cache was not properly releasing references to disposed
images. Added weak references and cleanup on dispose.

---

docs: Update API documentation for v2 endpoints
```

**Bad examples:**
```bash
# Too vague
"fix stuff"
"update"
"WIP"

# Too long
"Add new feature that does this and that and also..."
```

---

**19. What is trunk-based development?**

**Trunk-based development** is a workflow where all developers commit to a single branch (trunk/main) frequently.

**Key principles:**
1. Short-lived feature branches (< 2 days)
2. Frequent integration to main
3. Feature flags for incomplete features
4. High test coverage
5. Continuous integration

```bash
# Developer workflow
git checkout main
git pull
git checkout -b short-feature  # Very short-lived

# Work, commit frequently
git commit -m "Part 1 of feature"
git push

# Merge quickly (same day or next)
git checkout main
git merge short-feature
git push
git branch -d short-feature
```

**Benefits:**
- Reduces merge conflicts
- Faster feedback
- Always releasable main
- Simpler than Git Flow

---

**20. How do you squash commits and why would you do it?**

**Squashing** combines multiple commits into one.

**Why squash:**
- Clean up messy commit history
- Combine "WIP" commits
- One logical change = one commit
- Required by some projects

```bash
# Method 1: Interactive rebase
git rebase -i HEAD~3  # Last 3 commits

# In editor, change 'pick' to 'squash' (or 's')
pick abc123 Add feature
squash def456 Fix typo
squash ghi789 More fixes

# Save, then edit combined commit message

# Method 2: Squash merge
git checkout main
git merge --squash feature-branch
git commit -m "Add complete feature"

# Method 3: Soft reset and recommit
git reset --soft HEAD~3
git commit -m "Combined commit message"
```

---

## Advanced Operations

**21. When should you use rebase instead of merge?**

**Use rebase when:**
- Updating feature branch with latest main
- Cleaning up local commits before push
- Maintaining linear history
- Working on private branches

```bash
# Update feature branch with latest main
git checkout feature
git rebase main
```

**Use merge when:**
- Integrating feature into main
- Working on public/shared branches
- Preserving complete history
- Avoiding rewriting shared commits

```bash
# Merge feature into main
git checkout main
git merge feature
```

**Never rebase:**
- Public/shared branches
- After pushing to remote
- main/master/develop branches

---

**22. What is cherry-picking and when would you use it?**

**Cherry-pick** copies a specific commit to another branch.

```bash
# Copy commit to current branch
git cherry-pick abc123

# Copy multiple commits
git cherry-pick abc123 def456

# Copy range of commits
git cherry-pick abc123^..def456

# Without committing (stage only)
git cherry-pick --no-commit abc123

# Abort if conflicts
git cherry-pick --abort
```

**Use cases:**
1. **Hotfix**: Apply bug fix from develop to main
2. **Selective merge**: Only want specific commits
3. **Recover work**: Get commits from deleted branch
4. **Backport**: Apply fix to older release

```bash
# Example: Hotfix from develop to main
git checkout main
git cherry-pick abc123  # The fix commit from develop
git push origin main
```

---

**23. What is git stash and when would you use it?**

**Stash** temporarily saves uncommitted changes.

```bash
# Save current changes
git stash

# Save with message
git stash push -m "Work in progress on login"

# List stashes
git stash list
# stash@{0}: On feature: Work in progress on login
# stash@{1}: WIP on main: abc123 Previous work

# Apply most recent stash (keep in stash list)
git stash apply

# Apply and remove from stash list
git stash pop

# Apply specific stash
git stash apply stash@{1}

# Show stash contents
git stash show -p stash@{0}

# Delete stash
git stash drop stash@{0}

# Clear all stashes
git stash clear

# Stash including untracked files
git stash -u

# Stash including ignored files
git stash -a
```

**Use cases:**
- Need to switch branches urgently
- Pull changes when you have local modifications
- Test something quickly on clean state

---

**24. What is the difference between `git reset --soft`, `git reset --mixed`, and `git reset --hard`?**

```bash
# --soft: Move HEAD only (keeps staging and working dir)
git reset --soft HEAD~1
# Commits undone, changes staged, ready to recommit

# --mixed: Move HEAD + reset staging (default)
git reset --mixed HEAD~1
# or just
git reset HEAD~1
# Commits undone, changes unstaged but in working dir

# --hard: Move HEAD + reset staging + reset working dir
git reset --hard HEAD~1
# ⚠️ DANGEROUS: All changes lost!
```

| Reset Type | HEAD | Staging Area | Working Dir |
|------------|------|--------------|-------------|
| --soft | Moved | Unchanged | Unchanged |
| --mixed | Moved | Reset | Unchanged |
| --hard | Moved | Reset | Reset |

```bash
# Common uses
git reset --soft HEAD~1   # Undo commit, keep changes staged
git reset HEAD file.txt   # Unstage a file
git reset --hard HEAD     # Discard all uncommitted changes
git reset --hard origin/main  # Reset to remote state
```

---

**25. What is the difference between `git reset` and `git revert`?**

**Reset**: Moves HEAD backward, rewrites history
**Revert**: Creates new commit that undoes changes

```bash
# Reset - removes commits (rewrites history)
git reset --hard HEAD~2
# History: A-B-C becomes A

# Revert - keeps history, adds undo commit
git revert HEAD
# History: A-B-C becomes A-B-C-D (D undoes C)
```

| Aspect | Reset | Revert |
|--------|-------|--------|
| History | Rewrites | Preserves |
| Creates commit | No | Yes |
| Public branches | ❌ Dangerous | ✅ Safe |
| Can undo | Hard | Easy |
| Collaboration | Problematic | Safe |

**Rule**: Use `revert` for public branches, `reset` for local only.

---

**26. How do you amend the last commit?**

```bash
# Amend commit message only
git commit --amend -m "New message"

# Amend with editor
git commit --amend

# Add forgotten files to last commit
git add forgotten-file.txt
git commit --amend --no-edit

# Change author
git commit --amend --author="Name <email@example.com>"

# Amend without changing message
git commit --amend --no-edit
```

**Warning**: Don't amend pushed commits (rewrites history).

```bash
# If you need to fix a pushed commit, use revert instead
git revert HEAD
```

---

**27. What is interactive rebase and what can you do with it?**

**Interactive rebase** (`git rebase -i`) lets you modify commits.

```bash
git rebase -i HEAD~4  # Last 4 commits
```

**In the editor:**
```
pick abc123 Add feature
pick def456 Fix typo
pick ghi789 Update docs
pick jkl012 Add tests
```

**Commands:**
- `pick` (p): Use commit as-is
- `reword` (r): Edit commit message
- `edit` (e): Stop to amend commit
- `squash` (s): Combine with previous
- `fixup` (f): Squash, discard message
- `drop` (d): Delete commit
- `exec` (x): Run shell command

**Examples:**
```bash
# Reorder commits (change line order)
pick ghi789 Update docs
pick abc123 Add feature

# Squash commits
pick abc123 Add feature
squash def456 Fix typo

# Edit old commit
pick abc123 Add feature
edit def456 Change this one
pick ghi789 Continue

# After edit, when stopped:
# Make changes...
git add .
git commit --amend
git rebase --continue
```

---

**28. How do you undo a pushed commit?**

```bash
# Method 1: Revert (safe, preserves history)
git revert HEAD              # Revert last commit
git revert abc123            # Revert specific commit
git push origin main

# Method 2: Revert multiple commits
git revert HEAD~3..HEAD      # Revert last 3 commits
git push

# Method 3: Force push (⚠️ dangerous for shared branches)
git reset --hard HEAD~1
git push --force origin main

# Safer force push (fails if others pushed)
git push --force-with-lease origin main
```

**Best practice**: Always use `revert` for shared branches.

---

## Collaboration and Remote Repositories

**29. What is the difference between `git fetch` and `git pull`?**

```bash
# Fetch: Download remote changes, don't merge
git fetch origin
# Remote tracking branches updated, working dir unchanged

# Pull: Fetch + Merge
git pull origin main
# Equivalent to:
git fetch origin
git merge origin/main

# Pull with rebase
git pull --rebase origin main
# Equivalent to:
git fetch origin
git rebase origin/main
```

| Aspect | Fetch | Pull |
|--------|-------|------|
| Downloads changes | Yes | Yes |
| Merges automatically | No | Yes |
| Modifies working dir | No | Yes |
| Safe | Always | Can cause conflicts |
| Review first | Yes | No |

**Best practice**: Fetch first, review, then merge manually.

---

**30. How do you set up and manage multiple remote repositories?**

```bash
# List remotes
git remote -v

# Add remote
git remote add origin https://github.com/user/repo.git
git remote add upstream https://github.com/original/repo.git

# Rename remote
git remote rename origin github

# Change remote URL
git remote set-url origin git@github.com:user/repo.git

# Remove remote
git remote remove upstream

# Fetch from all remotes
git fetch --all

# Push to specific remote
git push origin main
git push upstream main

# Pull from specific remote
git pull upstream main
```

**Common setup for forks:**
```bash
# origin = your fork
git remote add origin https://github.com/you/repo.git

# upstream = original repo
git remote add upstream https://github.com/original/repo.git

# Keep fork updated
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

**31. What are Pull Requests (or Merge Requests) and what is their purpose?**

**Pull Request (PR)** / **Merge Request (MR)** is a request to merge one branch into another, with:
- Code review
- Discussion
- CI/CD checks
- Approval workflow

**Purpose:**
1. **Code review**: Team reviews changes before merge
2. **Discussion**: Comment on specific lines
3. **Quality gates**: Automated tests, linting
4. **Documentation**: Record of why changes were made
5. **Collaboration**: Multiple reviewers, suggestions

**Workflow:**
```bash
# 1. Create feature branch
git checkout -b feature/awesome

# 2. Make changes and push
git add .
git commit -m "Add awesome feature"
git push -u origin feature/awesome

# 3. Create PR on GitHub/GitLab (web interface)

# 4. Address review comments
git add .
git commit -m "Address review feedback"
git push

# 5. After approval, merge (web or CLI)
```

---

**32. What are the best practices for code reviews?**

**For authors:**
1. Keep PRs small (< 400 lines)
2. Write clear description
3. Self-review before requesting
4. Respond to feedback promptly
5. Test locally first

**For reviewers:**
1. Be constructive and respectful
2. Focus on logic, not style
3. Ask questions, don't demand
4. Approve explicitly
5. Review within 24 hours

**What to review:**
- [ ] Logic correctness
- [ ] Edge cases handled
- [ ] Error handling
- [ ] Security concerns
- [ ] Performance implications
- [ ] Tests included
- [ ] Documentation updated

**Good feedback example:**
```
"Could we consider using a Map here for O(1) lookup
instead of iterating through the array? This might
improve performance when the list grows."
```

---

**33. How do you resolve merge conflicts?**

```bash
# When conflict occurs:
git merge feature
# CONFLICT (content): Merge conflict in file.txt

# 1. Check conflicted files
git status

# 2. Open file and resolve manually
<<<<<<< HEAD
current branch content
=======
incoming branch content
>>>>>>> feature

# 3. Choose content (remove markers)
final resolved content

# 4. Mark as resolved
git add file.txt

# 5. Complete merge
git commit
# or for rebase:
git rebase --continue

# Abort if needed
git merge --abort
git rebase --abort
```

**Using merge tools:**
```bash
# Configure merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Launch merge tool
git mergetool
```

**Prevention tips:**
- Pull frequently
- Keep branches short-lived
- Communicate with team
- Use consistent formatting

---

## Git Configuration and Tools

**34. What is a .gitignore file and how do you use it?**

**.gitignore** specifies files/patterns Git should not track.

```gitignore
# Ignore single file
secrets.json

# Ignore by extension
*.log
*.tmp

# Ignore directory
node_modules/
build/
.dart_tool/

# Ignore pattern
*.local.*

# Negate pattern (don't ignore)
!important.log

# Ignore in specific directory
/root-only-file.txt
docs/*.pdf

# Ignore everywhere
**/debug.log

# Comments
# This is a comment
```

**Common patterns for Flutter:**
```gitignore
# Flutter/Dart
.dart_tool/
.packages
build/
.flutter-plugins
.flutter-plugins-dependencies

# IDE
.idea/
*.iml
.vscode/

# macOS
.DS_Store

# Android
/android/app/debug
/android/app/profile
/android/app/release

# iOS
/ios/Flutter/Flutter.framework
/ios/Flutter/Flutter.podspec
/ios/Pods/
```

```bash
# Force add ignored file
git add -f file.txt

# Check why file is ignored
git check-ignore -v file.txt

# Global gitignore
git config --global core.excludesfile ~/.gitignore_global
```

---

**35. What is the difference between lightweight tags and annotated tags?**

```bash
# Lightweight tag: Just a pointer (like a branch that doesn't move)
git tag v1.0

# Annotated tag: Full object with metadata
git tag -a v1.0 -m "Release version 1.0"

# View tags
git tag
git show v1.0

# Tag specific commit
git tag -a v1.0 abc123 -m "Release 1.0"

# Push tags
git push origin v1.0     # Single tag
git push origin --tags   # All tags

# Delete tag
git tag -d v1.0                    # Local
git push origin --delete v1.0     # Remote
```

| Aspect | Lightweight | Annotated |
|--------|-------------|-----------|
| Metadata | No | Yes (author, date, message) |
| Checksummed | No | Yes (SHA) |
| Signing | No | Can be GPG signed |
| Use case | Temporary | Releases |

**Best practice**: Use annotated tags for releases.

---

**36. What are Git hooks and give examples of when you would use them?**

**Git hooks** are scripts that run automatically on certain events.

Location: `.git/hooks/` (local) or configured path (shared)

```bash
# Common hooks
pre-commit      # Before commit created
commit-msg      # Validate commit message
pre-push        # Before push
post-merge      # After merge
pre-rebase      # Before rebase
```

**Example: Pre-commit hook** (`.git/hooks/pre-commit`)
```bash
#!/bin/sh
# Run tests before allowing commit
flutter test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

# Run formatter
dart format --set-exit-if-changed .
if [ $? -ne 0 ]; then
    echo "Please format your code. Commit aborted."
    exit 1
fi
```

**Example: commit-msg hook**
```bash
#!/bin/sh
# Enforce conventional commits
if ! grep -qE "^(feat|fix|docs|style|refactor|test|chore):" "$1"; then
    echo "Invalid commit message format"
    echo "Use: type: message"
    exit 1
fi
```

**Tools for shared hooks:**
- Husky (npm)
- pre-commit (Python)
- lefthook (Go)

---

**37. How do you create Git aliases to speed up your workflow?**

```bash
# Set alias
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

# Now use: git co, git br, git ci, git st

# Complex aliases
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# Log formatting
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.hist "log --pretty=format:'%h %ad | %s%d [%an]' --date=short"

# Useful aliases
git config --global alias.amend 'commit --amend --no-edit'
git config --global alias.undo 'reset --soft HEAD~1'
git config --global alias.stash-all 'stash save --include-untracked'
```

**In ~/.gitconfig:**
```ini
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    lg = log --oneline --graph --all
    undo = reset --soft HEAD~1
    amend = commit --amend --no-edit
```

---

## Platform Features and Troubleshooting

**38. What are some important GitHub/GitLab features for team collaboration?**

**GitHub Features:**
- **Pull Requests**: Code review, discussions
- **Issues**: Bug tracking, feature requests
- **Projects**: Kanban boards
- **Actions**: CI/CD pipelines
- **Wiki**: Documentation
- **Discussions**: Community forum
- **Code owners**: Auto-assign reviewers
- **Branch protection**: Require reviews, checks

**GitLab Features:**
- **Merge Requests**: Code review
- **Issues + Boards**: Project management
- **CI/CD**: Built-in pipelines
- **Container Registry**: Docker images
- **Wiki**: Documentation
- **Snippets**: Code sharing

**Branch Protection Rules:**
```
main branch:
  ✓ Require pull request reviews (2 approvals)
  ✓ Require status checks (CI must pass)
  ✓ Require linear history
  ✓ Include administrators
```

---

**39. What are common Git mistakes and how do you fix them?**

```bash
# Mistake 1: Committed to wrong branch
git reset --soft HEAD~1        # Undo commit
git stash                      # Save changes
git checkout correct-branch
git stash pop                  # Apply changes
git commit

# Mistake 2: Forgot to add file to commit
git add forgotten-file.txt
git commit --amend --no-edit

# Mistake 3: Wrong commit message
git commit --amend -m "Correct message"

# Mistake 4: Accidentally deleted branch
git reflog                     # Find commit
git checkout -b recovered-branch abc123

# Mistake 5: Committed sensitive data
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch secrets.txt" \
  --prune-empty --tag-name-filter cat -- --all
# Or use BFG Repo Cleaner (faster)

# Mistake 6: Messed up rebase
git rebase --abort             # During rebase
git reflog                     # After rebase
git reset --hard HEAD@{5}      # Go back to before rebase

# Mistake 7: Need to undo multiple commits
git revert HEAD~3..HEAD        # Revert last 3

# Mistake 8: Lost uncommitted changes
# If staged, might be in .git/objects
git fsck --lost-found
```

---

**40. How do you handle large files in Git repositories?**

**Problems with large files:**
- Slow clones
- Large repository size
- Memory issues

**Solutions:**

**1. Git LFS (Large File Storage)**
```bash
# Install LFS
git lfs install

# Track file types
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "assets/**"

# Check tracked patterns
cat .gitattributes

# Migrate existing files
git lfs migrate import --include="*.psd"

# Check LFS files
git lfs ls-files
```

**2. .gitignore large files**
```gitignore
*.zip
*.tar.gz
videos/
large-assets/
```

**3. Git archive for distribution**
```bash
git archive --format=zip HEAD > release.zip
```

**4. Shallow clone**
```bash
# Clone with limited history
git clone --depth 1 https://github.com/repo.git

# Clone single branch
git clone --single-branch --branch main https://github.com/repo.git
```

**5. Clean up repository**
```bash
# Find large files
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  sort -k3 -n -r | head -20

# Remove from history (BFG Repo Cleaner)
bfg --delete-files "*.zip" repo.git
```

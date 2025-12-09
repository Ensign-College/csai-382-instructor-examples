# Databricks notebook source
# COMMAND ----------
%md
# GitHub + Databricks Repos: Live Setup Demo

**Learning objectives**
- Understand how GitHub Classroom repositories work.
- Connect Databricks to GitHub and clone a repo into Repos.
- Organize project files into `notebooks/`, `sql/`, `etl_pipeline/`, `data_samples/`.
- Write a simple README in Markdown.
- Use AI helpers in an honest and ethical way.

👩‍🏫 Instructor tip: Run each cell and narrate the bullet points in simple sentences.

# COMMAND ----------
%md
## Quick Context: GitHub Classroom Repos

When a student **accepts** a GitHub Classroom assignment:
- A **personal repo** is created inside the teacher’s GitHub organization.
- The repo name often looks like `csai-382-pipeline-<username>`.
- This repo is where all course notebooks and ETL code will live.

Example file tree that might appear after cloning:
```text
csai-382-pipeline-username/
├── notebooks/
├── sql/
├── etl_pipeline/
├── data_samples/
└── README.md
```

👩‍🏫 Instructor tip: Show the actual GitHub Classroom invitation page in the browser so students see the "Accept" flow.

# COMMAND ----------
%sh
# Optional: Inspect the current folder to see if this notebook already lives in a Repo.
pwd
ls

# If you see a path with /Repos/ above, this notebook is inside a Git-backed folder.
# If you do NOT see /Repos/, you can still run the demo, but later open this notebook from inside a Repo for the full experience.

# COMMAND ----------
%md
## Databricks Repos Concept

**What is a Databricks Repo?**
- A Databricks Repo links a Git repository (like GitHub) to a folder in the workspace.
- It keeps your notebooks and files in sync with Git commits.
- For this class, we use **Repos** so code stays versioned and shareable.

**How to connect your Classroom repo**
- In the left sidebar, click **Repos → Add Repo**.
- Choose **GitHub**, authorize if prompted.
- Select your Classroom repo (after you accepted the assignment).
- The repo appears under **Repos** with your GitHub username.

**Common errors**
- Not accepting the Classroom assignment first (repo does not exist yet).
- Using the wrong GitHub account to authorize Databricks.
- Expecting the repo to show up under **Workspace** instead of **Repos**.

# COMMAND ----------
# Python cell: Show the notebook path programmatically.
context = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
print("Notebook path:", context.notebookPath().get())
print("Workspace URL:", context.browserHostName().get())

path_note = "Inside a Git-backed Repo" if "/Repos/" in context.notebookPath().get() else "Not inside a Repo yet"
print("Repo status:", path_note)
print("If you see /Repos/<username>/<repo-name>, you are in the Git-backed folder.")
print("If not, remind students their real class repo will live under /Repos.")

# COMMAND ----------
%md
## Required Folder Structure

Every Classroom repo should include:
```text
├── notebooks/
├── sql/
├── etl_pipeline/
├── data_samples/
└── README.md
```
- `notebooks/` → Where we keep Databricks or Jupyter notebooks.
- `sql/` → Standalone SQL query files.
- `etl_pipeline/` → Python scripts or workflow files that run the ETL automatically.
- `data_samples/` → Small example CSV or JSON files for testing.
- `README.md` → Project description and instructions.

**Ask students:**
- Which folder should we put a SQL transformation script in?
- Where do we save small sample CSV files?

# COMMAND ----------
# Optional: Create demo folders in DBFS to visualize the structure.
# This is just a demo in /tmp. Real project files will live in your Git-backed Repo under /Repos.

base_path = "/tmp/demo_pipeline"
dbutils.fs.mkdirs(f"{base_path}/notebooks")
dbutils.fs.mkdirs(f"{base_path}/sql")
dbutils.fs.mkdirs(f"{base_path}/etl_pipeline")
dbutils.fs.mkdirs(f"{base_path}/data_samples")

print("Created demo folders in DBFS (temporary):")
dbutils.fs.ls(base_path)

# COMMAND ----------
%md
## README.md and Markdown Basics

- A README explains **what the project does** and **how to run it**.
- It uses **Markdown**, a simple text format for headings, lists, and code blocks.

Here is a short template you can copy:
```markdown
# Project Title
One-sentence purpose of the project.

## Folders
- notebooks/ : Notebooks you run in class.
- sql/ : SQL query files.
- etl_pipeline/ : Scripts or jobs that move/clean data.
- data_samples/ : Small CSV or JSON files for quick tests.

## How to run this project
1. Open the notebooks in Databricks from the notebooks/ folder.
2. Run cells in order; adjust paths if needed.
3. Commit and push your changes so the instructor can see them.
```

👩‍🏫 Instructor tip: Show how to edit README.md directly in Databricks or in GitHub’s web editor.

# COMMAND ----------
# Sample README content you can copy into your repo.
sample_readme = """# STEDI Balance Data Pipeline\n\nThis project builds a small data pipeline for STEDI balance data.\n\n## Folders\n- notebooks/: Databricks notebooks for data exploration.\n- sql/: SQL scripts for transformations.\n- etl_pipeline/: Python jobs or workflow files to run the pipeline.\n- data_samples/: Small CSV files for testing locally.\n\n## How to run this project\n1. Open the notebooks/ folder and run the notebooks in order.\n2. Use the sql/ scripts inside Databricks SQL or `%sql` cells.\n3. Update etl_pipeline/ scripts if you automate the pipeline.\n4. Commit and push changes so GitHub stays in sync.\n"""

print(sample_readme)

# COMMAND ----------
%md
## How Changes Go from Databricks to GitHub

Basic Git flow inside Databricks Repos:
- Edit a notebook or file in the Repo.
- In the Repos sidebar, check **Pending changes**.
- Write a short commit message (example: "Add README and folder notes").
- Click **Commit & Push** to send updates to GitHub.

ASCII diagram:
```text
Edit in Databricks -> Commit -> Push -> GitHub updated
```

**Common problems**
- Forgetting to commit, so the teacher cannot see updates.
- Working in a non-Repo folder (changes are not tracked by Git).

# COMMAND ----------
%sh
# Optional Git commands demo. Safe to run even if not in a repo.
git status || echo "Not in a git repo"
git remote -v || echo "No git remote configured"

# COMMAND ----------
%md
## Using AI Helpers the Right Way

- AI can suggest README text, commands, or code examples.
- Always read and understand AI output before using it.
- Do not submit AI-generated work that you cannot explain.
- In this class, AI is a **tutor**, not a "do the assignment for me" button.
- Cite or mention AI help when it influenced your work.
- If unsure, ask the instructor before relying on AI suggestions.

**Discussion questions**
- Is it okay if AI writes my README if I really understand every line?
- What could go wrong if I copy AI commands I do not understand when working with Git or data pipelines?
- How can we use AI in a way that builds trust and skills?

# COMMAND ----------
%md
## Quick Recap and Checklist

Use this checklist for the real assignment:
- [ ] I have accepted my GitHub Classroom assignment.
- [ ] I connected my GitHub account to Databricks Repos.
- [ ] I cloned the Classroom repo into Databricks Repos.
- [ ] My repo contains `notebooks/`, `sql/`, `etl_pipeline/`, `data_samples/`, and `README.md`.
- [ ] I wrote or edited `README.md` in simple, clear English.
- [ ] I committed and pushed my changes to GitHub.
- [ ] I used any AI help in an honest way and understand my own work.

👩‍🏫 Instructor closing line: *“If you can check all of these boxes, your pipeline repository is ready for the rest of the course.”*

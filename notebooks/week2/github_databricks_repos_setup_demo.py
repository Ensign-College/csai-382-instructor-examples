# Databricks notebook source
# MAGIC %md
# MAGIC # GitHub + Databricks Repos: Live Setup Demo
# MAGIC
# MAGIC **Learning objectives**
# MAGIC - Understand how GitHub Classroom repositories work.
# MAGIC - Connect Databricks to GitHub and clone a repo into Repos.
# MAGIC - Organize project files into `notebooks/`, `sql/`, `etl_pipeline/`, `data_samples/`.
# MAGIC - Write a simple README in Markdown.
# MAGIC - Use AI helpers in an honest and ethical way.
# MAGIC
# MAGIC 👩‍🏫 Instructor tip: Run each cell and narrate the bullet points in simple sentences.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Quick Context: GitHub Classroom Repos
# MAGIC
# MAGIC When a student **accepts** a GitHub Classroom assignment:
# MAGIC - A **personal repo** is created inside the teacher’s GitHub organization.
# MAGIC - The repo name often looks like `csai-382-pipeline-<username>`.
# MAGIC - This repo is where all course notebooks and ETL code will live.
# MAGIC
# MAGIC Example file tree that might appear after cloning:
# MAGIC ```text
# MAGIC csai-382-pipeline-username/
# MAGIC ├── notebooks/
# MAGIC ├── sql/
# MAGIC ├── etl_pipeline/
# MAGIC ├── data_samples/
# MAGIC └── README.md
# MAGIC ```
# MAGIC
# MAGIC 👩‍🏫 Instructor tip: Show the actual GitHub Classroom invitation page in the browser so students see the "Accept" flow.

# COMMAND ----------

# MAGIC %sh
# MAGIC # Optional: Inspect the current folder to see if this notebook already lives in a Repo.
# MAGIC pwd
# MAGIC ls
# MAGIC
# MAGIC # If you see a path with /Repos/ above, this notebook is inside a Git-backed folder.
# MAGIC # If you do NOT see /Repos/, you can still run the demo, but later open this notebook from inside a Repo for the full experience.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Databricks Repos Concept
# MAGIC
# MAGIC **What is a Databricks Repo?**
# MAGIC - A Databricks Repo links a Git repository (like GitHub) to a folder in the workspace.
# MAGIC - It keeps your notebooks and files in sync with Git commits.
# MAGIC - For this class, we use **Repos** so code stays versioned and shareable.
# MAGIC
# MAGIC **How to connect your Classroom repo**
# MAGIC - In the left sidebar, click **Repos → Add Repo**.
# MAGIC - Choose **GitHub**, authorize if prompted.
# MAGIC - Select your Classroom repo (after you accepted the assignment).
# MAGIC - The repo appears under **Repos** with your GitHub username.
# MAGIC
# MAGIC **Common errors**
# MAGIC - Not accepting the Classroom assignment first (repo does not exist yet).
# MAGIC - Using the wrong GitHub account to authorize Databricks.
# MAGIC - Expecting the repo to show up under **Workspace** instead of **Repos**.

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

# MAGIC %md
# MAGIC ## Required Folder Structure
# MAGIC
# MAGIC Every Classroom repo should include:
# MAGIC ```text
# MAGIC ├── notebooks/
# MAGIC ├── sql/
# MAGIC ├── etl_pipeline/
# MAGIC ├── data_samples/
# MAGIC └── README.md
# MAGIC ```
# MAGIC - `notebooks/` → Where we keep Databricks or Jupyter notebooks.
# MAGIC - `sql/` → Standalone SQL query files.
# MAGIC - `etl_pipeline/` → Python scripts or workflow files that run the ETL automatically.
# MAGIC - `data_samples/` → Small example CSV or JSON files for testing.
# MAGIC - `README.md` → Project description and instructions.
# MAGIC
# MAGIC **Ask students:**
# MAGIC - Which folder should we put a SQL transformation script in?
# MAGIC - Where do we save small sample CSV files?

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

# MAGIC %md
# MAGIC ## README.md and Markdown Basics
# MAGIC
# MAGIC - A README explains **what the project does** and **how to run it**.
# MAGIC - It uses **Markdown**, a simple text format for headings, lists, and code blocks.
# MAGIC
# MAGIC Here is a short template you can copy:
# MAGIC ```markdown
# MAGIC # Project Title
# MAGIC One-sentence purpose of the project.
# MAGIC
# MAGIC ## Folders
# MAGIC - notebooks/ : Notebooks you run in class.
# MAGIC - sql/ : SQL query files.
# MAGIC - etl_pipeline/ : Scripts or jobs that move/clean data.
# MAGIC - data_samples/ : Small CSV or JSON files for quick tests.
# MAGIC
# MAGIC ## How to run this project
# MAGIC 1. Open the notebooks in Databricks from the notebooks/ folder.
# MAGIC 2. Run cells in order; adjust paths if needed.
# MAGIC 3. Commit and push your changes so the instructor can see them.
# MAGIC ```
# MAGIC
# MAGIC 👩‍🏫 Instructor tip: Show how to edit README.md directly in Databricks or in GitHub’s web editor.

# COMMAND ----------

# Sample README content you can copy into your repo.
sample_readme = """# STEDI Balance Data Pipeline\n\nThis project builds a small data pipeline for STEDI balance data.\n\n## Folders\n- notebooks/: Databricks notebooks for data exploration.\n- sql/: SQL scripts for transformations.\n- etl_pipeline/: Python jobs or workflow files to run the pipeline.\n- data_samples/: Small CSV files for testing locally.\n\n## How to run this project\n1. Open the notebooks/ folder and run the notebooks in order.\n2. Use the sql/ scripts inside Databricks SQL or `%sql` cells.\n3. Update etl_pipeline/ scripts if you automate the pipeline.\n4. Commit and push changes so GitHub stays in sync.\n"""

print(sample_readme)

# COMMAND ----------

# MAGIC %md
# MAGIC ## How Changes Go from Databricks to GitHub
# MAGIC
# MAGIC Basic Git flow inside Databricks Repos:
# MAGIC - Edit a notebook or file in the Repo.
# MAGIC - In the Repos sidebar, check **Pending changes**.
# MAGIC - Write a short commit message (example: "Add README and folder notes").
# MAGIC - Click **Commit & Push** to send updates to GitHub.
# MAGIC
# MAGIC ASCII diagram:
# MAGIC ```text
# MAGIC Edit in Databricks -> Commit -> Push -> GitHub updated
# MAGIC ```
# MAGIC
# MAGIC **Common problems**
# MAGIC - Forgetting to commit, so the teacher cannot see updates.
# MAGIC - Working in a non-Repo folder (changes are not tracked by Git).

# COMMAND ----------

# MAGIC %sh
# MAGIC # Optional Git commands demo. Safe to run even if not in a repo.
# MAGIC git status || echo "Not in a git repo"
# MAGIC git remote -v || echo "No git remote configured"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Using AI Helpers the Right Way
# MAGIC
# MAGIC - AI can suggest README text, commands, or code examples.
# MAGIC - Always read and understand AI output before using it.
# MAGIC - Do not submit AI-generated work that you cannot explain.
# MAGIC - In this class, AI is a **tutor**, not a "do the assignment for me" button.
# MAGIC - Cite or mention AI help when it influenced your work.
# MAGIC - If unsure, ask the instructor before relying on AI suggestions.
# MAGIC
# MAGIC **Discussion questions**
# MAGIC - Is it okay if AI writes my README if I really understand every line?
# MAGIC - What could go wrong if I copy AI commands I do not understand when working with Git or data pipelines?
# MAGIC - How can we use AI in a way that builds trust and skills?

# COMMAND ----------

# MAGIC %md
# MAGIC ## Quick Recap and Checklist
# MAGIC
# MAGIC Use this checklist for the real assignment:
# MAGIC - [ ] I have accepted my GitHub Classroom assignment.
# MAGIC - [ ] I connected my GitHub account to Databricks Repos.
# MAGIC - [ ] I cloned the Classroom repo into Databricks Repos.
# MAGIC - [ ] My repo contains `notebooks/`, `sql/`, `etl_pipeline/`, `data_samples/`, and `README.md`.
# MAGIC - [ ] I wrote or edited `README.md` in simple, clear English.
# MAGIC - [ ] I committed and pushed my changes to GitHub.
# MAGIC - [ ] I used any AI help in an honest way and understand my own work.
# MAGIC
# MAGIC 👩‍🏫 Instructor closing line: *“If you can check all of these boxes, your pipeline repository is ready for the rest of the course.”*

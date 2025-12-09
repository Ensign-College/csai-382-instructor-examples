# Databricks notebook source
# MAGIC %md
# MAGIC # Instructor Demo: Automated ETL Pipelines for STEDI (Assignment 3.3)
# MAGIC 
# MAGIC **Goal:** Guide students through turning their Assignment 3.2 work into a clean, automated ETL notebook and a Databricks Job that rewrites the curated table `labeled_step_test`. We will also practice SQL validation of labels.
# MAGIC 
# MAGIC **Learning Objectives**
# MAGIC - Understand the difference between an exploratory *student notebook* and a production-ready *automated ETL notebook*.
# MAGIC - See how a Databricks Job runs a notebook automatically and rewrites a curated table.
# MAGIC - Practice validating the curated table with SQL queries.
# MAGIC 
# MAGIC **Small and Simple (Spiritual Thought)**
# MAGIC - Alma 37:6 teaches that "by small and simple things are great things brought to pass." Daily ETL jobs may feel small, but consistent automation keeps data healthy, just like small daily spiritual habits keep us strong.
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ### Note about AI usage
# MAGIC - Databricks includes AI/code assistants that can suggest code.
# MAGIC - Students may use AI as a helper, but they must **understand and verify** the code they submit.
# MAGIC - AI can be wrong. Part of your skill is noticing and correcting mistakes.
# MAGIC 
# MAGIC ---
# MAGIC 
# MAGIC ## What is an Automated ETL Notebook?
# MAGIC ETL stands for **Extract, Transform, Load**.
# MAGIC - **Extract:** Read raw data (e.g., STEDI device messages, step test results).
# MAGIC - **Transform:** Clean, filter, join, and add labels.
# MAGIC - **Load:** Write the curated table to the lakehouse.
# MAGIC 
# MAGIC **Exploratory/Student notebook:**
# MAGIC - Many cells, tests, and visualizations.
# MAGIC - Messy like a home kitchen while cooking.
# MAGIC 
# MAGIC **Clean ETL notebook:**
# MAGIC - Few cells, clear steps, and reusable.
# MAGIC - Like a restaurant kitchen: clean stations, same recipe every time.
# MAGIC 
# MAGIC **Instructor Tip:** Invite students to imagine two kitchens: a messy home kitchen when experimenting, and a restaurant kitchen that follows the recipe exactly. Automated notebooks are the restaurant kitchen.
# COMMAND ----------
# MAGIC %md
# MAGIC ## Setup – Using an Existing Curated DataFrame
# MAGIC In Assignment 3.2, students created a curated DataFrame called `final_df` by joining and cleaning STEDI data. For the live demo, we simulate a small `final_df` with a few rows.
# MAGIC 
# MAGIC **Reminder:** In the real student notebook, `final_df` comes from their ETL steps (joins, cleaning, labeling). Here we create a tiny example so the notebook is self-contained.
# COMMAND ----------
# Import PySpark functions
from pyspark.sql import functions as F

# Simulated curated DataFrame from Assignment 3.2
sample_data = [
    ("CUST-001", "DEV-101", "step", "device"),
    ("CUST-002", "DEV-102", "no_step", "step"),
    ("CUST-003", "DEV-103", "step", "device"),
    ("CUST-004", "DEV-104", "no_step", "step"),
]

final_df = spark.createDataFrame(
    sample_data,
    ["customer", "device_id", "step_label", "source_label"]
)

# Show the simulated data
final_df.show()
# COMMAND ----------
# MAGIC %md
# MAGIC ## Writing the Curated Table (SQL) – Key Pattern
# MAGIC The **final cell** of the automated ETL notebook should overwrite the curated table. Use `CREATE OR REPLACE` so each run refreshes the table.
# MAGIC 
# MAGIC ```sql
# MAGIC CREATE OR REPLACE TABLE labeled_step_test AS
# MAGIC SELECT * FROM final_df;
# MAGIC ```
# MAGIC 
# MAGIC **Instructor Tip:** Common mistakes:
# MAGIC - Typo in the table name (`labeled_step_test`).
# MAGIC - Using a different DataFrame name instead of `final_df`.
# MAGIC - Forgetting to run this cell before validating.
# COMMAND ----------
%sql
-- Overwrite curated table from the final DataFrame
CREATE OR REPLACE TABLE labeled_step_test AS
SELECT * FROM final_df;
# COMMAND ----------
# MAGIC %md
# MAGIC ## Validating the Pipeline with SQL Queries
# MAGIC After the job runs, use SQL checks to confirm labels and counts. Run these in order and interpret the results out loud.
# COMMAND ----------
%sql
-- 1) Steps vs. No-Steps count
SELECT step_label, COUNT(*)
FROM labeled_step_test
GROUP BY step_label;
# COMMAND ----------
# MAGIC %md
# MAGIC **Good result:** Only `step` and `no_step` rows with realistic counts.
# MAGIC 
# MAGIC **Bad result:** Missing labels, spelling issues, or extra categories indicate problems in the labeling logic.
# COMMAND ----------
%sql
-- 2) Invalid or missing step labels
SELECT *
FROM labeled_step_test
WHERE step_label NOT IN ('step', 'no_step')
   OR step_label IS NULL
LIMIT 50;
# COMMAND ----------
# MAGIC %md
# MAGIC **Good result:** Zero rows returned.
# MAGIC 
# MAGIC **Bad result:** Any rows here suggest a join problem, typo, or missing labeling rule.
# MAGIC 
# MAGIC **Discussion Question:** If you see NULL `step_label`, which step in your ETL might be broken?
# COMMAND ----------
%sql
-- 3) Source label counts
SELECT source_label, COUNT(*)
FROM labeled_step_test
GROUP BY source_label;
# COMMAND ----------
# MAGIC %md
# MAGIC **Good result:** Only `device` and `step` categories appear.
# MAGIC 
# MAGIC **Bad result:** Extra labels or NULLs may indicate incorrect joins or case-sensitive spelling errors.
# MAGIC 
# MAGIC **Discussion Question:** If you see unexpected labels, what might have happened to your source data or mapping?
# COMMAND ----------
%sql
-- 4) Invalid source labels
SELECT *
FROM labeled_step_test
WHERE source_label NOT IN ('device', 'step')
   OR source_label IS NULL
LIMIT 50;
# COMMAND ----------
# MAGIC %md
# MAGIC **Good result:** Zero rows.
# MAGIC 
# MAGIC **Bad result:** Investigate missing joins, wrong column names, or unhandled label values.
# MAGIC 
# MAGIC **Discussion Question:** How would you track down where an invalid label was created?
# COMMAND ----------
# MAGIC %md
# MAGIC ## Common Troubleshooting Patterns
# MAGIC Use this quick checklist when validations fail:
# MAGIC - ✅ Did the notebook actually rewrite the table? Re-run the `CREATE OR REPLACE` cell.
# MAGIC - ✅ Did the join create duplicates or missing rows? Compare counts before and after joins.
# MAGIC - ✅ Are labels spelled correctly (case-sensitive)? Use `DISTINCT` to see unique values.
# MAGIC - ✅ Are there NULL labels? Look for missing join keys or filters.
# MAGIC 
# MAGIC **Mini examples**
# MAGIC - Check row counts before and after a join (example placeholder):
# MAGIC 
# MAGIC ```python
# MAGIC before_count = df_steps.count()
# MAGIC after_count = df_steps.join(df_labels, "device_id", "left").count()
# MAGIC print(before_count, after_count)
# MAGIC ```
# MAGIC 
# MAGIC - View all distinct step labels:
# MAGIC ```sql
# MAGIC SELECT DISTINCT step_label FROM labeled_step_test;
# MAGIC ```
# MAGIC 
# MAGIC - Quick NULL check:
# MAGIC ```sql
# MAGIC SELECT COUNT(*) AS null_steps
# MAGIC FROM labeled_step_test
# MAGIC WHERE step_label IS NULL;
# MAGIC ```
# COMMAND ----------
# MAGIC %md
# MAGIC ## Example “Clean ETL” Structure (Template)
# MAGIC Use this template when students refactor their Assignment 3.2 work into an automated ETL notebook.
# COMMAND ----------
# 1. Imports and configuration
from pyspark.sql import functions as F

# 2. Load raw data tables (replace with real catalog.schema paths)
df_device = spark.table("<your_catalog>.<your_schema>.raw_device_message")
df_step = spark.table("<your_catalog>.<your_schema>.raw_step_trainer")
df_demo = spark.table("<your_catalog>.<your_schema>.raw_demographics")

# 3. Transform and join (simplified placeholders)
df_joined = (
    df_device.join(df_step, on="sensor_reading_time", how="inner")
             .join(df_demo, on="serial_number", how="inner")
)

# 4. Add labels (placeholder logic)
df_labeled = df_joined.withColumn(
    "step_label",
    F.when(F.col("heart_rate") > 100, F.lit("step")).otherwise(F.lit("no_step"))
).withColumn(
    "source_label",
    F.when(F.col("heart_rate") > 100, F.lit("step")).otherwise(F.lit("device"))
)

# 5. Final curated DataFrame
final_df = df_labeled.select(
    "customer",
    "device_id",
    "step_label",
    "source_label"
)

# 6. Final SQL to write the curated table
final_df.createOrReplaceTempView("final_df")
# COMMAND ----------
%sql
-- Final write step in the clean ETL notebook
CREATE OR REPLACE TABLE labeled_step_test AS
SELECT * FROM final_df;
# COMMAND ----------
# MAGIC %md
# MAGIC ## Talking Through the Databricks Job UI (Demo Script)
# MAGIC 1. In the left menu, open **Workflows → Jobs → Create Job**.
# MAGIC 2. Name the job (e.g., "STEDI 3.3 Automated ETL").
# MAGIC 3. Select the clean ETL notebook you just built.
# MAGIC 4. Choose a cluster: **Single Node, smallest size, latest runtime** is fine for this class.
# MAGIC 5. Click **Run now** to test.
# MAGIC 
# MAGIC **Instructor Tip:** While clicking, connect the steps to production: reliable jobs, clear owners, alerts, and version control make real data pipelines trustworthy.
# COMMAND ----------
# MAGIC %md
# MAGIC ## Ethics Reflection
# MAGIC Automating health-related data (even simple balance scores) carries responsibility:
# MAGIC - Protect privacy and security. Avoid exposing personal identifiers.
# MAGIC - Keep labels accurate; do not make medical claims.
# MAGIC - When in doubt, slow down and review results. We protect **people**, not just data.
# MAGIC 
# MAGIC **Reflection Questions**
# MAGIC - How can we keep this data private while sharing insights?
# MAGIC - What harm could come from wrong labels?
# MAGIC - Who should be notified if an automated job fails or produces strange results?
# COMMAND ----------
# MAGIC %md
# MAGIC ## Wrap-Up & Practice Ideas
# MAGIC **Key Takeaways**
# MAGIC - Clean ETL notebooks are short, repeatable, and end with `CREATE OR REPLACE TABLE labeled_step_test`.
# MAGIC - Databricks Jobs rerun the notebook automatically, so validations must be quick and reliable.
# MAGIC - SQL validation queries catch label errors early.
# MAGIC 
# MAGIC **Practice Tasks for Students**
# MAGIC - Add one more validation query (e.g., check for duplicate device_id/customer pairs).
# MAGIC - Intentionally break a label and see what the invalid-label query shows.
# MAGIC - Set a job schedule (daily) and check the run history tomorrow.
# MAGIC 
# MAGIC Keep encouraging students: mastering small automation steps prepares them for larger ML pipelines! ✅

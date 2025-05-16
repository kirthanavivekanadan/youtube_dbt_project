
# 📺 YouTube Data Pipeline

This project fetches data from the YouTube API using a Python script and automates the data flow into Snowflake using AWS services. The data is then transformed using DBT Cloud and deployed back to Snowflake for analysis. The pipeline is triggered automatically via GitHub pushes using AWS CodePipeline and CodeBuild.

---

## 🏗️ Project Architecture

- **YouTube API**: Data is fetched from the YouTube Data API.
- **GitHub**: Stores the Python script and triggers the pipeline via code pushes.
- **AWS CodePipeline**: Orchestrates the CI/CD process.
- **AWS CodeBuild**: Executes the Python script to extract and load data.
- **Snowflake**: Stores the raw and transformed YouTube data.
- **DBT Cloud**: Transforms raw data into cleaned, analytics-ready tables in Snowflake.

---

## 🗺️ Architecture Diagram
(https://github.com/kirthanavivekanadan/youtube_dbt_project/blob/main/youtube_API.png?raw=true)

## ⚙️ Setup and Configuration

### 🔑 Prerequisites

- GitHub account and repository
- AWS account with permissions for CodePipeline and CodeBuild
- Snowflake account with access to create users, roles, databases, schemas, and tables
- DBT Cloud account and configured project
- YouTube Developer account with API key access

---

### 🪜 Steps

1. **Set up GitHub Repository**
   - Store your `extract_youtube_data.py` script.
   - Add `requirements.txt` and `buildspec.yml`.

2. **Create CodePipeline in AWS**
   - Connect to the GitHub repository.
   - Set source to trigger on pushes to your chosen branch.
   - Add CodeBuild as a build stage.

3. **Configure CodeBuild Project**
   - Use a build environment with Python installed.
   - Add environment variables for Snowflake credentials and YouTube API key.
   - Ensure `buildspec.yml` installs dependencies and runs the script.

4. **Set Up Snowflake**
   - Create a warehouse, database, schema, and staging table(s).
   - Ensure the Python script can connect using Snowflake connector.

5. **Configure DBT Cloud**
   - Connect DBT Cloud to your Snowflake environment.
   - Build transformation models using raw data.
   - Set up a job to run after data is loaded.

---

## ▶️ Running the Project

Once everything is set up:

1. Push your code to the configured GitHub repository.
2. AWS CodePipeline is triggered automatically.
3. CodeBuild runs the Python script to pull data from YouTube and load it to Snowflake.
4. DBT Cloud triggers a job to transform the raw data and publish it back to Snowflake.

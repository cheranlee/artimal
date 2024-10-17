# Artimal Setup Guide

## Steps to Run

1. **Create a Virtual Environment:**

   ```bash
   python3 -m venv myenv  # Create virtual environment
   ```

2. **Activate the Virtual Environment:**

   ```bash
   source myenv/bin/activate  # Activate virtual environment
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt  # Install required packages
   ```

4. **Run the Code:**

   ```bash
   python3 main_otter.py  # Run the main script

   #or

   python3 main_macaque.py

   ```


5. **Deactivate the Virtual Environment:**

   After you're done, deactivate the virtual environment using:

   ```bash
   deactivate  # Exit virtual environment
   ```

---

## Notes

- Make sure you have the `.env` file in the root directory before running the application.

---

## Create a `.env` File in the Root Directory

Add the following content to a `.env` file to securely store environment variables:

```bash
MYSQL_HOST='put_host_name_here'
MYSQL_PORT=port_num
MYSQL_USER='admin'
MYSQL_DATABASE='artimal'
MYSQL_PASSWORD='password'

OPENAI_API_KEY="open_ai_api_key"
```

- Replace the placeholders:
  - `put_host_name_here`: Your MySQL host.
  - `port_num`: The port number for your MySQL server.
  - `admin`: Your MySQL username.
  - `artimal`: The database name.
  - `password`: Your MySQL password.
  - `openai_api_key`: Your OpenAI API key.

---

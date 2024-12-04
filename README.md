# gsheets-vms
Volunteer Management Software (VMS) that works with Google Sheets (.gsheet)

## Setup
To run this project, follow these steps:

### Clone the repository
```bash
git clone https://github.com/ibtikar-org-tr/gsheets-vms
```
```bash
cd gsheets-vms
```

### Create and activate virtual environment
```bash
python -m venv venv
```
### activate the venv
#### On Windows
```bash
.\venv\Scripts\activate
```
#### On Unix or MacOS
```bash
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start the application
```bash
uvicorn app.main:app --reload --port 3001
```

## Dev
### Update packages
```bash
pip freeze > requirements.txt
```

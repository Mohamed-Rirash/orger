# orger
A simple Python CLI tool to automatically organize files in your Downloads (or any specified) folder into dated subdirectories and type-based categories (images, documents, videos, others). Keeps your folder tidy by moving today’s files into a YYYY-MM-DD/ directory with categorized subfolders.
![[demo.png]]


## Features

- **Source Directory**: Defaults to `~/Downloads`, customizable via `--src`.
    
- **Date-Based Folders**: Creates a folder named for today’s date (`YYYY-MM-DD`) or a user-specified date.
    
- **Type Classification**: Sorts files by extension into `images/`, `docs/`, `videos/`, and `other/`.
    
- **Dry-Run & Force**: Preview actions without moving files (`--dry-run`) or skip confirmations (`--yes`).
    
- **Collision Handling**: Appends numeric suffixes to duplicate filenames.
    
- **Configurable & Extensible**: Override date, source path, and extension mappings.



## Installation

1. Clone the repository:
    
    ```
    git clone https://github.com/yourusername/cli-organizer.git
    cd cli-organizer
    ```
    
2. (Optional) Create and activate a virtual environment:
    
    ```
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\\Scripts\\activate  # Windows
    ```
    
3. Install dependencies (none required for core functionality; optional extras below):
    
    ```
    pip install -r requirements.txt  # if you add rich/tabulate
    ```
    

## Usage

```
# Run with defaults
cli-organizer

# Specify a custom source folder and date\cli-organizer --src /path/to/dir --date 2025-04-01

# Dry-run to preview actions
cli-organizer --dry-run

# Skip confirmation
cli-organizer --yes
```

### CLI Options

|Flag|Description|
|---|---|
|`--src <path>`|Source directory (default: `~/Downloads`).|
|`--date <YYYY-MM-DD>`|Override today’s date for the target folder.|
|`--dry-run`|Show planned moves without performing them.|
|`--yes`, `--force`|Skip the confirmation prompt.|
|`--help`|Show help text and exit.|

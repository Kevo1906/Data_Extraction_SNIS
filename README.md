
# **Data Extraction SNIS**

## **Project Overview**

This project is an automated data extraction system designed to streamline the download of various datasets from "Ministerio de Salud y de Deportes de Bolivia". By utilizing Python's robust libraries and best practices in software development, this system ensures accuracy, reliability, and efficiency in retrieving, processing, and storing data.

The project follows a modular structure, with clear separation of concerns for better maintainability and scalability. The code is well-documented, making it easy to extend or integrate into existing workflows.

### **Key Features**
- **Dynamic Data Downloading**: Configurable for multiple sources, designed for flexibility with various endpoints.
- **Modular Architecture**: The project is split into reusable components, ensuring scalability for future enhancements.
- **Error Handling & Logging**: Robust exception handling and logging mechanisms to ensure the system runs smoothly with proper traceability.
- **Virtual Environment Setup**: Isolated Python environment with all dependencies managed for a seamless development experience.
- **Source Code Management**: Clean code structure with version control via `.gitignore` to avoid unnecessary files in the repository.

## **Project Structure**
```
- venv/                # Virtual environment for isolated development
- downloads/           # Downloaded files example
- .gitignore           # Ensures unnecessary files are ignored in version control
- Download_Base.py     # Base script for download logic
- download_tools.py    # Helper functions for data processing and downloading
- __init__.py          # Package initialization
- robots/
    - __init__.py      # Robots package initialization
    - SNIS.py          # Specific script for SNIS data source
```


## **How to Use**
1. Clone the repository.
2. Set up a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On Mac/Linux:
      ```bash
      source venv/bin/activate
      ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```
5. Run the script:
    ```bash
    python __init__.py
    ```


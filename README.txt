# Smart Text Expander

![Smart Text Expander Banner](banner.png)

## Overview

**Smart Text Expander** is a versatile tool designed to streamline your typing by automatically expanding predefined trigger words into longer, frequently used phrases or snippets. Whether you're drafting emails, coding, or writing documents, Smart Text Expander enhances your productivity by reducing repetitive typing tasks.

## Why Smart Text Expander?

Repetitive typing can be time-consuming and monotonous. Smart Text Expander was created to alleviate this by allowing users to define trigger words that automatically expand into desired text. This tool is perfect for individuals and professionals who want to save time, reduce errors, and maintain consistency in their written communications.

## Features

- **Easy Installation:** Simple setup process with automated dependency management.
- **User-Friendly Interface:** Intuitive GUI built with PySide6 for managing triggers.
- **Customizable Triggers:** Add, update, delete, import, and export trigger phrases effortlessly.
- **Dark Mode:** A sleek dark-themed interface that's easy on the eyes.
- **Global Keyboard Hook:** Works across all applications to detect and expand triggers in real-time.

## How It Was Made

Smart Text Expander is developed using Python 3.8 and leverages the PySide6 library for the graphical user interface. The tool employs the `keyboard` library to intercept and handle keyboard events, allowing it to detect trigger words globally across the system. Dependencies are managed within a virtual environment to ensure a smooth installation process.

## Installation

### Prerequisites

- **Operating System:** Windows
- **Python:** Version 3.8 or later

### Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/Smart-Text-Expander.git
    ```
2. **Navigate to the Directory:**
    ```bash
    cd Smart-Text-Expander
    ```
3. **Install Dependencies:**
    ```bash
    python install.py
    ```

*Note: The installation script will set up a virtual environment, install required packages, and create a desktop shortcut for easy access.*

## Usage

1. **Launch Smart Text Expander:**
    - Use the desktop shortcut named "Smart Text Expander".
    - Or run `Smart Text Expander.py` from the installation directory:
      ```bash
      python Smart\ Text\ Expander.py
      ```
2. **Add a Trigger:**
    - Enter a trigger word (e.g., `sig`).
    - Enter the expanded text (e.g., your email signature).
    - Click "Add/Update".
3. **Manage Triggers:**
    - Select a trigger from the list to edit or delete.
    - Use the "Export Triggers" and "Import Triggers" buttons to backup or restore your triggers.
4. **Use in Any Application:**
    - Type your trigger word followed by a space or enter, and it will automatically expand.

## Example Scenario

**Customer Support Representative:**

Imagine you're a customer support rep who frequently sends the same responses to common queries. Instead of typing out the full response each time, you can set up triggers like:

- **Trigger:** `tyvm`
- **Expansion:** `Thank you very much for reaching out. We appreciate your patience.`

Now, whenever you type `tyvm` followed by a space or enter, Smart Text Expander will automatically expand it to the full thank-you message, saving you time and ensuring consistency in your communications.

## Requirements

- **Python 3.8 or later**
- **Windows Operating System**

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, feel free to open an issue on the [GitHub repository](https://github.com/yourusername/Smart-Text-Expander).
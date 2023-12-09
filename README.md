# Document Parser Library

The Document Parser Library is a Python library that provides a set of classes for parsing various types of documents, including PDFs, JSON files, text files, images, Word documents, and Excel spreadsheets. The library is designed to be extensible, allowing users to dynamically create parser objects based on the file type extension.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Classes](#classes)
- [Abstract Factory Design Pattern](#abstract-factory-design-pattern)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/document-parser-library.git
    ```

2. Navigate to the project directory:

    ```bash
    cd document-parser-library
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the document parser library, you can import the necessary classes into your Python code. For example:

    ```python
    from parser import Parser
    ```

Create an instance of the Parser class by providing the path to the document you want to parse. Use the create_parser method to dynamically create the parser object based on the file type extension:

    ```python
    file_path = "path/to/your/file.pdf"
    parser = Parser(file_path)
    parser = parser.create_parser()
    ```

Once you have the parser object, you can use its methods to extract metadata, text, images, and tables as needed.

## Classes

### Parser
The Parser class is responsible for dynamically creating parser objects based on the file type extension. It contains a factory_map that maps file extensions to corresponding parser factories. The create_parser method uses the selected factory to create the parser object.

#### Parser (Abstract Class)
The Parser is an abstract class with a static method create_parser. Concrete factories such as PDFParser, JSONParser, etc., extend this class and implement the create_parser method to instantiate the corresponding parser class.

#### Concrete Parser Classes
The library includes the following concrete parser classes:

    ```bash
    PDFParser: Parses PDF files.
    JSONParser: Parses JSON files.
    TextParser: Parses text files.
    ImageParser: Parses image files.
    WordParser: Parses Word documents.
    ExcelParser: Parses Excel spreadsheets.
    ```

Each parser class provides methods for extracting metadata, text, images, and tables from the respective document type.

#### Abstract Factory Design Pattern

The library employs the abstract factory design pattern to allow for the dynamic creation of parser objects. The Parser is an abstract class that declares the create_parser method, and each concrete factory provides its own implementation of this method. The Parser class uses the selected factory to create the parser object dynamically based on the file type extension.

## Testing

To run unit tests for the parser classes, use the following commands:
    ```bash
    python -m unittest PDFParserTest.py
    python -m unittest JSONParserTest.py
    python -m unittest TextParserTest.py
    python -m unittest ImageParserTest.py
    python -m unittest WordParserTest.py
    python -m unittest ExcelParserTest.py
    ```

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
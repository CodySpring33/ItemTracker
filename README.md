# CS:GO Item Tracker

CS:GO Item Tracker is a command-line application that tracks the prices of your favorite CS:GO items on the Steam Market. It allows you to easily monitor price trends, view historical price data, and add or remove items from your tracking list.

## Features

- Track CS:GO items on the Steam Market by name
- Display tracked items with their current prices
- View historical price data with timestamps
- Generate price/time graphs for selected items
- Add and remove items from the tracking list
- Customize the output with colors and ASCII art

## Installation

1. Make sure you have Python 3.6 or higher installed on your system. You can download the latest version of Python from [the official website](https://www.python.org/downloads/).

2. Clone the repository or download the `csgo.py` script to a directory of your choice.

3. Install the required packages:

```bash
pip install requests beautifulsoup4 matplotlib rich
```

4. (Optional) If you are using Windows, you might need to install the `windows-curses` package to properly display the output:

```bash
pip install windows-curses
```

## Usage

1. Open a terminal or command prompt in the directory where the `csgo.py` script is located.

2. Run the script:

```bash
python main.py
```

3. Follow the on-screen instructions to add items to your tracking list, view prices, and generate graphs.

4. To exit the program, enter 'q' during the waiting period between price updates.

## Contributing

Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue on the project's repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

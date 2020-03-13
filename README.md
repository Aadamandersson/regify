# regify

## Documentation

Documentation can be found at [https://regify.github.io](https://regify.github.io)

## Installation

You can download and install the latest version of this software using pip as below:

    $ pip install regify

## Usage
    >>> import regify
    >>> src = 'VARCHAR("A-Z", 1, 2)'
    >>> regify.generate(src)
    '[A-Z]{1,2}'

If you prefer to write in a seperate file and generate the pattern from that, you could use regify.generate_from_file(filepath) instead.

## Authors

* **Adam Andersson & Ludwig Hansson** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
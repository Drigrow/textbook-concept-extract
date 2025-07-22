# textbook-concept-extract
I wrote this program to extract concept definitions from Chinese senior high school textbooks.

## Before Start

There are some python libraries you may not have installed. And horribly I forgot what libs are being used so you may read the `import` part and check you installed libs.

## How to use

1. Download book pdf and get path. Fill the path to `extract.py `
2. Download `concept.md` and see the format. Use similar format for your concept and save as `concept.md`.
3. Fill your AI API to `extract.py`. In this case, understanding long files is a must, so I chose qwen-long. If you have your own model, modify the code yourself please, I called API in openai compatible format for ease of use.
4. <del>Press F5</del> Run the code. You will find one `output` folder and that's where the extraction is stored.
5. For further formating, like transforming `.md` file to `.docx` or `.pdf` files, see `convertion.py`. GO THROUGH CODE BEFORE RUN PLZ. If you find it difficult running `conversion.py` (just like me lol), don't hesitate, go ask AI.

## PS

I only used it to extract from Biology books, for other subjects, test yourself :)

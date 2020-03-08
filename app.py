from textwrap import dedent
from flask import Flask, request, make_response, render_template, escape
import black

app = Flask(__name__)

def black_format_code():
    source = request.form['source']
    print(list(request.form.items()))
    kwargs = {
        'line_length': int(request.form['-l']),
        'string_normalization': False if request.form.get('-s') == 'on' else True,
    }
    reformatted_source = black.format_file_contents(
        source, fast=True, mode=black.FileMode(**kwargs)
    )
    return reformatted_source

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        code_placeholder = black_format_code()
    else:
        code_placeholder = escape(dedent('''
        print('Press the "Black" button to reformat this code!')
        j = [1,
        2,
        3
        ]
        
        def very_important_function(template: str, *variables, file: os.PathLike, engine: str, header: bool = True, debug: bool = False):
            """Applies `variables` to the `template` and writes to `file`."""
            with open(file, 'w') as f:
                ...
        
        '''))
    return render_template('home.j2', code_placeholder=code_placeholder)


@app.route('/format', methods=['POST'])
def format_code():
    reformatted_source = black_format_code()
    response = make_response(reformatted_source)
    response.mimetype = 'text/plain'
    return response


if __name__ == '__main__':
    app.run(debug=True)
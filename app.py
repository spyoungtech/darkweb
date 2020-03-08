from flask import Flask, request, make_response, render_template_string, flash
import black

app = Flask(__name__)


@app.route('/')
def home():
    return render_template_string(
        '''
    <html>
    <form method="post" action="/format" id="blackform">
    Line Length: <input type="number" name="-l" value="88"><br/>
    Skip String Normalization: <input type="checkbox" name="-s"><br/>
    <textarea name="source" form="blackform">print('Paste your code here!')</textarea><br/>
    <input type="submit" value="Black"><br/>
    </form>
    </html>
    '''
    )


@app.route('/format', methods=['POST'])
def format_code():
    source = request.form['source']
    print(list(request.form.items()))
    kwargs = {
        'line_length': int(request.form['-l']),
        'string_normalization': False if request.form.get('-s') == 'on' else True,
    }
    reformatted_source = black.format_file_contents(
        source, fast=True, mode=black.FileMode(**kwargs)
    )
    response = make_response(reformatted_source)
    response.mimetype = 'text/plain'
    return response


if __name__ == '__main__':
    app.run(debug=True)
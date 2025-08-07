from flask import Flask, render_template, request, jsonify
import sys
from io import StringIO
import meow

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json.get('code', '')

    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    result_value, error = meow.run('<playground>', code)
    
    sys.stdout = old_stdout 

    captured_print_output = redirected_output.getvalue()

    final_output_lines = []
    if captured_print_output:
        final_output_lines.append(captured_print_output.strip())

    response_data = {}
    if error:
        response_data['error'] = error.as_string()
        response_data['output'] = "\n".join(final_output_lines)
    elif result_value:
        if isinstance(result_value, meow.List):
            meaningful_results_from_statements = []
            for element in result_value.elements:
                if element != meow.Number.null or isinstance(element, (meow.List, meow.String)):
                    meaningful_results_from_statements.append(element)
            
            if meaningful_results_from_statements:
                if len(meaningful_results_from_statements) == 1:
                    final_output_lines.append(repr(meaningful_results_from_statements[0]))
                else:
                    final_output_lines.append(repr(meaningful_results_from_statements[-1]))
        else:
            if result_value != meow.Number.null:
                final_output_lines.append(repr(result_value))

        response_data['output'] = "\n".join(final_output_lines)
        response_data['error'] = None
    else:
        response_data['output'] = "\n".join(final_output_lines)
        response_data['error'] = None

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)


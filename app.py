from flask import Flask, request, jsonify, render_template
import ast
from radon.complexity import cc_visit
from radon.metrics import mi_visit

app = Flask(__name__)

def analyze_time_complexity(node):
    """
    Analyze time complexity using basic heuristics.
    """
    complexity = 'O(1)'
    if isinstance(node, ast.For) or isinstance(node, ast.While):
        complexity = 'O(n)'
        # Look for nested loops to adjust complexity
        if isinstance(node, ast.For):
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.For):
                    complexity = 'O(n^2)'
                elif isinstance(sub_node, ast.While):
                    complexity = 'O(n^2)'  # Handle nested while loops
    elif isinstance(node, ast.FunctionDef):
        # Analyze function for recursive calls
        for n in ast.walk(node):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                if n.func.id == node.name:
                    complexity = 'O(n log n)'  # Assumes recursion
    return complexity

def analyze_space_complexity(node):
    """
    Analyze space complexity using basic heuristics.
    """
    complexity = 'O(1)'
    if isinstance(node, ast.Assign):
        if isinstance(node.value, (ast.List, ast.Dict, ast.Set)):
            complexity = 'O(n)'
        elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            # Estimate based on function calls
            complexity = 'O(n)'  # Assumes space grows with input size
    return complexity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_code():
    code = request.json.get('code')
    try:
        if not code:
            raise ValueError("No code provided")
        
        # Parse the code into an AST
        tree = ast.parse(code)
        
        # Analyze complexity using Radon
        complexities = cc_visit(tree)
        complexity_data = []

        for complexity in complexities:
            complexity_data.append({
                'name': complexity.name,
                'complexity': complexity.complexity,
                'lineno': complexity.lineno,
                'col_offset': complexity.col_offset
            })

        # Estimate time and space complexity
        time_complexities = set()
        space_complexities = set()

        for node in ast.walk(tree):
            time_complexity = analyze_time_complexity(node)
            space_complexity = analyze_space_complexity(node)

            if time_complexity != 'O(1)':
                time_complexities.add(time_complexity)
            if space_complexity != 'O(1)':
                space_complexities.add(space_complexity)

        time_complexity = 'O(1)' if not time_complexities else max(time_complexities, key=lambda x: ('O(n^2)', 'O(n log n)', 'O(n)', 'O(1)').index(x))
        space_complexity = 'O(1)' if not space_complexities else max(space_complexities, key=lambda x: ('O(n)', 'O(1)').index(x))

        # Calculate maintainability index
        maintainability = mi_visit(code, multi=True)

        # Prepare the results
        results = {
            "complexity": complexity_data,
            "maintainability_index": maintainability,
            "time_complexity": time_complexity,
            "space_complexity": space_complexity
        }

        return jsonify(results)
    
    except Exception as e:
        # Return error message
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

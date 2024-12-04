from flask import Flask, render_template, request, jsonify
import pandas as pd
import unicodedata
import re

app = Flask(__name__)

# Carregar dados
try:
    file_path = 'student_scores.csv'  # Caminho do arquivo no servidor
    data = pd.read_csv(file_path)
    print("Dataset carregado com sucesso.")
except Exception as e:
    data = None
    print(f"Erro ao carregar os dados: {e}")

def normalize_string(s):
    if isinstance(s, str):
        return unicodedata.normalize('NFKD', s.lower()).encode('ASCII', 'ignore').decode('utf-8')
    return str(s).lower()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('question', '')

    if not user_input:
        return jsonify({"response": "Por favor, forneça uma pergunta válida."}), 400

    response = get_response(user_input)
    return jsonify({"response": response})

def get_response(user_input):
    if data is None:
        return "Desculpe, não foi possível carregar a base de dados."

    user_input_lower = normalize_string(user_input)

    # Buscar por tempo de estudo
    if "tempo de estudo" in user_input_lower or "horas" in user_input_lower:
        try:
            Hours = int(re.search(r'\d+', user_input_lower).group())
            return search_by_study_time(Hours)
        except:
            return "Por favor, especifique um número válido de horas."

    # Buscar por notas
    elif "notas" in user_input_lower:
        try:
            grade = float(re.search(r'\d+', user_input_lower).group())
            return search_by_grades(grade)
        except:
            return "Por favor, especifique uma nota válida."

    # Estatísticas gerais
    elif "estatísticas" in user_input_lower:
        return get_statistics()

    else:
        return "Desculpe, não entendi. Por favor, tente uma das opções sugeridas."

def search_by_study_time(Hours):
    matches = data[data['Hours'] == Hours]
    if matches.empty:
        return f"Nenhum estudante encontrado que estude {Hours} horas."
    
    count = len(matches)
    avg_score = matches['Scores'].mean()
    return (
        f"Estudantes que estudam {Hours} horas:\n"
        f"Total: {count} estudantes\n"
        f"Média das notas: {avg_score:.2f}"
    )

def search_by_grades(grade):
    matches = data[data['Scores'] > grade]
    if matches.empty:
        return f"Nenhum estudante encontrado com nota acima de {grade}."
    
    count = len(matches)
    avg_score = matches['Scores'].mean()
    return (
        f"Estudantes com notas acima de {grade}:\n"
        f"Total: {count} estudantes\n"
        f"Média das notas: {avg_score:.2f}"
    )

def get_statistics():
    total_students = len(data)
    avg_score = data['Scores'].mean()
    avg_study_time = data['Hours'].mean()
    return (
        f"Estatísticas gerais:\n\n"
        f"Total de estudantes: {total_students}\n"
        f"Média das notas: {avg_score:.2f}\n"
        f"Média de tempo de estudo: {avg_study_time:.2f} horas"
    )

if __name__ == "__main__":
    app.run(debug=True)

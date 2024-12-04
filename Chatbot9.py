import pandas as pd
import unicodedata
import re
from flask import Flask, render_template, request

app = Flask(__name__)

class Chatbot:
    def __init__(self):
        self.load_data()

    def load_data(self):
        try:
            file_path = r'C:\Users\pedro\Desktop\Chatbot3\student_scores.csv'
            self.data = pd.read_csv(file_path)
            print("Dataset carregado com sucesso.")
        except Exception as e:
            self.data = None
            print(f"Erro ao carregar os dados: {e}")

    def normalize_string(self, s):
        if isinstance(s, str):
            return unicodedata.normalize('NFKD', s.lower()).encode('ASCII', 'ignore').decode('utf-8')
        return str(s).lower()

    def get_response(self, user_input):
        if self.data is None:
            return "Desculpe, não foi possível carregar a base de dados."

        user_input_lower = self.normalize_string(user_input)

        # Buscar por tempo de estudo
        if "tempo de estudo" in user_input_lower or "horas" in user_input_lower:
            try:
                Hours = int(re.search(r'\d+', user_input_lower).group())
                return self.search_by_study_time(Hours)
            except:
                return "Por favor, especifique um número válido de horas."

        # Buscar por notas
        elif "notas" in user_input_lower:
            try:
                grade = float(re.search(r'\d+', user_input_lower).group())
                return self.search_by_grades(grade)
            except:
                return "Por favor, especifique uma nota válida."

        # Estatísticas gerais
        elif "estatísticas" in user_input_lower:
            return self.get_statistics()

        else:
            return "Desculpe, não entendi. Por favor, tente uma das opções sugeridas."

    def search_by_study_time(self, Hours):
        matches = self.data[self.data['Hours'] == Hours]
        if matches.empty:
            return f"Nenhum estudante encontrado que estude {Hours} horas."
        
        count = len(matches)
        avg_score = matches['Scores'].mean()
        return (
            f"Estudantes que estudam {Hours} horas:\n"
            f"Total: {count} estudantes\n"
            f"Média das notas: {avg_score:.2f}"
        )

    def search_by_grades(self, grade):
        matches = self.data[self.data['Scores'] > grade]
        if matches.empty:
            return f"Nenhum estudante encontrado com nota acima de {grade}."
        
        count = len(matches)
        avg_score = matches['Scores'].mean()
        return (
            f"Estudantes com notas acima de {grade}:\n"
            f"Total: {count} estudantes\n"
            f"Média das notas: {avg_score:.2f}"
        )

    def get_statistics(self):
        total_students = len(self.data)
        avg_score = self.data['Scores'].mean()
        avg_study_time = self.data['Hours'].mean()
        return (
            f"Estatísticas gerais:\n\n"
            f"Total de estudantes: {total_students}\n"
            f"Média das notas: {avg_score:.2f}\n"
            f"Média de tempo de estudo: {avg_study_time:.2f} horas"
        )


# Instanciando o chatbot
chatbot = Chatbot()

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = chatbot.get_response(user_input)
    return render_template("index.html", response=response)


if __name__ == "__main__":
    app.run(debug=True)


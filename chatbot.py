import customtkinter as ctk
import pandas as pd
import unicodedata
import re
import gdown
import os

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Student Performance Assistant")
        master.geometry("800x600")

        # Configuração da janela
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=0)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Área de texto
        self.text_area = ctk.CTkTextbox(master, width=700, height=400, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, "Olá! Eu sou seu assistente de Desempenho Estudantil. Você pode fazer perguntas como:\n\n" +
                            "1. Buscar por gênero: 'Mostre informações sobre estudantes do gênero [M/F]'\n" +
                            "2. Buscar por idade: 'Quais estudantes têm [idade] anos?'\n" +
                            "3. Buscar por tempo de estudo: 'Mostrar estudantes que estudam [X] horas'\n" +
                            "4. Buscar por notas: 'Mostrar estudantes com notas acima de [X]'\n" +
                            "5. Estatísticas: 'Mostrar estatísticas gerais'\n\n")
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=600, placeholder_text="Digite sua pergunta...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="blue", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

        # Carregar dados
        self.load_data()

    def load_data(self):
        try:
            file_path = 'StudentPerformanceFactors.csv'
            if not os.path.exists(file_path):
                print("Baixando dataset...")
                url = 'https://drive.google.com/uc?id=12Byng2nIS2QFBifzCj6TvVQXud5ejpg7'
                gdown.download(url, file_path, quiet=False)
            
            self.data = pd.read_csv(file_path)
        except Exception as e:
            self.data = None
            print(f"Erro ao carregar dados: {e}")

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "\nVocê: " + user_input + "\n")
        self.text_area.configure(state="disabled")

        response = self.get_response(user_input)

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Assistente: " + response + "\n")
        self.text_area.see("end")
        self.text_area.configure(state="disabled")

        self.entry.delete(0, ctk.END)

    def normalize_string(self, s):
        if isinstance(s, str):
            return unicodedata.normalize('NFKD', s.lower()).encode('ASCII', 'ignore').decode('utf-8')
        return str(s).lower()

    def get_response(self, user_input):
        if self.data is None:
            return "Desculpe, não foi possível carregar a base de dados."

        user_input_lower = self.normalize_string(user_input)

        # Busca por gênero
        if "gênero" in user_input_lower:
            gender = 'M' if 'masculino' in user_input_lower or 'm' in user_input_lower else 'F'
            return self.search_by_gender(gender)

        # Busca por idade
        elif "idade" in user_input_lower or "anos" in user_input_lower:
            try:
                age = int(re.search(r'\d+', user_input_lower).group())
                return self.search_by_age(age)
            except:
                return "Por favor, especifique uma idade válida"

        # Busca por tempo de estudo
        elif "tempo de estudo" in user_input_lower or "horas" in user_input_lower:
            try:
                hours = int(re.search(r'\d+', user_input_lower).group())
                return self.search_by_study_time(hours)
            except:
                return "Por favor, especifique um número válido de horas"

        # Busca por notas
        elif "notas" in user_input_lower:
            try:
                grade = float(re.search(r'\d+', user_input_lower).group())
                return self.search_by_grades(grade)
            except:
                return "Por favor, especifique uma nota válida"

        # Estatísticas gerais
        elif "estatísticas" in user_input_lower:
            return self.get_statistics()

        else:
            return "Desculpe, não entendi sua pergunta. Por favor, tente uma das opções sugeridas."

    def search_by_gender(self, gender):
        matches = self.data[self.data['gender'] == gender]
        if matches.empty:
            return f"Nenhum estudante encontrado do gênero {gender}."
        
        avg_grade = matches['grade'].mean()
        count = len(matches)
        return f"Estudantes do gênero {gender}:\n" + \
               f"Total: {count} estudantes\n" + \
               f"Média das notas: {avg_grade:.2f}"

    def search_by_age(self, age):
        matches = self.data[self.data['age'] == age]
        if matches.empty:
            return f"Nenhum estudante encontrado com {age} anos."
        
        count = len(matches)
        avg_grade = matches['grade'].mean()
        return f"Estudantes com {age} anos:\n" + \
               f"Total: {count} estudantes\n" + \
               f"Média das notas: {avg_grade:.2f}"

    def search_by_study_time(self, hours):
        matches = self.data[self.data['studytime'] == hours]
        if matches.empty:
            return f"Nenhum estudante encontrado que estude {hours} horas."
        
        count = len(matches)
        avg_grade = matches['grade'].mean()
        return f"Estudantes que estudam {hours} horas:\n" + \
               f"Total: {count} estudantes\n" + \
               f"Média das notas: {avg_grade:.2f}"

    def search_by_grades(self, grade):
        matches = self.data[self.data['grade'] > grade]
        if matches.empty:
            return f"Nenhum estudante encontrado com nota acima de {grade}."
        
        count = len(matches)
        avg_grade = matches['grade'].mean()
        return f"Estudantes com notas ac ima acima de {grade}:\n" + \
               f"Total: {count} estudantes\n" + \
               f"Média das notas: {avg_grade:.2f}"

    def get_statistics(self):
        total_students = len(self.data)
        avg_grade = self.data['grade'].mean()
        gender_distribution = self.data['gender'].value_counts()

        stats = f"Estatísticas gerais:\n\n" \
                f"Total de estudantes: {total_students}\n" \
                f"Média das notas: {avg_grade:.2f}\n\n" \
                f"Distribuição de gênero:\n"
        
        for gender, count in gender_distribution.items():
            stats += f"- {gender}: {count} estudantes\n"
        
        return stats

def main():
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()

if __name__ == "__main__":
    main()
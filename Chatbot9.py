from flask import Flask
import customtkinter as ctk
import pandas as pd
import unicodedata
import re


class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Artemis - Assistente Estudantil")
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
        self.text_area.insert(
            ctk.END,
            "Olá! Eu sou seu assistente de Desempenho Estudantil. Você pode fazer perguntas como:\n\n"
            "1. Buscar por tempo de estudo: 'Mostrar estudantes que estudam [X] horas'\n"
            "2. Buscar por notas: 'Mostrar estudantes com notas acima de [X]'\n"
            "3. Estatísticas: 'Mostrar estatísticas gerais'\n\n"
        )
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=600, placeholder_text="Digite sua pergunta aqui...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="blue", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

        # Carregar dados
        self.load_data()

    def load_data(self):
        try:
            file_path = r'C:\Users\pedro\Desktop\Chatbot3\student_scores.csv'
            self.data = pd.read_csv(file_path)
            print("Dataset carregado com sucesso.")
        except Exception as e:
            self.data = None
            print(f"Erro ao carregar os dados: {e}")

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "\nVocê: " + user_input + "\n")
        self.text_area.configure(state="disabled")

        response = self.get_response(user_input)

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Artemis: " + response + "\n")
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


# Fim da classe Chatbot

def main():
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()


if __name__ == "__main__":
    main()

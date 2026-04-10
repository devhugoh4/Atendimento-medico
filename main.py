import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import sqlite3

def iniciar_db():
    conn = sqlite3.connect("agendamentos_medicos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medico TEXT,
            data TEXT,
            dia_semana TEXT,
            hora TEXT
        )
    """)
    conn.commit()
    conn.close()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppAgendamento(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Seja Bem-Vindo a Clínica Viver")
        self.geometry("500x500")

        self.medicos = [
            "Dr. Silva - Cardiologista",
            "Dra. Costa - Dermatologista",
            "Dr. Pereira - Clínico Geral"
        ]

        iniciar_db()
        self.criar_interface()

    def criar_interface(self):
        ctk.CTkLabel(self, text="Agendamento Médico", font=("Arial", 22, "bold")).pack(pady=20)

        ctk.CTkLabel(self, text="Selecione o Médico:").pack(pady=5)
        self.combo_medico = ctk.CTkComboBox(self, values=self.medicos, width=300)
        self.combo_medico.pack(pady=5)


        ctk.CTkLabel(self, text="Data (DD/MM/AAAA):").pack(pady=5)
        self.entry_data = ctk.CTkEntry(self, placeholder_text="Ex: 10/04/2026", width=300)
        self.entry_data.pack(pady=5)

        ctk.CTkLabel(self, text="Escolha o Horário:").pack(pady=5)
        horarios = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        self.combo_hora = ctk.CTkComboBox(self, values=horarios, width=300)
        self.combo_hora.pack(pady=5)

        self.btn_confirmar = ctk.CTkButton(self, text="Confirmar Agendamento", 
                                          command=self.salvar_agendamento, fg_color="green", hover_color="#006400")
        self.btn_confirmar.pack(pady=20)

        self.btn_ver = ctk.CTkButton(self, text="Ver Agendamentos Salvos", 
                                     command=self.visualizar_banco, fg_color="gray")
        self.btn_ver.pack(pady=5)

    def obter_dia_semana(self, data_str):
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y")
            dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
            return dias[data_obj.weekday()]
        except ValueError:
            return None

    def salvar_agendamento(self):
        medico = self.combo_medico.get()
        data_texto = self.entry_data.get()
        hora = self.combo_hora.get()
        dia_semana = self.obter_dia_semana(data_texto)

        if not dia_semana:
            messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA.")
            return
        try:
            conn = sqlite3.connect("agendamentos_medicos.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO agendamentos (medico, data, dia_semana, hora) VALUES (?, ?, ?, ?)",
                           (medico, data_texto, dia_semana, hora))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", f"Agendado com sucesso!\n\n{medico}\n{data_texto} ({dia_semana}) às {hora}")
            self.entry_data.delete(0, 'end') 
        except Exception as e:
            messagebox.showerror("Erro de Banco", f"Erro ao salvar: {e}")

    def visualizar_banco(self):
        conn = sqlite3.connect("agendamentos_medicos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agendamentos")
        dados = cursor.fetchall()
        conn.close()

        lista_msg = "\n".join([f"{d[1]} - {d[2]} ({d[3]}) às {d[4]}" for d in dados])
        messagebox.showinfo("Consultas Agendadas", lista_msg if lista_msg else "Nenhum agendamento encontrado.")

if __name__ == "__main__":
    app = AppAgendamento()
    app.mainloop()
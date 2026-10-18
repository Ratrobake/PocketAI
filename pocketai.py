import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class BotCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador de Bots Offline")
        self.root.geometry("750x520")
        self.root.minsize(700, 500)

        # Diccionario para almacenar los bots y sus reglas: {nombre_bot: {comando: respuesta}}
        self.bots_database = {
            "AsistenteLocal": {
                "/hola": "¡Hola! Soy tu bot offline. ¿En qué puedo ayudarte?",
                "/ayuda": "Comandos disponibles: /hola, /hora, /estado, /ayuda",
                "/hora": f"La hora local actual es {datetime.datetime.now().strftime('%H:%M:%S')}",
                "/estado": "Sistemas operando al 100%. Sin conexión a internet requerida."
            }
        }
        self.current_bot = "AsistenteLocal"

        self.setup_styles()
        self.create_widgets()
        self.load_bot_rules()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Colores personalizados estilo moderno
        self.bg_color = "#f4f6f9"
        self.primary_color = "#2c3e50"
        self.accent_color = "#2980b9"
        
        self.root.configure(bg=self.bg_color)

    def create_widgets(self):
        # Título principal
        title_label = tk.Label(
            self.root, text="🤖 Entorno de Creación de Bots Offline", 
            font=("Segoe UI", 16, "bold"), bg=self.bg_color, fg=self.primary_color
        )
        title_label.pack(pady=10)

        # Contenedor principal divido en dos pestañas o paneles
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=5)

        # Pestaña 1: Editor de Reglas del Bot
        self.tab_editor = ttk.Frame(notebook)
        notebook.add(self.tab_editor, text="⚙️ Configurar Bot")

        # Pestaña 2: Simulador de Chat Offline
        self.tab_chat = ttk.Frame(notebook)
        notebook.add(self.tab_chat, text="💬 Probar Chat Offline")

        self.setup_editor_tab()
        self.setup_chat_tab()

    def setup_editor_tab(self):
        # Panel superior: Selección y creación de bots
        top_frame = tk.Frame(self.tab_editor, bg="white", padx=10, pady=10)
        top_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(top_frame, text="Seleccionar Bot:", font=("Segoe UI", 10, "bold"), bg="white").pack(side="left", padx=5)
        
        self.bot_combobox = ttk.Combobox(top_frame, state="readonly", width=20)
        self.bot_combobox.pack(side="left", padx=5)
        self.bot_combobox['values'] = list(self.bots_database.keys())
        self.bot_combobox.set(self.current_bot)
        self.bot_combobox.bind("<<ComboboxSelected>>", self.on_bot_selected)

        new_bot_btn = ttk.Button(top_frame, text="➕ Nuevo Bot", command=self.crear_nuevo_bot)
        new_bot_btn.pack(side="left", padx=10)

        # Panel central: Tabla de Comandos y Respuestas
        center_frame = tk.Frame(self.tab_editor, bg="white", padx=10, pady=10)
        center_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(center_frame, text="Reglas de Respuestas (Comando y Respuesta):", font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w", pady=5)

        # Treeview para mostrar comandos
        columns = ("Comando", "Respuesta del Bot")
        self.tree = ttk.Treeview(center_frame, columns=columns, show="headings", height=8)
        self.tree.heading("Comando", text="Comando / Palabra Clave")
        self.tree.heading("Respuesta del Bot", text="Respuesta Configurada")
        self.tree.column("Comando", width=180, anchor="w")
        self.tree.column("Respuesta del Bot", width=400, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Panel inferior: Añadir/Eliminar reglas
        bottom_frame = tk.Frame(self.tab_editor, bg="white", padx=10, pady=10)
        bottom_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(bottom_frame, text="Comando:", bg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.cmd_entry = ttk.Entry(bottom_frame, width=20)
        self.cmd_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(bottom_frame, text="Respuesta:", bg="white").grid(row=0, column=2, sticky="w", padx=5)
        self.resp_entry = ttk.Entry(bottom_frame, width=40)
        self.resp_entry.grid(row=0, column=3, padx=5, pady=5)

        add_btn = ttk.Button(bottom_frame, text="Guardar Regla", command=self.agregar_regla)
        add_btn.grid(row=0, column=4, padx=10)

        del_btn = ttk.Button(bottom_frame, text="Eliminar Regla", command=self.eliminar_regla)
        del_btn.grid(row=0, column=5, padx=5)

    def setup_chat_tab(self):
        # Panel de chat interactivo offline
        chat_frame = tk.Frame(self.tab_chat, bg="white", padx=10, pady=10)
        chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.chat_display = tk.Text(chat_frame, wrap="word", state="disabled", font=("Consolas", 10), bg="#fafafa")
        self.chat_display.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        input_frame = tk.Frame(chat_frame, bg="white")
        input_frame.pack(side="bottom", fill="x", pady=5)

        self.chat_input = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.chat_input.pack(side="left", fill="x", expand=True, padx=5)
        self.chat_input.bind("<Return>", lambda event: self.enviar_mensaje())

        send_btn = ttk.Button(input_frame, text="Enviar", command=self.enviar_mensaje)
        send_btn.pack(side="right", padx=5)

        # Mensaje inicial en el chat
        self.escribir_en_chat("Sistema", "¡Bienvenido al simulador! Escribe un comando configurado (ej. /hola) para hablar con el bot activo.")

    def load_bot_rules(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar reglas del bot actual
        rules = self.bots_database.get(self.current_bot, {})
        for cmd, resp in rules.items():
            self.tree.insert("", "end", values=(cmd, resp))

    def on_bot_selected(self, event):
        self.current_bot = self.bot_combobox.get()
        self.load_bot_rules()

    def crear_nuevo_bot(self):
        nombre = f"Bot_{len(self.bots_database) + 1}"
        self.bots_database[nombre] = {"/hola": f"¡Hola! Soy {nombre} operando sin conexión."}
        self.bot_combobox['values'] = list(self.bots_database.keys())
        self.bot_combobox.set(nombre)
        self.current_bot = nombre
        self.load_bot_rules()
        messagebox.info("Éxito", f"Se ha creado el bot '{nombre}'.")

    def agregar_regla(self):
        cmd = self.cmd_entry.get().strip()
        resp = self.resp_entry.get().strip()

        if not cmd or not resp:
            messagebox.showerror("Error", "Debes rellenar tanto el comando como la respuesta.")
            return

        if not cmd.startswith("/"):
            cmd = "/" + cmd  # Asegurar formato comando

        self.bots_database[self.current_bot][cmd] = resp
        self.load_bot_rules()
        
        self.cmd_entry.delete(0, tk.END)
        self.resp_entry.delete(0, tk.END)

    def eliminar_regla(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atención", "Selecciona una regla de la lista para eliminar.")
            return

        item_values = self.tree.item(selected_item, "values")
        cmd = item_values[0]

        if cmd in self.bots_database[self.current_bot]:
            del self.bots_database[self.current_bot][cmd]
            self.load_bot_rules()

    def enviar_mensaje(self):
        mensaje = self.chat_input.get().strip()
        if not mensaje:
            return

        self.escribir_en_chat("Tú", mensaje)
        self.chat_input.delete(0, tk.END)

        # Lógica de respuesta offline del bot
        rules = self.bots_database.get(self.current_bot, {})
        
        # Buscar coincidencia exacta de comando
        respuesta_bot = rules.get(mensaje.lower(), None)
        
        if not respuesta_bot:
            # Respuesta por defecto si no encuentra el comando
            respuesta_bot = f"Lo siento, no reconozco el comando '{mensaje}'. Escribe /ayuda para ver las opciones disponibles."

        # Simular una pequeña pausa o responder inmediatamente de forma local
        self.root.after(200, lambda: self.escribir_en_chat(self.current_bot, respuesta_bot))

    def escribir_en_chat(self, remitente, texto):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"{remitente}: {texto}\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotCreatorApp(root)
    root.mainloop()

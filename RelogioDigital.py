import customtkinter as ctk
import time
import locale

# --- CLASSE PRINCIPAL DA APLICAÇÃO ---
class DigitalClock(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. CONFIGURAÇÕES DA JANELA (Otimizadas para um visual limpo) ---
        self.title("Relógio Digital Profissional")

        # Define a aparência global (System, Dark, Light)
        ctk.set_appearance_mode("Dark") 
        # Define o tema de cores padrão (blue, dark-blue, green)
        ctk.set_default_color_theme("blue")

        # Remove a barra de título e bordas padrão do sistema operacional
        self.overrideredirect(True)
        # Torna o fundo da janela transparente (a cor exata depende do tema)
        # No tema "Dark", o fundo padrão é #242424
        self.wm_attributes("-transparentcolor", "#242424")

        # Define a geometria inicial e centraliza a janela
        window_width = 500
        window_height = 220
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Permite arrastar a janela sem barra de título
        self.bind("<B1-Motion>", self.move_window)
        self.bind("<ButtonPress-1>", self.get_pos)

        # --- 2. CRIAÇÃO DOS WIDGETS ---
        
        # Label para exibir a hora
        self.time_label = ctk.CTkLabel(
            self, 
            text="", # O texto será atualizado pela função update_clock
            font=ctk.CTkFont(family="Digital-7", size=80, weight="bold")
        )
        self.time_label.pack(expand=True, padx=20, pady=20)

        # Label para exibir a data
        self.date_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="Arial", size=18)
        )
        self.date_label.pack(expand=True, anchor='s', pady=(0, 20))

        # ===== MUDANÇA PRINCIPAL AQUI =====
        # Botão para fechar a aplicação (agora usando texto)
        self.close_button = ctk.CTkButton(
            self,
            text="✕",  # Usando um caractere unicode para um 'X' mais elegante
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="white",
            width=28,
            height=28,
            fg_color="transparent", # Cor de fundo normal (transparente)
            hover_color="#c90000", # Cor de fundo ao passar o mouse (vermelho)
            command=self.quit
        )
        self.close_button.place(x=window_width - 35, y=5)
        # ==================================

        # --- 3. INICIALIZAÇÃO ---
        self.update_clock()

    # --- FUNÇÕES ---

    def update_clock(self):
        """
        Atualiza as labels de hora e data a cada segundo.
        Esta função se auto-chama usando o método 'after', garantindo que a GUI não trave.
        """
        current_time = time.strftime('%H:%M:%S')
        self.time_label.configure(text=current_time)
        
        current_date = time.strftime('%A, %d de %B de %Y').capitalize()
        self.date_label.configure(text=current_date)
        
        self.after(1000, self.update_clock)

    def get_pos(self, event):
        """Captura a posição inicial do clique para mover a janela."""
        self.x_win = event.x
        self.y_win = event.y

    def move_window(self, event):
        """Move a janela com base no arrastar do mouse."""
        self.geometry(f'+{event.x_root - self.x_win}+{event.y_root - self.y_win}')


# --- PONTO DE ENTRADA DA APLICAÇÃO ---
if __name__ == "__main__":
    # Define o idioma para a exibição da data em português
    try:
        # Tenta configurar para Português do Brasil em diferentes sistemas operacionais
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
        except locale.Error:
            print("Locale pt_BR não encontrado. A data pode aparecer em inglês.")

    app = DigitalClock()
    # Carrega a fonte customizada (garanta que a pasta 'fonts' e o arquivo .ttf existam)
    try:
        app.time_label.cget("font").add_font("fonts/digital-7.ttf")
    except Exception as e:
        print(f"Aviso: Não foi possível carregar a fonte 'Digital-7'. Usando fonte padrão. Erro: {e}")

    app.mainloop()
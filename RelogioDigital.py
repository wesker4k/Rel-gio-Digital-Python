# ==============================================================================
#  1. IMPORTAÇÕES NECESSÁRIAS
# ==============================================================================
import customtkinter as ctk
import tkinter as tk
import time
import locale
import json
import os
import threading
from playsound import playsound

# ==============================================================================
#  2. MÓDULO DE GERENCIAMENTO DE CONFIGURAÇÃO (ConfigManager)
#    (Lógica que antes estava em config_manager.py)
# ==============================================================================
CONFIG_FILE = 'config.json'

DEFAULT_SETTINGS = {
    "geometry": "450x300+100+100",
    "theme": "Dark",
    "color_theme": "blue",
    "always_on_top": False,
    "opacity": 1.0,
    "alarms": []  # Lista de alarmes no formato "HH:MM"
}

def load_settings():
    """Carrega as configurações do arquivo JSON. Se não existir, cria com valores padrão."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        return DEFAULT_SETTINGS
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            settings = json.load(f)
            # Garante que todas as chaves padrão existam
            for key in DEFAULT_SETTINGS:
                if key not in settings:
                    settings[key] = DEFAULT_SETTINGS[key]
            return settings
    except (json.JSONDecodeError, IOError):
        # Em caso de arquivo corrompido, retorna o padrão
        return DEFAULT_SETTINGS

def save_settings(settings):
    """Salva o dicionário de configurações no arquivo JSON."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings, f, indent=4)


# ==============================================================================
#  3. MÓDULO DE GERENCIAMENTO DE ALARMES (AlarmManager)
#     (Lógica que antes estava em alarm_manager.py)
# ==============================================================================
class AlarmManager:
    def __init__(self, app_instance):
        self.app = app_instance
        self.thread = None
        self.running = False

    def start(self):
        """Inicia a thread de verificação de alarmes."""
        self.running = True
        self.thread = threading.Thread(target=self._check_alarms_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Para a thread de verificação."""
        self.running = False

    def _check_alarms_loop(self):
        """Loop que verifica continuamente se é hora de algum alarme tocar."""
        while self.running:
            now = time.strftime('%H:%M')
            # Usamos uma cópia da lista para evitar problemas com concorrência de threads
            alarms_to_check = list(self.app.settings.get("alarms", []))
            
            if now in alarms_to_check:
                print(f"Alarme disparado: {now}")
                try:
                    # Toca o som do alarme
                    playsound('assets/alarm.mp3')
                except Exception as e:
                    print(f"Erro ao tocar o som do alarme: {e}")
                
                # Remove o alarme para não tocar novamente no mesmo minuto
                self.app.remove_alarm(now, from_thread=True)
                # Dorme o resto do minuto para não disparar de novo
                time.sleep(60) 
            else:
                time.sleep(1) # Verifica a cada segundo


# ==============================================================================
#  4. CLASSE PRINCIPAL DA APLICAÇÃO (DigitalClockApp)
#     (O coração do programa, que antes estava em app.py)
# ==============================================================================
class DigitalClockApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÃO INICIAL E CARREGAMENTO ---
        self.settings = load_settings()
        self.alarm_manager = AlarmManager(self)
        
        # Estado do Cronômetro e Timer
        self.stopwatch_running = False
        self.stopwatch_time = 0.0
        self.timer_running = False
        self.timer_time_left = 0

        self._setup_window()
        self._create_widgets()
        self._apply_settings()

        # Inicia loops
        self.update_loop()
        self.alarm_manager.start()

    def _setup_window(self):
        """Configura a janela principal."""
        self.title("Relógio Digital Pro")
        self.geometry(self.settings["geometry"])
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Button-3>", self.show_context_menu)

    def _create_widgets(self):
        """Cria todos os widgets da interface."""
        self.tab_view = ctk.CTkTabview(self, anchor="w")
        self.tab_view.pack(expand=True, fill="both", padx=5, pady=5)
        self.tab_view.add("Relógio")
        self.tab_view.add("Alarmes")
        self.tab_view.add("Cronômetro")
        self.tab_view.add("Timer")
        
        # --- ABA RELÓGIO ---
        self.time_label = ctk.CTkLabel(self.tab_view.tab("Relógio"), font=ctk.CTkFont(size=60, weight="bold"))
        self.time_label.pack(expand=True, padx=20, pady=5)
        self.date_label = ctk.CTkLabel(self.tab_view.tab("Relógio"), font=ctk.CTkFont(size=18))
        self.date_label.pack(expand=True, padx=20, pady=5)

        # --- ABA ALARMES ---
        alarm_frame = ctk.CTkFrame(self.tab_view.tab("Alarmes"))
        alarm_frame.pack(expand=True, fill="both", padx=5, pady=5)
        self.alarm_entry = ctk.CTkEntry(alarm_frame, placeholder_text="HH:MM")
        self.alarm_entry.pack(pady=10, padx=10, fill="x")
        add_button = ctk.CTkButton(alarm_frame, text="Adicionar Alarme", command=self.add_alarm)
        add_button.pack(pady=5, padx=10, fill="x")
        self.alarms_list_frame = ctk.CTkScrollableFrame(alarm_frame, label_text="Alarmes Ativos")
        self.alarms_list_frame.pack(expand=True, fill="both", pady=10, padx=10)
        
        # --- ABA CRONÔMETRO ---
        stopwatch_frame = ctk.CTkFrame(self.tab_view.tab("Cronômetro"))
        stopwatch_frame.pack(expand=True, fill="both")
        self.stopwatch_label = ctk.CTkLabel(stopwatch_frame, font=ctk.CTkFont(size=50, weight="bold"), text="00:00:00.0")
        self.stopwatch_label.pack(expand=True)
        stopwatch_controls = ctk.CTkFrame(stopwatch_frame, fg_color="transparent")
        stopwatch_controls.pack(pady=10)
        ctk.CTkButton(stopwatch_controls, text="Iniciar", command=self.start_stopwatch).pack(side="left", padx=5)
        ctk.CTkButton(stopwatch_controls, text="Pausar", command=self.pause_stopwatch).pack(side="left", padx=5)
        ctk.CTkButton(stopwatch_controls, text="Zerar", command=self.reset_stopwatch).pack(side="left", padx=5)

        # --- ABA TIMER ---
        timer_frame = ctk.CTkFrame(self.tab_view.tab("Timer"))
        timer_frame.pack(expand=True, fill="both")
        self.timer_label = ctk.CTkLabel(timer_frame, font=ctk.CTkFont(size=50, weight="bold"), text="00:00:00")
        self.timer_label.pack(expand=True)
        timer_input_frame = ctk.CTkFrame(timer_frame, fg_color="transparent")
        timer_input_frame.pack(pady=5)
        self.timer_min_entry = ctk.CTkEntry(timer_input_frame, placeholder_text="Min", width=60)
        self.timer_min_entry.pack(side="left", padx=5)
        self.timer_sec_entry = ctk.CTkEntry(timer_input_frame, placeholder_text="Seg", width=60)
        self.timer_sec_entry.pack(side="left", padx=5)
        timer_controls = ctk.CTkFrame(timer_frame, fg_color="transparent")
        timer_controls.pack(pady=10)
        ctk.CTkButton(timer_controls, text="Iniciar", command=self.start_timer).pack(side="left", padx=5)
        ctk.CTkButton(timer_controls, text="Pausar", command=self.pause_timer).pack(side="left", padx=5)
        ctk.CTkButton(timer_controls, text="Zerar", command=self.reset_timer).pack(side="left", padx=5)

    def _apply_settings(self):
        """Aplica as configurações carregadas na interface."""
        ctk.set_appearance_mode(self.settings["theme"])
        ctk.set_default_color_theme(self.settings["color_theme"])
        self.wm_attributes("-topmost", self.settings["always_on_top"])
        self.wm_attributes("-alpha", self.settings["opacity"])
        self.update_alarms_display()
        
    def update_loop(self):
        """Loop principal que atualiza a UI a cada 100ms."""
        self.time_label.configure(text=time.strftime('%H:%M:%S'))
        self.date_label.configure(text=time.strftime('%A, %d de %B de %Y').capitalize())
        
        if self.stopwatch_running: self.stopwatch_time += 0.1
        mins, secs = divmod(self.stopwatch_time, 60)
        hours, mins = divmod(mins, 60)
        self.stopwatch_label.configure(text=f'{int(hours):02}:{int(mins):02}:{int(secs):02}.{int((self.stopwatch_time % 1) * 10)}')

        if self.timer_running and self.timer_time_left > 0.09: self.timer_time_left -= 0.1
        elif self.timer_running and self.timer_time_left <= 0.09:
            self.timer_time_left = 0
            self.timer_running = False
            playsound('assets/alarm.mp3')
        mins, secs = divmod(self.timer_time_left, 60)
        hours, mins = divmod(mins, 60)
        self.timer_label.configure(text=f'{int(hours):02}:{int(mins):02}:{int(round(secs)):02}')

        self.after(100, self.update_loop)

    def on_closing(self):
        self.settings["geometry"] = self.geometry()
        save_settings(self.settings)
        self.alarm_manager.stop()
        self.destroy()

    def show_context_menu(self, event):
        context_menu = tk.Menu(self, tearoff=0)
        theme_menu = tk.Menu(context_menu, tearoff=0)
        theme_menu.add_command(label="Dark", command=lambda: self.set_theme("Dark"))
        theme_menu.add_command(label="Light", command=lambda: self.set_theme("Light"))
        context_menu.add_cascade(label="Tema", menu=theme_menu)
        opacity_menu = tk.Menu(context_menu, tearoff=0)
        for val in [1.0, 0.9, 0.8, 0.7]:
            opacity_menu.add_command(label=f"{int(val*100)}%", command=lambda v=val: self.set_opacity(v))
        context_menu.add_cascade(label="Opacidade", menu=opacity_menu)
        on_top_var = tk.BooleanVar(value=self.settings["always_on_top"])
        context_menu.add_checkbutton(label="Sempre no Topo", variable=on_top_var, command=lambda: self.toggle_on_top(on_top_var.get()))
        context_menu.add_separator()
        context_menu.add_command(label="Sair", command=self.on_closing)
        context_menu.tk_popup(event.x_root, event.y_root)

    def set_theme(self, theme):
        ctk.set_appearance_mode(theme)
        self.settings["theme"] = theme
    
    def set_opacity(self, value):
        self.wm_attributes("-alpha", value)
        self.settings["opacity"] = value
        
    def toggle_on_top(self, value):
        self.wm_attributes("-topmost", value)
        self.settings["always_on_top"] = value
        
    def add_alarm(self):
        alarm_time = self.alarm_entry.get()
        if len(alarm_time) == 5 and alarm_time[2] == ':' and alarm_time[:2].isdigit() and alarm_time[3:].isdigit():
            if alarm_time not in self.settings["alarms"]:
                self.settings["alarms"].append(alarm_time)
                self.settings["alarms"].sort()
                self.update_alarms_display()
                self.alarm_entry.delete(0, 'end')
        else:
            print("Formato de alarme inválido. Use HH:MM")

    def remove_alarm(self, alarm_time, from_thread=False):
        if alarm_time in self.settings["alarms"]:
            self.settings["alarms"].remove(alarm_time)
            if not from_thread: self.update_alarms_display()

    def update_alarms_display(self):
        for widget in self.alarms_list_frame.winfo_children(): widget.destroy()
        for alarm in self.settings["alarms"]:
            frame = ctk.CTkFrame(self.alarms_list_frame)
            label = ctk.CTkLabel(frame, text=alarm, font=ctk.CTkFont(size=16))
            label.pack(side="left", padx=10, pady=5)
            remove_btn = ctk.CTkButton(frame, text="Remover", width=80, command=lambda t=alarm: self.remove_alarm(t))
            remove_btn.pack(side="right", padx=10)
            frame.pack(fill="x", pady=2)

    def start_stopwatch(self): self.stopwatch_running = True
    def pause_stopwatch(self): self.stopwatch_running = False
    def reset_stopwatch(self): 
        self.stopwatch_running = False; self.stopwatch_time = 0.0

    def start_timer(self):
        if not self.timer_running or self.timer_time_left == 0:
            try:
                mins = int(self.timer_min_entry.get() or 0)
                secs = int(self.timer_sec_entry.get() or 0)
                self.timer_time_left = (mins * 60) + secs
                self.timer_running = True
            except ValueError: print("Por favor, insira números válidos para o timer.")
    def pause_timer(self): self.timer_running = False
    def reset_timer(self):
        self.timer_running = False; self.timer_time_left = 0.0

# ==============================================================================
#  5. PONTO DE ENTRADA DA APLICAÇÃO (Execução)
# ==============================================================================
if __name__ == "__main__":
    # Tenta configurar o idioma para Português para exibir a data corretamente
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
        except locale.Error:
            print("Locale pt_BR não foi encontrado. A data pode aparecer em inglês.")

    app = DigitalClockApp()
    app.mainloop()
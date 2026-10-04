import tkinter as tk
from tkinter import ttk, messagebox
from time import strftime


class ClockStopwatchApp:
    BG = "#1e1e2e"
    FG = "#cdd6f4"
    ACCENT = "#89b4fa"
    GREEN = "#a6e3a1"
    RED = "#f38ba8"
    YELLOW = "#f9e2af"
    MAUVE = "#cba6f7"
    BTN_BG = "#313244"
    BTN_ACTIVE = "#45475a"

    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock & Stopwatch")
        self.root.geometry("560x540")
        self.root.configure(bg=self.BG)
        self.root.resizable(False, False)

        self._setup_style()

        self.notebook = ttk.Notebook(self.root, style="Dark.TNotebook")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        clock_tab = ttk.Frame(self.notebook, style="Dark.TFrame")
        timer_tab = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.notebook.add(clock_tab, text="  Clock & Stopwatch  ")
        self.notebook.add(timer_tab, text="  Countdown Timer  ")

        self.running = False
        self.elapsed_ms = 0

        self._build_clock_section(clock_tab)
        self._build_separator(clock_tab)
        self._build_stopwatch_section(clock_tab)
        self._build_stopwatch_buttons(clock_tab)

        self.countdown = CountdownTimer(timer_tab, self)

        self._tick_clock()

    def _setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("default")
        except tk.TclError:
            pass
        style.configure("Dark.TNotebook", background=self.BG, borderwidth=0)
        style.configure("Dark.TFrame", background=self.BG)
        style.configure(
            "Dark.TNotebook.Tab",
            background=self.BTN_BG, foreground=self.FG,
            padding=[24, 10], font=("Segoe UI", 11, "bold"),
            borderwidth=0,
        )
        style.map(
            "Dark.TNotebook.Tab",
            background=[("selected", self.ACCENT)],
            foreground=[("selected", self.BG)],
        )

    def _build_clock_section(self, parent):
        tk.Label(
            parent, text="CURRENT TIME", font=("Segoe UI", 12, "bold"),
            bg=self.BG, fg=self.ACCENT,
        ).pack(pady=(24, 4))

        self.clock_label = tk.Label(
            parent, font=("Consolas", 44, "bold"),
            bg=self.BG, fg=self.FG,
        )
        self.clock_label.pack(pady=(0, 8))

        self.date_label = tk.Label(
            parent, font=("Segoe UI", 12),
            bg=self.BG, fg=self.YELLOW,
        )
        self.date_label.pack()

    def _build_separator(self, parent):
        tk.Frame(parent, bg=self.ACCENT, height=2, width=440).pack(pady=14)

    def _build_stopwatch_section(self, parent):
        tk.Label(
            parent, text="STOPWATCH", font=("Segoe UI", 12, "bold"),
            bg=self.BG, fg=self.GREEN,
        ).pack(pady=(0, 4))

        self.stopwatch_label = tk.Label(
            parent, text="00:00:00.00", font=("Consolas", 36, "bold"),
            bg=self.BG, fg=self.FG,
        )
        self.stopwatch_label.pack(pady=(0, 16))

    def _build_stopwatch_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg=self.BG)
        btn_frame.pack()

        self.start_btn = self._make_button(
            btn_frame, "START", self.GREEN, self.start_stopwatch
        )
        self.start_btn.grid(row=0, column=0, padx=8)
        self.stop_btn = self._make_button(
            btn_frame, "STOP", self.RED, self.stop_stopwatch
        )
        self.stop_btn.grid(row=0, column=1, padx=8)
        self.reset_btn = self._make_button(
            btn_frame, "RESET", self.YELLOW, self.reset_stopwatch
        )
        self.reset_btn.grid(row=0, column=2, padx=8)

    def _make_button(self, parent, text, color, command):
        return tk.Button(
            parent, text=text, font=("Segoe UI", 12, "bold"),
            width=8, bg=color, fg=self.BG, activebackground=self.BTN_ACTIVE,
            activeforeground=color, relief="flat", cursor="hand2",
            command=command,
        )

    def _tick_clock(self):
        self.clock_label.config(text=strftime("%H:%M:%S"))
        self.date_label.config(text=strftime("%A, %d %B %Y"))
        self.root.after(1000, self._tick_clock)

    def _run_stopwatch(self):
        if self.running:
            self.elapsed_ms += 50
            self._update_stopwatch_display()
            self.root.after(50, self._run_stopwatch)

    def _update_stopwatch_display(self):
        ms = self.elapsed_ms
        hours = ms // 3600000
        minutes = (ms % 3600000) // 60000
        seconds = (ms % 60000) // 1000
        centis = (ms % 1000) // 10
        self.stopwatch_label.config(
            text=f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centis:02d}"
        )

    def start_stopwatch(self):
        if not self.running:
            self.running = True
            self._run_stopwatch()

    def stop_stopwatch(self):
        self.running = False

    def reset_stopwatch(self):
        self.running = False
        self.elapsed_ms = 0
        self._update_stopwatch_display()


class CountdownTimer:
    def __init__(self, parent, app):
        self.app = app
        self.root = app.root
        self.BG = app.BG
        self.FG = app.FG
        self.ACCENT = app.ACCENT
        self.GREEN = app.GREEN
        self.RED = app.RED
        self.YELLOW = app.YELLOW
        self.MAUVE = app.MAUVE
        self.BTN_BG = app.BTN_BG

        self.running = False
        self.remaining = 0
        self.set_minutes = tk.IntVar(value=1)
        self.set_seconds = tk.IntVar(value=0)
        self._flash_job = None
        self._tick_job = None

        self._build(parent)

    def _build(self, parent):
        tk.Label(
            parent, text="COUNTDOWN TIMER", font=("Segoe UI", 14, "bold"),
            bg=self.BG, fg=self.MAUVE,
        ).pack(pady=(28, 10))

        set_frame = tk.Frame(parent, bg=self.BG)
        set_frame.pack(pady=(0, 16))

        tk.Label(
            set_frame, text="Minutes", font=("Segoe UI", 10),
            bg=self.BG, fg=self.FG,
        ).grid(row=0, column=0, padx=10)
        tk.Label(
            set_frame, text="Seconds", font=("Segoe UI", 10),
            bg=self.BG, fg=self.FG,
        ).grid(row=0, column=1, padx=10)

        self.min_spin = tk.Spinbox(
            set_frame, from_=0, to=59, width=5, font=("Consolas", 16, "bold"),
            textvariable=self.set_minutes, justify="center",
            bg=self.BTN_BG, fg=self.FG, buttonbackground=self.ACCENT,
            relief="flat", highlightthickness=0,
        )
        self.min_spin.grid(row=1, column=0, padx=10, pady=6)

        self.sec_spin = tk.Spinbox(
            set_frame, from_=0, to=59, width=5, font=("Consolas", 16, "bold"),
            textvariable=self.set_seconds, justify="center",
            bg=self.BTN_BG, fg=self.FG, buttonbackground=self.ACCENT,
            relief="flat", highlightthickness=0,
        )
        self.sec_spin.grid(row=1, column=1, padx=10, pady=6)

        self.display_label = tk.Label(
            parent, text="01:00", font=("Consolas", 56, "bold"),
            bg=self.BG, fg=self.FG,
        )
        self.display_label.pack(pady=(8, 8))

        self.alert_label = tk.Label(
            parent, text="", font=("Segoe UI", 16, "bold"),
            bg=self.BG, fg=self.RED,
        )
        self.alert_label.pack(pady=(0, 12))

        btn_frame = tk.Frame(parent, bg=self.BG)
        btn_frame.pack()

        self.start_btn = self._make_button(
            btn_frame, "START", self.GREEN, self.start
        )
        self.start_btn.grid(row=0, column=0, padx=8)
        self.pause_btn = self._make_button(
            btn_frame, "PAUSE", self.YELLOW, self.pause
        )
        self.pause_btn.grid(row=0, column=1, padx=8)
        self.reset_btn = self._make_button(
            btn_frame, "RESET", self.RED, self.reset
        )
        self.reset_btn.grid(row=0, column=2, padx=8)

        self._update_display_from_inputs()

    def _make_button(self, parent, text, color, command):
        return tk.Button(
            parent, text=text, font=("Segoe UI", 12, "bold"),
            width=8, bg=color, fg=self.BG, activebackground="#45475a",
            activeforeground=color, relief="flat", cursor="hand2",
            command=command,
        )

    def _total_seconds(self):
        try:
            m = int(self.set_minutes.get())
            s = int(self.set_seconds.get())
        except (tk.TclError, ValueError):
            return 0
        m = max(0, min(59, m))
        s = max(0, min(59, s))
        return m * 60 + s

    def _format(self, secs):
        secs = max(0, secs)
        return f"{secs // 60:02d}:{secs % 60:02d}"

    def _update_display_from_inputs(self):
        self.display_label.config(
            text=self._format(self._total_seconds()), fg=self.FG
        )

    def _update_display(self):
        self.display_label.config(text=self._format(self.remaining))

    def start(self):
        if self.running:
            return
        if self.remaining <= 0:
            self.remaining = self._total_seconds()
        if self.remaining <= 0:
            self.alert_label.config(text="Set a time greater than 0!", fg=self.YELLOW)
            return
        self.alert_label.config(text="", fg=self.RED)
        self.display_label.config(fg=self.FG)
        self.running = True
        self._tick()

    def _tick(self):
        if not self.running:
            return
        self._update_display()
        if self.remaining <= 0:
            self.running = False
            self._trigger_alert()
            return
        self.remaining -= 1
        if self.remaining <= 10:
            self.display_label.config(fg=self.YELLOW)
        self._tick_job = self.root.after(1000, self._tick)

    def pause(self):
        if self.running:
            self.running = False
            if self._tick_job is not None:
                self.root.after_cancel(self._tick_job)
                self._tick_job = None
            self.alert_label.config(text="PAUSED", fg=self.ACCENT)

    def reset(self):
        self.running = False
        if self._tick_job is not None:
            self.root.after_cancel(self._tick_job)
            self._tick_job = None
        if self._flash_job is not None:
            self.root.after_cancel(self._flash_job)
            self._flash_job = None
        self.remaining = 0
        self.alert_label.config(text="", fg=self.RED)
        self._update_display_from_inputs()

    def _trigger_alert(self):
        self.display_label.config(text="00:00", fg=self.RED)
        self.alert_label.config(text="⏰  TIME'S UP!  ⏰", fg=self.RED)
        try:
            self.root.bell()
        except tk.TclError:
            pass
        self._flash_state = 0
        self._flash()

    def _flash(self):
        if self._flash_state >= 12:
            return
        if self._flash_state % 2 == 0:
            self.display_label.config(fg=self.RED)
            self.alert_label.config(fg=self.RED)
        else:
            self.display_label.config(fg=self.YELLOW)
            self.alert_label.config(fg=self.YELLOW)
        self._flash_state += 1
        self._flash_job = self.root.after(400, self._flash)


def main():
    root = tk.Tk()
    ClockStopwatchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

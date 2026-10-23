"""GUI на tkinter."""
import tkinter as tk

class ShellApp:
    """Окно эмулятора."""

    def __init__(self, shell, title: str):
        self.shell = shell
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("800x600")

        self.output = tk.Text(self.root, state="disabled", bg="black", fg="white")
        self.output.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.root, bg="black", fg="white")
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_submit)
        self.root.bind("<Control-c>", self.on_exit)

    def echo(self, text: str) -> None:
        """Добавляет строку в вывод."""
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def on_submit(self, _event) -> None:
        """Обработка Enter."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.echo(f"> {line}")
        try:
            result = self.shell.execute(line)
            if result:
                self.echo(result)
        except SystemExit:
            self.root.destroy()
        except Exception as exc:
            self.echo(f"error: {exc}")

    def on_exit(self, _event) -> None:
        """Ctrl+C."""
        self.root.destroy()

    def run(self) -> None:
        """Запуск главного цикла."""
        self.root.mainloop()

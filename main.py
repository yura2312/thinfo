from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Tab, TabPane, TabbedContent, Tabs

from pages.resume import ResumePage


class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "main.css"
    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="resume"):
            
            with TabPane("Geral", id="resume"):
                yield ResumePage()

            with TabPane("Cache", id="cache"):
                pass

            with TabPane("Placa mãe", id="motherboard"):
                pass

            with TabPane("CPU", id="cpu"):
                pass

            with TabPane("RAM", id="ram"):
                pass

            with TabPane("Memoria Sec.", id="storage"):
                pass


        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def on_mount(self) -> None:
        self.title = "THInfo"
        self.sub_title = "Terminal Hardware Info"

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
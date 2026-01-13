import json
import pyperclip
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, ListView, ListItem, Label, Static, Input
from textual.notifications import Notify
from rich.syntax import Syntax

# --- 1. Data Loader ---
def load_snippets():
    try:
        with open("snippet.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

class SnippetVaultApp(App):
    """A Textual app to manage, search, and copy code snippets."""

    CSS = """
    Screen {
        layout: horizontal;
    }

    #sidebar {
        dock: left;
        width: 30%;
        height: 100%;
        border-right: solid green;
        background: $surface;
    }

    #search-box {
        dock: top;
        margin: 1;
        background: $boost;
    }

    #code-container {
        width: 70%;
        height: 100%;
        padding: 2;
    }

    ListView {
        height: 100%;
    }

    ListItem {
        padding: 1;
    }

    ListItem:hover {
        background: $accent;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Dark Mode"),
        ("c", "copy_snippet", "Copy Code"), 
    ]

    def __init__(self):
        super().__init__()
        self.snippets_data = load_snippets()
        self.current_snippet_code = "" # Tracks what is currently on screen

    def compose(self) -> ComposeResult:
        yield Header()
        
        # Left Sidebar
        with Vertical(id="sidebar"):
            yield Input(placeholder="Search snippets...", id="search-box")
            yield ListView(id="snippet-list")

        # Right Code Area
        with Container(id="code-container"):
            yield Static("Select a snippet...", id="code-view")

        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts. Load the initial list."""
        self.populate_list(self.snippets_data)

    def populate_list(self, data_dict):
        """Helper to clear and refill the list view."""
        list_view = self.query_one("#snippet-list")
        list_view.clear()
        
        for title in data_dict.keys():
            # Store the title in the ListItem's ID so we can look it up later
            list_view.append(ListItem(Label(title), name=title))

    def on_input_changed(self, event: Input.Changed) -> None:
        """Called immediately when user types in the search box."""
        search_term = event.value.lower()
        
        # Filter dictionary keys based on search term
        filtered_data = {
            k: v for k, v in self.snippets_data.items() 
            if search_term in k.lower()
        }
        self.populate_list(filtered_data)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """When user presses Enter on a list item."""
        snippet_name = event.item.name
        data = self.snippets_data.get(snippet_name)
        
        if data:
            self.current_snippet_code = data["code"]
            
            # Render syntax highlighting
            syntax = Syntax(
                data["code"],
                data["lang"],
                theme="monokai",
                line_numbers=True,
                word_wrap=True
            )
            self.query_one("#code-view").update(syntax)

    def action_copy_snippet(self) -> None:
        """Action bound to 'c' key."""
        if self.current_snippet_code:
            pyperclip.copy(self.current_snippet_code)
            # Show a toast notification (Textual feature!)
            self.notify("Code copied to clipboard!", title="Success", severity="information")
        else:
            self.notify("No snippet selected.", title="Error", severity="error")

if __name__ == "__main__":
    app = SnippetVaultApp()
    app.run()
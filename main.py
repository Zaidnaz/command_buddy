from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, ListView, ListItem, Label, Static
from rich.syntax import Syntax

# --- 1. The Data ---
# A simple dictionary to store our snippets. 
# In the future, this could load from a JSON or CSV file.
SNIPPETS = {
    "Python: HTTP Server": {
        "lang": "python",
        "code": "python -m http.server 8000\n# Serves the current directory on port 8000"
    },
    "Git: Undo Last Commit": {
        "lang": "bash",
        "code": "git reset --soft HEAD~1\n# Undoes the commit but keeps your changes staged"
    },
    "Docker: Remove All Containers": {
        "lang": "bash",
        "code": "docker rm $(docker ps -a -q)\n# Force remove all stopped containers"
    },
    "JS: Console Table": {
        "lang": "javascript",
        "code": "console.table(data);\n// Displays array of objects as a neat table"
    },
    "SQL: Select Unique": {
        "lang": "sql",
        "code": "SELECT DISTINCT column_name FROM table_name;"
    }
}

# --- 2. The Widgets ---

class SnippetList(ListView):
    """A widget to display the list of selectable snippets."""
    pass

class CodeView(Static):
    """A widget to display the syntax-highlighted code."""
    pass

# --- 3. The Main Application ---

class SnippetVaultApp(App):
    """A Textual app to manage code snippets."""

    # CSS styles to layout the app (Looks like CSS, works in Terminal)
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

    #sidebar-title {
        text-align: center;
        background: $primary;
        color: auto;
        padding: 1;
        text-style: bold;
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
        ("d", "toggle_dark", "Toggle Dark Mode"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        # Left Sidebar container
        with Vertical(id="sidebar"):
            yield Label("VAULT CONTENTS", id="sidebar-title")
            
            # Create a ListItem for each snippet in our dictionary
            items = [ListItem(Label(title), name=title) for title in SNIPPETS.keys()]
            yield SnippetList(*items)

        # Right Code View container
        with Container(id="code-container"):
            yield CodeView("Select a snippet from the left to view code...", id="code-view")

        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Called when the user clicks or presses Enter on a list item."""
        # Get the name of the selected item
        snippet_name = event.item.name
        
        # Retrieve data from our dictionary
        data = SNIPPETS.get(snippet_name)
        
        if data:
            # Create a Rich Syntax object for beautiful highlighting
            syntax_view = Syntax(
                data["code"],
                data["lang"],
                theme="monokai",
                line_numbers=True,
                word_wrap=True
            )
            # Update the CodeView widget
            self.query_one("#code-view").update(syntax_view)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = SnippetVaultApp()
    app.run()
"""
main.py
Numerical Analysis Solver — main entry point.

Run:
    python main.py
"""

import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.dirname(__file__))

import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.home_page import HomePage
from ui.root_page import RootPage
from ui.interpolation_page import InterpolationPage
from ui.integration_page import IntegrationPage
from ui.differential_page import DifferentialPage
from ui.regression_page import RegressionPage
from ui.about_page import AboutPage

# ── Global appearance ─────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_MAIN   = "#0d1117"
BG_HEADER = "#010409"
ACCENT    = "#00b4d8"
TEXT_PRI  = "#e6edf3"
TEXT_SEC  = "#8b949e"


class App(ctk.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.title("Numerical Analysis Solver")
        self.geometry("1200x750")
        self.minsize(900, 620)
        self.configure(fg_color=BG_MAIN)

        # Try to set a nice icon (skip if unavailable)
        try:
            self.iconbitmap("")
        except Exception:
            pass

        self._pages: dict[str, ctk.CTkFrame] = {}
        self._current: str | None = None
        self._build_layout()

    def _build_layout(self):
        """Build sidebar + header + content area layout."""
        # Top header bar
        header = ctk.CTkFrame(self, fg_color=BG_HEADER, height=48, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="  📐 Numerical Analysis Solver",
            text_color=ACCENT,
            font=ctk.CTkFont(family="Courier New", size=15, weight="bold"),
            anchor="w",
        ).pack(side="left", padx=16, fill="y")

        ctk.CTkLabel(
            header,
            text="University Course Project  •  Dark Mode",
            text_color=TEXT_SEC,
            font=ctk.CTkFont(size=11),
        ).pack(side="right", padx=16, fill="y")

        # Body row: sidebar + main
        body = ctk.CTkFrame(self, fg_color=BG_MAIN)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # Sidebar
        sidebar = Sidebar(body, on_navigate=self._navigate)
        sidebar.grid(row=0, column=0, sticky="nsew")
        self._sidebar = sidebar

        # Content container
        self._content = ctk.CTkFrame(body, fg_color=BG_MAIN, corner_radius=0)
        self._content.grid(row=0, column=1, sticky="nsew")
        self._content.rowconfigure(0, weight=1)
        self._content.columnconfigure(0, weight=1)

        # Instantiate all pages (lazy-packing)
        self._pages = {
            "Home":            HomePage(self._content),
            "Root Finding":    RootPage(self._content),
            "Interpolation":   InterpolationPage(self._content),
            "Integration":     IntegrationPage(self._content),
            "Differential Eq.": DifferentialPage(self._content),
            "Regression":      RegressionPage(self._content),
            "About":           AboutPage(self._content),
        }

        # Navigate to Home
        self._navigate("Home")
        sidebar.set_active("Home")

    def _navigate(self, page_name: str):
        """Switch visible page."""
        if self._current:
            self._pages[self._current].grid_remove()

        page = self._pages.get(page_name)
        if page:
            page.grid(row=0, column=0, sticky="nsew")
            self._current = page_name


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

"""
ui/sidebar.py
Left sidebar with navigation buttons.
"""

from __future__ import annotations
import customtkinter as ctk

BG_SIDEBAR = "#010409"
BG_BTN = "#161b22"
BG_ACTIVE = "#0d419d"
TEXT_PRI = "#e6edf3"
TEXT_SEC = "#8b949e"
ACCENT = "#00b4d8"

NAV_ITEMS = [("🏠", "Home"), ("🔍", "Root Finding"), ("📐", "Interpolation"), ("∫", "Integration"), ("📈", "Differential Eq."), ("📊", "Regression"), ("ℹ️", "About")]


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, on_navigate, **kwargs):
        super().__init__(parent, fg_color=BG_SIDEBAR, width=210, corner_radius=0, **kwargs)
        self.on_navigate = on_navigate
        self._buttons = {}
        self._active = None
        self._build()

    def _build(self):
        self.grid_propagate(False)
        logo_frame = ctk.CTkFrame(self, fg_color="#010409")
        logo_frame.pack(fill="x", pady=(20, 10), padx=12)
        ctk.CTkLabel(logo_frame, text="📐 NumSolver", text_color=ACCENT, font=ctk.CTkFont(family="Courier New", size=16, weight="bold"), anchor="w").pack(fill="x")
        ctk.CTkLabel(logo_frame, text="Numerical Analysis Suite", text_color=TEXT_SEC, font=ctk.CTkFont(size=10), anchor="w").pack(fill="x")
        ctk.CTkFrame(self, fg_color="#21262d", height=1).pack(fill="x", padx=10, pady=8)
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=8)
        for icon, name in NAV_ITEMS:
            btn = ctk.CTkButton(nav_frame, text=f"  {icon}   {name}", anchor="w", height=42, corner_radius=8, fg_color=BG_BTN, hover_color="#1f2937", text_color=TEXT_PRI, font=ctk.CTkFont(size=13), command=lambda n=name: self._click(n))
            btn.pack(fill="x", pady=3)
            self._buttons[name] = btn
        ctk.CTkFrame(self, fg_color="#21262d", height=1).pack(fill="x", padx=10, side="bottom", pady=8)
        ctk.CTkLabel(self, text="v1.0.0  •  Numerical Analysis", text_color=TEXT_SEC, font=ctk.CTkFont(size=9)).pack(side="bottom", pady=(0, 10))

    def _click(self, name: str):
        self._set_active(name)
        self.on_navigate(name)

    def _set_active(self, name: str):
        if self._active and self._active in self._buttons:
            self._buttons[self._active].configure(fg_color=BG_BTN, text_color=TEXT_PRI)
        self._active = name
        if name in self._buttons:
            self._buttons[name].configure(fg_color=BG_ACTIVE, text_color="#ffffff")

    def set_active(self, name: str):
        self._set_active(name)

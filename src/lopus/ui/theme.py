"""Tema visual inicial do painel local."""

from nicegui import ui


def apply_theme() -> None:
    ui.colors(primary="#2563eb", secondary="#0f172a", accent="#38bdf8", positive="#16a34a", negative="#dc2626", warning="#f59e0b")
    ui.add_head_html("""
        <style>
            body { background: #070b14; color: #e5e7eb; }
            .lopus-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; }
            .lopus-muted { color: #94a3b8; }
            .lopus-title { letter-spacing: -0.02em; }
        </style>
    """)

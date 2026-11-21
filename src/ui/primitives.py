import html
import streamlit as st

def get_badge_html(text: str, variant: str = "default", icon: str = "") -> str:
    """Returns HTML for a Sky/Slate Studio pill badge (.dad-badge)."""
    variant_class = ""
    if variant in ("audio", "video", "image", "amber"):
        variant_class = f"dad-badge-{variant}"
    
    icon_html = f'<span class="material-symbols-rounded" style="font-size:0.95rem;">{html.escape(icon)}</span> ' if icon else ""
    return f'<span class="dad-badge {variant_class}">{icon_html}{html.escape(text)}</span>'

def render_badge(text: str, variant: str = "default", icon: str = "") -> None:
    """Renders a standalone pill badge in Streamlit."""
    st.markdown(get_badge_html(text, variant=variant, icon=icon), unsafe_allow_html=True)

def render_micro_card(
    title: str,
    subtitle: str,
    badge_text: str = "",
    badge_variant: str = "default",
    icon: str = ""
) -> None:
    """Renders the top summary micro-card (.dad-micro-card)."""
    icon_html = f'<span class="material-symbols-rounded" style="color:var(--primary);font-size:1.25rem;">{html.escape(icon)}</span> ' if icon else ""
    badge_html = get_badge_html(badge_text, variant=badge_variant) if badge_text else ""
    
    card_html = f"""
    <div class="dad-micro-card">
      <div>
        <p class="dad-micro-title">{icon_html}{html.escape(title)}</p>
        <p class="dad-micro-sub">{html.escape(subtitle)}</p>
      </div>
      {badge_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_step_bar(steps: list[str], active_index: int = 0) -> None:
    """
    Renders a responsive 3-column progress step bar (.dad-step-bar).
    
    :param steps: List of step labels (e.g., ["Pegar URL", "Configurar", "Descargar"]).
    :param active_index: 0-based index of the currently active step.
    """
    items_html = []
    for idx, label in enumerate(steps):
        if idx < active_index:
            state_class = "done"
            num_display = "✓"
        elif idx == active_index:
            state_class = "active"
            num_display = str(idx + 1)
        else:
            state_class = ""
            num_display = str(idx + 1)
            
        items_html.append(f"""
        <div class="dad-step-item {state_class}">
          <span class="dad-step-num">{num_display}</span>
          <span class="dad-step-label">{html.escape(label)}</span>
        </div>
        """)
    
    bar_html = f'<div class="dad-step-bar">{"".join(items_html)}</div>'
    st.markdown(bar_html, unsafe_allow_html=True)

def render_amber_callout(title: str, items: list[str], icon: str = "center_focus_strong") -> None:
    """Renders a high-visibility amber callout banner (.dad-callout)."""
    header_icon = f'<span class="material-symbols-rounded">{html.escape(icon)}</span>' if icon else ""
    
    item_rows = []
    for idx, item in enumerate(items, start=1):
        item_rows.append(f"""
        <div class="dad-callout-item">
          <span class="dad-callout-num">{idx}</span>
          <span>{html.escape(item)}</span>
        </div>
        """)
    
    callout_html = f"""
    <div class="dad-callout">
      <div class="dad-callout-header">
        {header_icon}
        <span>{html.escape(title)}</span>
      </div>
      {"".join(item_rows)}
    </div>
    """
    st.markdown(callout_html, unsafe_allow_html=True)

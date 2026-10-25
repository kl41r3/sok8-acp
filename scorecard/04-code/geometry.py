"""Workshop scorecard geometry; inputs and output paths are supplied by plot.py."""
def fig_scorecard():
    names = [p[0] for p in D.PROTOCOLS]
    scores = np.array([p[3] for p in D.PROTOCOLS], dtype=float)
    totals = np.array([p[4] for p in D.PROTOCOLS], dtype=float)
    origins = [p[2] for p in D.PROTOCOLS]
    mat = np.concatenate([scores, totals[:, None]], axis=1)
    fig = new_fig(W, 2.95)
    ax = fig.add_axes([0.22, 0.2, 0.76, 0.74])
    score_fill = {0.5: C['gold'], 1.0: C['mint'], 1.5: C['blue'], 2.0: C['wine']}
    score_fg = {0.5: C['ink'], 1.0: C['ink'], 1.5: C['paper'], 2.0: C['paper']}
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(7.5, -0.5)
    for i in range(scores.shape[0]):
        for j in range(scores.shape[1]):
            v = float(scores[i, j])
            ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=score_fill[v], edgecolor=C['paper'], linewidth=1.0))
            ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=9, color=score_fg[v])
        ax.add_patch(Rectangle((4.5, i - 0.5), 1, 1, facecolor=mix(ORIGIN_COLOR[origins[i]], 0.55), edgecolor='white', linewidth=1.0))
        ax.text(5, i, f'{totals[i]:.1f}', ha='center', va='center', fontsize=9, fontweight='bold', color=C['ink'])
    ax.set_xticks(list(range(5)) + [5])
    ax.set_xticklabels(list(D.SCORE_DIMS) + ['Σ'], fontsize=9)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    for tick, origin in zip(ax.get_yticklabels(), origins):
        tick.set_color(ORIGIN_COLOR[origin])
        tick.set_fontweight('bold')
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.add_patch(Rectangle((-0.5, 6.5), 6, 1, fill=False, edgecolor=C['wine'], linewidth=1.2))
    handles = [Patch(facecolor=C['gold'], edgecolor=C['ink'], linewidth=0.4, label='0.5'), Patch(facecolor=C['mint'], edgecolor=C['ink'], linewidth=0.4, label='1.0'), Patch(facecolor=C['blue'], edgecolor=C['ink'], linewidth=0.4, label='1.5'), Patch(facecolor=C['wine'], edgecolor=C['ink'], linewidth=0.4, label='2.0'), Patch(facecolor=C['coral'], edgecolor=C['ink'], linewidth=0.4, label='Web2'), Patch(facecolor=C['blue'], edgecolor=C['ink'], linewidth=0.4, label='Web3')]
    ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=6, fontsize=7.4, handletextpad=0.28, columnspacing=0.7)
    fig.text(0.22, 0.005, 'Human-adjudicated 0–2 lock. Kleros scored as stack L8.', fontsize=7.5, color=C['muted'], style='italic')
    save(fig, '04_protocol_scorecard')
_RADAR_TH = np.deg2rad([90.0, 162.0, 234.0, 306.0, 18.0])
_RADAR_LABS = (('C', 'center', 'bottom', 2.06, 0.0, 0.03), ('I', 'right', 'center', 2.26, -0.12, 0.02), ('A', 'right', 'top', 2.2, -0.04, -0.06), ('EM', 'left', 'top', 2.2, 0.04, -0.06), ('S', 'left', 'center', 2.26, 0.12, 0.02))

def _radar_xy(radii):
    r = np.asarray(radii, dtype=float)
    x = r * np.cos(_RADAR_TH)
    y = r * np.sin(_RADAR_TH)
    return (np.r_[x, x[0]], np.r_[y, y[0]])

def _radar_grid(ax, lim=2.7, lab_size=7.4, labs=_RADAR_LABS):
    """Hairline pentagon frame. Regular axes, not polar, so there is no circular spine."""
    ax.set_aspect('equal')
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.axis('off')
    ax.set_facecolor(C['paper'])
    for r in (0.5, 1.0, 1.5):
        gx, gy = _radar_xy([r] * 5)
        ax.plot(gx, gy, color=C['grid'], lw=0.32, solid_joinstyle='round', zorder=1)
    ox, oy = _radar_xy([2.0] * 5)
    ax.plot(ox, oy, color=C['rule'], lw=0.42, solid_joinstyle='round', zorder=1)
    for th in _RADAR_TH:
        ax.plot([0.0, 2.0 * np.cos(th)], [0.0, 2.0 * np.sin(th)], color=C['grid'], lw=0.28, zorder=1)
    for th, (lab, ha, va, rr, dx, dy) in zip(_RADAR_TH, labs):
        ax.text(rr * np.cos(th) + dx, rr * np.sin(th) + dy, lab, ha=ha, va=va, fontsize=lab_size, fontweight='bold', color=C['ink'], zorder=8, clip_on=False)

def _radar_series(ax, values, color, ls='-', marker='o', lw=1.05, fill_alpha=0.1, z=3):
    x, y = _radar_xy(values)
    ax.fill(x, y, color=color, alpha=fill_alpha, zorder=z)
    ax.plot(x, y, color=color, lw=lw, ls=ls, solid_joinstyle='round', solid_capstyle='round', zorder=z + 1)
    ax.plot(x[:-1], y[:-1], linestyle='none', marker=marker, markersize=3.0, color=color, markerfacecolor=color, markeredgecolor=C['paper'], markeredgewidth=0.35, zorder=z + 2, clip_on=False)

def _radar_panel(ax, values, color, dashed=False):
    _radar_grid(ax, lim=2.62, lab_size=7.0)
    ls = (0, (3.2, 1.5)) if dashed else '-'
    _radar_series(ax, values, color, ls=ls, fill_alpha=0.15)

def fig_radars():
    """Two stacked rows of four. Eight across one row crowds the five axis labels."""
    fig = new_fig(W_FULL, 3.28)
    gs = fig.add_gridspec(2, 4, left=0.015, right=0.985, top=0.868, bottom=0.092, wspace=0.11, hspace=0.46)
    axes = []
    for i, proto in enumerate(D.PROTOCOLS):
        name, layer, origin, vals, total = proto
        ax = fig.add_subplot(gs[i // 4, i % 4])
        color = ORIGIN_COLOR[origin]
        _radar_panel(ax, vals, color, dashed=name == 'Kleros')
        axes.append((ax, name, layer, total, color))
    fig.canvas.draw()
    for ax, name, layer, total, color in axes:
        bbox = ax.get_position()
        cx = 0.5 * (bbox.x0 + bbox.x1)
        fig.text(cx, bbox.y1 + 0.048, name, ha='center', va='bottom', fontsize=8.2, fontweight='bold', color=color)
        fig.text(cx, bbox.y1 + 0.022, f'{layer}   Σ {total:.1f}', ha='center', va='bottom', fontsize=6.4, color=C['muted'])
    fig.text(0.015, 0.016, 'Human-adjudicated 0–2 lock.  C coherence · I interoperability · A assurance · EM emerging-market fitness · S standardization.  Kleros is dashed as a stack L8 candidate.', fontsize=6.6, color=C['muted'])
    save(fig, '05_protocol_radars')

def _ink_shade(hex_color: str, ink_w: float) -> str:
    r, g, b = to_rgb(hex_color)
    ir, ig, ib = to_rgb(C['ink'])
    r = r * (1 - ink_w) + ir * ink_w
    g = g * (1 - ink_w) + ig * ink_w
    b = b * (1 - ink_w) + ib * ink_w
    return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
_GOLD_INK = _ink_shade(C['gold'], 0.28)
_WEB2_COLOR = {'AP2': (C['coral'], C['coral']), 'UCP': (C['wine'], C['wine']), 'MCP': (C['mint'], C['mint']), 'A2A': (C['blue'], C['blue']), 'AG-UI': (_GOLD_INK, C['gold'])}
_WEB3_COLOR = {'x402': (C['blue'], C['blue']), 'ERC-8004': (C['coral'], C['coral']), 'Kleros': (C['wine'], C['wine'])}
_OVERLAY_LABS = (('C', 'center', 'bottom', 2.08, 0.0, 0.04), ('I', 'right', 'center', 2.16, -0.06, 0.02), ('A', 'right', 'top', 2.14, -0.02, -0.05), ('EM', 'left', 'top', 2.14, 0.02, -0.05), ('S', 'right', 'bottom', 2.06, -0.02, 0.08))

def _draw_overlay(ax, names, colors, fill_alpha):
    _radar_grid(ax, lim=2.42, lab_size=7.4, labs=_OVERLAY_LABS)
    by_name = {p[0]: p for p in D.PROTOCOLS}
    for name in names:
        vals = by_name[name][3]
        stroke, fill = colors[name]
        ls = (0, (3.2, 1.5)) if name == 'Kleros' else '-'
        x, y = _radar_xy(vals)
        ax.fill(x, y, color=fill, alpha=fill_alpha, zorder=2)
        ax.plot(x, y, color=stroke, lw=1.15, ls=ls, solid_joinstyle='round', solid_capstyle='round', zorder=3)
        ax.plot(x[:-1], y[:-1], linestyle='none', marker='o', markersize=2.8, color=stroke, markerfacecolor=stroke, markeredgecolor=C['paper'], markeredgewidth=0.3, zorder=4, clip_on=False)

def _side_key(ax, names, colors, title):
    """Vertical colour key. Compact, no matplotlib legend chrome."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    by_name = {p[0]: p for p in D.PROTOCOLS}
    n = len(names)
    block = 0.11 + n * 0.13
    y0 = 0.5 + block / 2.0
    ax.text(0.0, y0, title, ha='left', va='center', fontsize=8.4, fontweight='bold', color=C['ink'])
    for i, name in enumerate(names):
        y = y0 - 0.13 * (i + 1)
        stroke, _fill = colors[name]
        ls = (0, (3.2, 1.5)) if name == 'Kleros' else '-'
        ax.plot([0.0, 0.22], [y, y], color=stroke, lw=1.45, ls=ls, solid_capstyle='round', clip_on=False)
        ax.plot(0.11, y, linestyle='none', marker='o', markersize=3.4, color=stroke, markerfacecolor=stroke, markeredgecolor=C['paper'], markeredgewidth=0.3, clip_on=False)
        layer = by_name[name][1]
        ax.text(0.3, y, f'{name}  {layer}', ha='left', va='center', fontsize=7.1, color=C['ink'], clip_on=False)

def _origin_strip(width, height, radar_w, key_w, g_in, gap, stacked):
    """Radar–key pairs. Horizontal for the gallery; stacked for the paper column."""
    fig = new_fig(width, height)
    names2 = list(_WEB2_COLOR)
    names3 = list(_WEB3_COLOR)
    if stacked:
        row_h, left, bot = (0.46, 0.01, 0.02)
        top = bot + row_h + 0.04
        ax_r2 = fig.add_axes([left, top, radar_w, row_h])
        ax_k2 = fig.add_axes([left + radar_w + g_in, top, key_w, row_h])
        ax_r3 = fig.add_axes([left, bot, radar_w, row_h])
        ax_k3 = fig.add_axes([left + radar_w + g_in, bot, key_w, row_h])
    else:
        bot, h, x0 = (0.01, 0.98, 0.002)
        ax_r2 = fig.add_axes([x0, bot, radar_w, h])
        x0 += radar_w + g_in
        ax_k2 = fig.add_axes([x0, bot, key_w, h])
        x0 += key_w + gap
        ax_r3 = fig.add_axes([x0, bot, radar_w, h])
        x0 += radar_w + g_in
        ax_k3 = fig.add_axes([x0, bot, key_w, h])
    _draw_overlay(ax_r2, names2, _WEB2_COLOR, fill_alpha=0.08)
    _draw_overlay(ax_r3, names3, _WEB3_COLOR, fill_alpha=0.1)
    _side_key(ax_k2, names2, _WEB2_COLOR, 'Web2')
    _side_key(ax_k3, names3, _WEB3_COLOR, 'Web3')
    return fig

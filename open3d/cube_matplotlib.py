import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
import numpy as np

size = 2.5
RANGE = 15
ax_limit = (-2, RANGE)
GIZMO_LEN = 3.0

initial_origins = [
    np.array([0, 0, 0], dtype=float),
    np.array([5, 0, 0], dtype=float),
    np.array([0, 5, 0], dtype=float),
]
colors = ['lightblue', 'lightgreen', 'lightsalmon']
edge_colors = ['blue', 'green', 'red']

def make_cube_faces(origin, size):
    x0, y0, z0 = origin
    x1, y1, z1 = origin + size
    v = np.array([
        [x0, y0, z0],[x1, y0, z0],[x1, y1, z0],[x0, y1, z0],
        [x0, y0, z1],[x1, y0, z1],[x1, y1, z1],[x0, y1, z1],
    ])
    return [
        [v[0],v[1],v[2],v[3]],[v[4],v[5],v[6],v[7]],
        [v[0],v[1],v[5],v[4]],[v[2],v[3],v[7],v[6]],
        [v[0],v[3],v[7],v[4]],[v[1],v[2],v[6],v[5]],
    ]

def get_cube_vertices(origin, size):
    x0, y0, z0 = origin
    x1, y1, z1 = origin + size
    return np.array([
        [x0, y0, z0],[x1, y0, z0],[x1, y1, z0],[x0, y1, z0],
        [x0, y0, z1],[x1, y0, z1],[x1, y1, z1],[x0, y1, z1],
    ])

fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(*ax_limit); ax.set_ylim(*ax_limit); ax.set_zlim(*ax_limit)
try: ax.set_box_aspect([1,1,1])
except: pass
ax.set_xlabel("X [cm]"); ax.set_ylabel("Y [cm]"); ax.set_zlabel("Z [cm]")
ax.set_title("3 Cubes (2.5cm) + Gizmo\n[Gizmo: axis] [Cube body: XY] [Shift/Right: Z] [Empty: camera] [1/2/3: select]")

cubes = []
for i, origin in enumerate(initial_origins):
    faces = make_cube_faces(origin, size)
    poly = Poly3DCollection(faces, alpha=0.6, edgecolor='black', facecolor=colors[i], linewidths=1)
    ax.add_collection3d(poly)
    cubes.append({'origin': origin.copy(), 'poly': poly, 'color': colors[i], 'edge_selected': edge_colors[i]})

ax.view_init(elev=20, azim=30)

# Gizmo
gizmo_lines = {}
for axis, col in [('x','red'), ('y','green'), ('z','blue')]:
    line, = ax.plot([], [], [], color=col, linewidth=5, alpha=0.95)
    tip, = ax.plot([], [], [], color=col, marker='o', markersize=10, markeredgecolor='black', markeredgewidth=1)
    line.set_visible(False); tip.set_visible(False)
    gizmo_lines[axis] = (line, tip)

status_text = fig.text(0.02, 0.02, "selected: none | click cube or press 1/2/3", fontsize=9, family='monospace',
                       bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))

def update_gizmo(idx):
    if idx is None:
        for a in gizmo_lines:
            l,t = gizmo_lines[a]
            l.set_visible(False); t.set_visible(False)
            l.set_data([],[]); l.set_3d_properties([])
            t.set_data([],[]); t.set_3d_properties([])
        return
    center = cubes[idx]['origin'] + size/2
    dirs = {'x': np.array([1,0,0]), 'y': np.array([0,1,0]), 'z': np.array([0,0,1])}
    for axis, d in dirs.items():
        end = center + d * GIZMO_LEN
        l,t = gizmo_lines[axis]
        l.set_data([center[0], end[0]], [center[1], end[1]])
        l.set_3d_properties([center[2], end[2]])
        t.set_data([end[0]], [end[1]])
        t.set_3d_properties([end[2]])
        l.set_visible(True); t.set_visible(True)

state = {
    'selected': None, 'dragging': False, 'drag_axis': None,
    'drag_mode': 'xy', 'start_xy': None, 'start_origin': None,
    'stored_view': None, 'gizmo_vec': None, 'gizmo_len_px': None,
}

def update_highlight():
    for idx,c in enumerate(cubes):
        if idx == state['selected']:
            c['poly'].set_edgecolor(c['edge_selected']); c['poly'].set_linewidth(2.5); c['poly'].set_alpha(0.9)
        else:
            c['poly'].set_edgecolor('black'); c['poly'].set_linewidth(1); c['poly'].set_alpha(0.6)

def update_status():
    if state['selected'] is None:
        status_text.set_text("selected: none | click cube (bbox) or press 1/2/3 | drag empty: camera")
    else:
        o = cubes[state['selected']]['origin']
        status_text.set_text(f"selected: cube {state['selected']+1} at ({o[0]:.2f}, {o[1]:.2f}, {o[2]:.2f}) | gizmo(R/G/B)=X/Y/Z drag | cube drag=XY | Shift+drag=Z")

def get_cube_center_display(idx):
    origin = cubes[idx]['origin']
    center = origin + size/2
    x2,y2,_ = proj3d.proj_transform(center[0], center[1], center[2], ax.get_proj())
    return ax.transAxes.transform((x2,y2))

def pick_cube(event):
    # 2段階: まずバウンディングボックス内か、次に中心距離
    best_idx = None
    best_dist = float('inf')
    best_inside = False
    for idx in range(len(cubes)):
        verts = get_cube_vertices(cubes[idx]['origin'], size)
        xs, ys = [], []
        try:
            for v in verts:
                x2,y2,_ = proj3d.proj_transform(v[0], v[1], v[2], ax.get_proj())
                sx,sy = ax.transAxes.transform((x2,y2))
                xs.append(sx); ys.append(sy)
            cx,cy = get_cube_center_display(idx)
        except Exception as e:
            continue
        xmin, xmax = min(xs)-8, max(xs)+8
        ymin, ymax = min(ys)-8, max(ys)+8
        inside = (xmin <= event.x <= xmax and ymin <= event.y <= ymax)
        dist = np.hypot(event.x - cx, event.y - cy)
        # 中心距離もbboxサイズで正規化: 大きく見える立方体は拾いやすい
        # bboxの対角線長でスケール
        diag = np.hypot(xmax-xmin, ymax-ymin)
        # insideなら優先、同じinsideならdistが小さい方
        if inside:
            if not best_inside or dist < best_dist:
                best_dist, best_idx, best_inside = dist, idx, True
        else:
            if not best_inside and dist < best_dist:
                best_dist, best_idx = dist, idx
    # 閾値: insideなら80px, outsideなら60pxまで許容
    if best_idx is None:
        return None
    thresh = 80 if best_inside else 60
    if best_dist < thresh:
        return best_idx
    # デバッグ: クリック位置と各中心距離を出力（失敗時のみ）
    # print(f"pick_cube miss: best_idx={best_idx} dist={best_dist:.1f} inside={best_inside} thresh={thresh}")
    return None

def pick_gizmo(event):
    if state['selected'] is None:
        return None
    center = cubes[state['selected']]['origin'] + size/2
    dirs = {'x': np.array([1,0,0]), 'y': np.array([0,1,0]), 'z': np.array([0,0,1])}
    best_axis, best_dist = None, float('inf')
    best_vec, best_len = None, None
    for axis, d in dirs.items():
        end = center + d * GIZMO_LEN
        try:
            x2s,y2s,_ = proj3d.proj_transform(center[0], center[1], center[2], ax.get_proj())
            x2e,y2e,_ = proj3d.proj_transform(end[0], end[1], end[2], ax.get_proj())
        except: continue
        sx,sy = ax.transAxes.transform((x2s,y2s))
        ex,ey = ax.transAxes.transform((x2e,y2e))
        ab = np.array([ex-sx, ey-sy])
        ap = np.array([event.x - sx, event.y - sy])
        len2 = np.dot(ab,ab)
        if len2 < 1e-6: continue
        t = np.clip(np.dot(ap,ab)/len2, 0, 1)
        closest = np.array([sx,sy]) + t*ab
        dist = np.hypot(event.x-closest[0], event.y-closest[1])
        tip_dist = np.hypot(event.x-ex, event.y-ey)
        dist = min(dist, tip_dist)
        if dist < best_dist:
            best_dist, best_axis, best_vec = dist, axis, ab
            best_len = np.linalg.norm(ab)
    if best_dist < 22:  # 太くしたので閾値も上げる
        return best_axis, best_vec, best_len
    return None

def select_cube(idx):
    state['selected'] = idx
    update_highlight(); update_gizmo(idx); update_status()
    fig.canvas.draw_idle()
    print(f"[select] cube {idx} origin={cubes[idx]['origin'].round(2)}")

def deselect():
    state['selected'] = None
    update_highlight(); update_gizmo(None); update_status()
    fig.canvas.draw_idle()
    print("[deselect]")

def on_press(event):
    # inaxesがNoneでもaxes bbox内なら通す（3Dでevent.inaxesが不安定なため）
    if event.x is None or event.y is None:
        return
    if event.inaxes is not None and event.inaxes != ax:
        return
    # 追加チェック: マウスがaxesのbbox外なら無視（カメラ操作に任せる）
    try:
        bbox = ax.get_window_extent()
        if not (bbox.x0 < event.x < bbox.x1 and bbox.y0 < event.y < bbox.y1):
            return
    except: pass

    gizmo_pick = pick_gizmo(event)
    if gizmo_pick is not None:
        axis, vec, lpx = gizmo_pick
        state['dragging'] = True
        state['drag_axis'] = axis
        state['start_xy'] = (event.x, event.y)
        state['start_origin'] = cubes[state['selected']]['origin'].copy()
        state['stored_view'] = (ax.elev, ax.azim)
        state['gizmo_vec'] = vec
        state['gizmo_len_px'] = lpx
        print(f"[gizmo] cube {state['selected']} axis={axis} lpx={lpx:.1f}")
        return

    idx = pick_cube(event)
    is_shift = (event.key == 'shift')
    mode = 'z' if (event.button == 3 or is_shift) else 'xy'

    if idx is not None:
        # 既に選択中と同じならドラッグ開始のみ、違うなら選択切り替え＋ドラッグ
        if state['selected'] != idx:
            state['selected'] = idx
            update_highlight(); update_gizmo(idx); update_status()
        state['dragging'] = True
        state['drag_axis'] = None
        state['drag_mode'] = mode
        state['start_xy'] = (event.x, event.y)
        state['start_origin'] = cubes[idx]['origin'].copy()
        state['stored_view'] = (ax.elev, ax.azim)
        fig.canvas.draw_idle()
        print(f"[cube-drag] cube {idx} mode={mode}")
    else:
        # 空クリック: 左クリックなら選択解除、右/中はカメラ操作に委譲
        if event.button == 1 and state['selected'] is not None:
            # クリック位置がどのcubeのbboxにも入ってなければ解除
            # ただしドラッグ開始はしない
            deselect()

def on_motion(event):
    if not state['dragging'] or state['selected'] is None: return
    if event.x is None or event.y is None: return
    # カメラ回転固定
    if state['stored_view'] is not None:
        try: ax.view_init(elev=state['stored_view'][0], azim=state['stored_view'][1])
        except: pass

    idx = state['selected']
    dx = event.x - state['start_xy'][0]
    dy = event.y - state['start_xy'][1]

    if state['drag_axis'] is not None:
        vec = state['gizmo_vec']; lpx = state['gizmo_len_px']
        if lpx is None or lpx < 5:
            bbox = ax.get_window_extent()
            scale = (ax_limit[1]-ax_limit[0]) / max(bbox.width,1) * 2.0
            axis_idx = {'x':0,'y':1,'z':2}[state['drag_axis']]
            delta = (dx - dy) * scale * 0.5
            new_origin = state['start_origin'].copy()
            new_origin[axis_idx] += delta
        else:
            unit = vec / lpx
            proj = dx*unit[0] + dy*unit[1]
            world = proj * (GIZMO_LEN / lpx)
            new_origin = state['start_origin'].copy()
            axis_idx = {'x':0,'y':1,'z':2}[state['drag_axis']]
            new_origin[axis_idx] += world
        for k in range(3):
            lo, hi = ax_limit[0], ax_limit[1]-size
            new_origin[k] = np.clip(new_origin[k], lo, hi)
        cubes[idx]['origin'] = new_origin
        cubes[idx]['poly'].set_verts(make_cube_faces(new_origin, size))
        update_gizmo(idx); update_status()
        fig.canvas.draw_idle()
        return

    # フリー移動
    try: bbox = ax.get_window_extent(); w, h = max(bbox.width,1), max(bbox.height,1)
    except: w,h = 800,600
    sx = (ax_limit[1]-ax_limit[0]) / w * 2.0
    sy = (ax_limit[1]-ax_limit[0]) / h * 2.0
    sz = (ax_limit[1]-ax_limit[0]) / h * 2.0
    new_origin = state['start_origin'].copy()
    if state['drag_mode'] == 'xy':
        new_origin[0] += dx * sx
        new_origin[1] += -dy * sy
    else:
        new_origin[2] += -dy * sz
    for k in range(3):
        lo, hi = ax_limit[0], ax_limit[1]-size
        new_origin[k] = np.clip(new_origin[k], lo, hi)
    cubes[idx]['origin'] = new_origin
    cubes[idx]['poly'].set_verts(make_cube_faces(new_origin, size))
    update_gizmo(idx); update_status()
    fig.canvas.draw_idle()

def on_release(event):
    if state['dragging'] and state['selected'] is not None:
        print(f"[move] cube {state['selected']} -> {cubes[state['selected']]['origin'].round(2)}")
    state['dragging'] = False
    state['drag_axis'] = None
    state['start_xy'] = None
    state['start_origin'] = None
    state['stored_view'] = None

def on_key(event):
    # 1,2,3で確実に選択（クリックが難しい時のフォールバック）
    if event.key in ['1','2','3']:
        idx = int(event.key)-1
        if 0 <= idx < len(cubes):
            select_cube(idx)
        return
    if state['selected'] is None: return
    idx = state['selected']
    step = 0.25
    if event.key == 'escape':
        deselect(); return
    d = np.zeros(3)
    if event.key in ['left','a']: d[0]-=step
    elif event.key in ['right','d']: d[0]+=step
    elif event.key in ['up','w']: d[1]+=step
    elif event.key in ['down','s']: d[1]-=step
    elif event.key in ['q','pageup']: d[2]+=step
    elif event.key in ['e','pagedown']: d[2]-=step
    else: return
    new_origin = cubes[idx]['origin']+d
    for k in range(3):
        lo,hi = ax_limit[0], ax_limit[1]-size
        new_origin[k]=np.clip(new_origin[k], lo, hi)
    cubes[idx]['origin']=new_origin
    cubes[idx]['poly'].set_verts(make_cube_faces(new_origin,size))
    update_gizmo(idx); update_status(); fig.canvas.draw_idle()
    print(f"[key] cube {idx} -> {new_origin.round(2)}")

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('key_press_event', on_key)

# 初期描画（projを確定させるため）
fig.canvas.draw()
update_highlight(); update_gizmo(None); update_status()
print("--- Gizmo改良版 ---")
print("  [クリック] 立方体バウンディングボックス判定で選択 (閾値80px)")
print("  [1/2/3キー] 確実に選択（クリックが外れる時の代替）")
print("  [ギズモ] 太さ5, 判定22pxに拡大")
print("  [空ドラッグ] カメラ回転は維持")

plt.tight_layout()
plt.show()

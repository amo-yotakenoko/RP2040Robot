import trimesh
import pyvista as pv
import numpy as np

# 1. trimeshでGLTFを読み込み、階層構造（ワールド変換）を正しく反映する
gltf_path = r"C:\Users\taken\Downloads\main.gltf"
print(f"Loading {gltf_path}...")
scene = trimesh.load(gltf_path)

pl = pv.Plotter()
actors = []
current_widget = [None]

# 2. シーン内の各パーツをPyVista用に変換してプロッターに追加
for node_name in scene.graph.nodes_geometry:
    matrix, geometry_name = scene.graph[node_name]
    mesh_trimesh = scene.geometry[geometry_name].copy()
    
    # ワールド座標系への変換を適用
    mesh_trimesh.apply_transform(matrix)
    
    v = mesh_trimesh.vertices
    f = mesh_trimesh.faces
    faces_pv = np.hstack([np.full((f.shape[0], 1), 3, dtype=f.dtype), f]).flatten()
    
    poly = pv.PolyData(v, faces_pv)
    poly.compute_normals()
    
    # pickable=Trueにしてマウス選択できるようにする
    actor = pl.add_mesh(poly, color='lightblue', show_edges=True, pickable=True)
    actor.name = node_name
    actors.append(actor)

print(f"{len(actors)}個のパーツを読み込みました。")

# 3. パーツがクリックされたときのコールバック処理
def select_callback(actor):
    if actor is None:
        return
    print(f"選択中パーツ: {getattr(actor, 'name', 'Unknown')}")
    
    # 選択色の切り替え（選ばれたら赤、他は水色）
    for a in actors:
        a.prop.color = 'lightblue'
    actor.prop.color = 'red'
    
    # 既存の移動・回転ギズモを削除
    if current_widget[0] is not None:
        current_widget[0].remove()
        
    # 選択したアクターにアフィン変換ウィジェット（ギズモ）を追加
    current_widget[0] = pl.add_affine_transform_widget(actor)

# 4. マウス左クリックでアクターを選択できるように有効化
pl.enable_mesh_picking(
    callback=select_callback,
    use_actor=True,
    left_clicking=True,
    show=False
)

print("\n--- 操作方法 ---")
print("  [左クリック]: パーツを選択（赤色になり、移動・回転ギズモが表示されます）")
print("  [ギズモ操作]: 矢印やリングをドラッグして位置・姿勢を自由に変更")

pl.add_axes()
pl.show()
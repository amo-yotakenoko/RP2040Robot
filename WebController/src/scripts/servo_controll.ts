import { Mesh } from "@babylonjs/core/Meshes/mesh";
import { Vector3 } from "@babylonjs/core/Maths/math.vector";
import { TransformNode } from "@babylonjs/core/Meshes/transformNode";

export default class MyScriptComponent {
    private targets: TransformNode[] = [];

    public constructor(public mesh: Mesh) { }

    public onStart(): void {
        const scene = this.mesh.getScene();
        const names = ["hone000", "hone001", "hone002", "hone003", "hone004", "hone005"];

        for (const name of names) {
            const node = scene.getTransformNodeByName(name) || scene.getNodeByName(name);
            if (!node) {
                console.log("Not found: " + name);
                continue;
            }

            console.log("Found: " + name + " (" + node.getClassName() + ")");

            // rotationQuaternion が優先されていると回転が効かないので null にする
            if ((node as any).rotationQuaternion) {
                (node as any).rotationQuaternion = null;
            }

            // オイラー角を初期化しておく（未定義だと不具合になる場合あり）
            if (!(node as any).rotation) {
                (node as any).rotation = Vector3.Zero();
            }

            this.targets.push(node as TransformNode);
        }
    }

    public onUpdate(): void {
        const ratio = this.mesh.getScene().getAnimationRatio();
        for (const m of this.targets) {
            // ローカルX軸方向に回転（ラジアン）
            m.rotation.x += 0.04 * ratio;
        }
    }
}

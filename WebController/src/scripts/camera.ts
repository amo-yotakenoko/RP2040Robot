import { Mesh } from "@babylonjs/core/Meshes/mesh";
import { Vector3 } from "@babylonjs/core/Maths/math.vector";
import { Color3 } from "@babylonjs/core/Maths/math.color";
import { StandardMaterial } from "@babylonjs/core/Materials/standardMaterial";
import { VideoTexture } from "@babylonjs/core/Materials/Textures/videoTexture";

import { IScript, visibleAsNumber } from "babylonjs-editor-tools";

export default class SceneComponent implements IScript {
    // 回転速度
    @visibleAsNumber("Speed", {
        min: 0,
        max: 0.1,
    })
    private _speed: number = 0.04;

    // アスペクト比（幅/高さ）
    @visibleAsNumber("AspectRatio", {
        min: 0.1,
        max: 10,
    })
    private _aspectRatio: number = 16 / 9;

    // Webカメラのビデオテクスチャ
    private _videoTexture?: VideoTexture;

    public constructor(public mesh: Mesh) { }

    public onStart(): void {
        const scene = this.mesh.getScene();
        // メッシュの縦横比を調整
        this.mesh.scaling = new Vector3(this._aspectRatio, 1, 1);

        // Webカメラへのアクセス
        navigator.mediaDevices
            .getUserMedia({ video: true, audio: false })
            .then((stream) => {
                // ビデオ要素を作成
                const video = document.createElement("video");
                video.srcObject = stream;
                video.autoplay = true;
                video.muted = true;
                video.playsInline = true;
                video.setAttribute("playsinline", "");
                video.setAttribute("webkit-playsinline", "");

                // ビデオテクスチャを作成（自動再生設定）
                this._videoTexture = new VideoTexture("webcamVideo", video, scene, true, false, undefined, {
                    autoPlay: true,
                    muted: true,
                    loop: true,
                    autoUpdateTexture: true,
                });

                // 再生を試行
                const playVideo = () => {
                    video.play().catch(() => { });
                };
                playVideo();
                video.addEventListener("loadedmetadata", playVideo, { once: true });
                document.addEventListener("click", playVideo, { once: true });
                document.addEventListener("touchstart", playVideo, { once: true });

                // マテリアルを作成してビデオを適用
                const material = new StandardMaterial("webcamMaterial", scene);
                material.diffuseTexture = this._videoTexture;
                material.emissiveColor = new Color3(1, 1, 1);
                material.specularColor = new Color3(0, 0, 0);
                this.mesh.material = material;
            })
            .catch((err) => {
                console.error("Webカメラへのアクセスに失敗しました:", err);
            });
    }

    public onUpdate(): void {
        // メッシュを回転
        // this.mesh.rotate(Vector3.UpReadOnly, this._speed * this.mesh.getScene().getAnimationRatio());
    }
}

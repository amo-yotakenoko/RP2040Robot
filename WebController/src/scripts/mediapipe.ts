import { Mesh } from "@babylonjs/core/Meshes/mesh";
import { Vector3 } from "@babylonjs/core/Maths/math.vector";
import { Color3 } from "@babylonjs/core/Maths/math.color";
import { StandardMaterial } from "@babylonjs/core/Materials/standardMaterial";
import { VideoTexture } from "@babylonjs/core/Materials/Textures/videoTexture";
import { DynamicTexture } from "@babylonjs/core/Materials/Textures/dynamicTexture";

import { IScript, visibleAsNumber } from "babylonjs-editor-tools";

import {
    FaceLandmarker,
    FilesetResolver,
    DrawingUtils,
    type FaceLandmarkerResult,
} from "@mediapipe/tasks-vision";

export default class MediapipeScript implements IScript {
    @visibleAsNumber("AspectRatio", {
        min: 0.1,
        max: 10,
    })
    private _aspectRatio: number = 16 / 9;

    private _videoTexture?: VideoTexture;
    private _videoElement?: HTMLVideoElement;
    private _faceLandmarker?: FaceLandmarker;
    private _running: boolean = false;
    private _lastTimestampMs: number = 0;
    private _canvas?: HTMLCanvasElement;
    private _canvasCtx?: CanvasRenderingContext2D;
    private _drawingUtils?: DrawingUtils;
    private _overlayCanvas?: HTMLCanvasElement;
    private _overlayCtx?: CanvasRenderingContext2D;
    private _logEl?: HTMLElement;

    public constructor(public mesh: Mesh) {}

    public async onStart(): Promise<void> {
        const scene = this.mesh.getScene();
        this.mesh.scaling = new Vector3(this._aspectRatio, 1, 1);

        try {
            const vision = await FilesetResolver.forVisionTasks(
                "/mediapipe/vision_wasm_internal"
            );

            this._faceLandmarker = await FaceLandmarker.createFromOptions(vision, {
                baseOptions: {
                    modelAssetPath: "/face_landmarker.task",
                    delegate: "GPU",
                },
                runningMode: "VIDEO",
                numFaces: 1,
                outputFaceBlendshapes: true,
                outputFacialTransformationMatrixes: true,
            });
        } catch (err) {
            console.error("[mediapipe] Failed to initialize FaceLandmarker:", err);
            return;
        }

        navigator.mediaDevices
            .getUserMedia({ video: true, audio: false })
            .then((stream) => {
                const video = document.createElement("video");
                video.srcObject = stream;
                video.autoplay = true;
                video.muted = true;
                video.playsInline = true;
                video.setAttribute("playsinline", "");
                video.setAttribute("webkit-playsinline", "");

                this._videoElement = video;

                this._videoTexture = new VideoTexture("webcamVideoMp", video, scene, true, false, undefined, {
                    autoPlay: true,
                    muted: true,
                    loop: true,
                    autoUpdateTexture: true,
                });

                const material = new StandardMaterial("webcamMaterialMp", scene);
                material.diffuseTexture = this._videoTexture;
                material.emissiveColor = new Color3(1, 1, 1);
                material.specularColor = new Color3(0, 0, 0);
                this.mesh.material = material;

                const playVideo = () => {
                    video.play().catch(() => {});
                };
                playVideo();
                video.addEventListener("loadedmetadata", playVideo, { once: true });
                document.addEventListener("click", playVideo, { once: true });
                document.addEventListener("touchstart", playVideo, { once: true });

                this._canvas = document.createElement("canvas");
                this._canvas.width = 1280;
                this._canvas.height = 720;
                this._canvasCtx = this._canvas.getContext("2d") || undefined;
                if (this._canvasCtx) {
                    this._drawingUtils = new DrawingUtils(this._canvasCtx);
                }

                const oc = document.getElementById("mp-canvas");
                this._overlayCanvas = oc instanceof HTMLCanvasElement ? oc : undefined;
                if (this._overlayCanvas) {
                    this._overlayCtx = this._overlayCanvas.getContext("2d") || undefined;
                }
                const le = document.getElementById("mp-log");
                this._logEl = le instanceof HTMLElement ? le : undefined;

                this._running = true;
            })
            .catch((err) => {
                console.error("[mediapipe] Failed to access webcam:", err);
            });
    }

    public onUpdate(): void {
        if (!this._running || !this._faceLandmarker || !this._videoElement) {
            return;
        }

        if (this._videoElement.readyState < 2) {
            return;
        }

        this._lastTimestampMs += 1;
        let result: FaceLandmarkerResult;
        try {
            result = this._faceLandmarker.detectForVideo(this._videoElement, this._lastTimestampMs);
        } catch (e) {
            console.error("[mediapipe] detectForVideo error:", e);
            return;
        }

        // オーバーレイにカメラ映像を描画
        if (this._overlayCanvas && this._overlayCtx && this._videoElement) {
            try {
                this._overlayCtx.drawImage(this._videoElement, 0, 0, this._overlayCanvas.width, this._overlayCanvas.height);
            } catch (_) {}
        }

        if (result.faceLandmarks && result.faceLandmarks.length > 0) {
            const landmarks = result.faceLandmarks[0];

            // ランドマークをオーバーレイに描画
            if (this._overlayCtx && this._overlayCanvas) {
                this._overlayCtx.fillStyle = "#00ff00";
                for (let i = 0; i < landmarks.length; i++) {
                    const p = landmarks[i];
                    const x = p.x * this._overlayCanvas.width;
                    const y = p.y * this._overlayCanvas.height;
                    this._overlayCtx.beginPath();
                    this._overlayCtx.arc(x, y, 1, 0, 2 * Math.PI);
                    this._overlayCtx.fill();
                }
            }

            let cx = 0,
                cy = 0,
                cz = 0;
            for (let i = 0; i < landmarks.length; i++) {
                cx += landmarks[i].x;
                cy += landmarks[i].y;
                cz += landmarks[i].z;
            }
            cx /= landmarks.length;
            cy /= landmarks.length;
            cz /= landmarks.length;

            let position: [number, number, number] | null = null;
            let rotationMatrix: number[][] | null = null;
            if (result.facialTransformationMatrixes && result.facialTransformationMatrixes.length > 0) {
                const m = result.facialTransformationMatrixes[0] as any;
                rotationMatrix = [
                    [m[0], m[1], m[2]],
                    [m[3], m[4], m[5]],
                    [m[6], m[7], m[8]],
                ];
                position = [m[12], m[13], m[14]];
            }

            const blendshapes: Array<{ name: string; value: number }> = [];
            if (result.faceBlendshapes && result.faceBlendshapes.length > 0) {
                const list = result.faceBlendshapes[0].categories;
                for (let i = 0; i < list.length; i++) {
                    blendshapes.push({ name: list[i].categoryName, value: list[i].score });
                }
            }

            const out = {
                position,
                rotationMatrix,
                blendshapes,
                center: { x: cx, y: cy, z: cz },
            };
            console.log(JSON.stringify(out));
            if (this._logEl) {
                this._logEl.textContent = JSON.stringify(out, null, 2).slice(0, 2000);
            }
        } else {
            if (this._logEl) {
                this._logEl.textContent = "(no face)";
            }
            // 顔が検出されない場合も定期的にログ出力して動作確認しやすくする
            // 必要に応じてコメントアウト可
        }
    }

    public onDestroy(): void {
        this._running = false;
        if (this._videoElement && this._videoElement.srcObject) {
            const stream = this._videoElement.srcObject as MediaStream;
            stream.getTracks().forEach((t) => t.stop());
        }
        if (this._videoTexture) {
            this._videoTexture.dispose();
        }
        if (this._faceLandmarker) {
            this._faceLandmarker.close();
        }
    }
}

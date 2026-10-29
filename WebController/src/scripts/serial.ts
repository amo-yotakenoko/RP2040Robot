import { Mesh } from "@babylonjs/core/Meshes/mesh";
import { Vector3 } from "@babylonjs/core/Maths/math.vector";
import { AdvancedDynamicTexture } from "@babylonjs/gui/2D/advancedDynamicTexture";
import { Button } from "@babylonjs/gui/2D/controls/button";
import { Control } from "@babylonjs/gui/2D/controls/control";

export default class SceneComponent {
    private port?: SerialPort;
    private reader?: ReadableStreamDefaultReader<Uint8Array>;
    private writer?: WritableStreamDefaultWriter<Uint8Array>;
    private encoder = new TextEncoder();
    private decoder = new TextDecoder();
    private baudRate = 115200;
    private gui?: AdvancedDynamicTexture;

    public constructor(public mesh: Mesh) { }

    public onStart(): void {
        // フルスクリーンUIを作成
        this.gui = AdvancedDynamicTexture.CreateFullscreenUI("SerialUI");

        // 接続ボタンを作成
        const button = Button.CreateSimpleButton("connectBtn", "シリアル接続");
        button.width = "200px";
        button.height = "40px";
        button.color = "white";
        button.background = "#2f7bff";
        button.cornerRadius = 4;
        button.horizontalAlignment = Control.HORIZONTAL_ALIGNMENT_CENTER;
        button.verticalAlignment = Control.VERTICAL_ALIGNMENT_BOTTOM;
        button.paddingBottom = "20px";

        // ボタンクリック時に接続（ユーザージェスチャ内から呼ぶ）
        button.onPointerClickObservable.add(() => {
            this.connect();
        });

        this.gui.addControl(button);
    }

    public async connect(): Promise<void> {
        console.log("接続ボタンがクリックされました");
        try {
            // フィルタなしでポートを選択
            this.port = await navigator.serial.requestPort();
            await this.port.open({ baudRate: this.baudRate });
            console.log("シリアルポートに接続しました");
            this.readLoop();
            this.send("1,10");
        } catch (e: any) {
            if (e.name === "NotFoundError") {
                // ユーザーがポート選択をキャンセルした場合
                return;
            }
            console.error("シリアルポートの接続に失敗しました:", e);
        }
    }

    private async readLoop(): Promise<void> {
        if (!this.port?.readable) return;
        this.reader = this.port.readable.getReader();

        try {
            while (true) {
                const { value, done } = await this.reader.read();
                if (done) break;
                if (value) {
                    console.log(this.decoder.decode(value));
                }
            }
        } catch (e) {
            console.error("読み取りエラー:", e);
        } finally {
            this.reader?.releaseLock();
        }
    }

    public async send(data: string | Uint8Array): Promise<void> {
        if (!this.port?.writable) return;
        if (!this.writer) {
            this.writer = this.port.writable.getWriter();
        }
        const bytes = typeof data === "string" ? this.encoder.encode(data) : data;
        await this.writer.write(bytes);
    }

    public async close(): Promise<void> {
        this.reader?.cancel();
        this.reader?.releaseLock();
        this.writer?.releaseLock();
        await this.port?.close();
        this.port = undefined;
    }

    public onUpdate(): void {
        this.mesh.rotation.y += 0.04 * this.mesh.getScene().getAnimationRatio();
    }

    public onDestroy(): void {
        this.gui?.dispose();
        this.close();
    }
}
using UnityEngine;
using UnityEngine.Rendering;

public class WebCam : MonoBehaviour
{
    private WebCamTexture webcam;

    void Start()
    {
        Renderer targetRenderer = GetComponent<MeshRenderer>();

        // 映像表示用のマテリアルを作成
        Material material = new Material(
            Shader.Find("Universal Render Pipeline/Unlit")
        );

        material.color = Color.white;

        webcam = new WebCamTexture();
        webcam.Play();

        material.mainTexture = webcam;
        targetRenderer.material = material;

        targetRenderer.shadowCastingMode = ShadowCastingMode.Off;
        targetRenderer.receiveShadows = false;
    }

    void OnDestroy()
    {
        if (webcam != null)
            webcam.Stop();
    }
}

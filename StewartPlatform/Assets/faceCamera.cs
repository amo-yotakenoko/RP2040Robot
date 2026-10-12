using UnityEngine;

public class FaceCamera : MonoBehaviour
{
    private Camera cam;
    private RenderTexture rt;
    private Texture2D tex;

    private const int width = 128;
    private const int height = 64;

    void Start()
    {
        cam = GetComponent<Camera>();

        rt = new RenderTexture(width, height, 24);
        tex = new Texture2D(width, height, TextureFormat.RGB24, false);

        cam.targetTexture = rt;
    }

    public byte[] GetfaceFrame()
    {
        cam.Render();

        RenderTexture.active = rt;
        tex.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        tex.Apply();
        RenderTexture.active = null;

        Color32[] pixels = tex.GetPixels32();
        byte[] data = new byte[width * height / 8];

        for (int y = 0; y < height; y++)
        {
            for (int x = width - 1; x >= 0; x--)
            {
                Color32 c = pixels[y * width + x];
                int gray = (c.r * 299 + c.g * 587 + c.b * 114) / 1000;

                if (!(gray <= 128))
                {
                    int index = (y / 8) * width + x;
                    data[index] |= (byte)(1 << (y % 8));
                }
            }
        }

        return data;
    }

    void OnDestroy()
    {
        if (cam != null)
            cam.targetTexture = null;

        if (rt != null)
        {
            rt.Release();
            Destroy(rt);
        }

        if (tex != null)
            Destroy(tex);
    }
}
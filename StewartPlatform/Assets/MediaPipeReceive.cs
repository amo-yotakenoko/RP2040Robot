using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class MediaPipeReceive : MonoBehaviour
{
    [Serializable]
    public class Vec3
    {
        public float x;
        public float y;
        public float z;
    }

    [Serializable]
    public class Quat
    {
        public float x;
        public float y;
        public float z;
        public float w;
    }

    [Serializable]
    public class FaceData
    {
        public Vec3 position;
        public Quat rotation;
    }

    private UdpClient client;
    private Thread receiveThread;
    private volatile bool running;

    private readonly object dataLock = new object();
    private FaceData latestData;

    [Header("Position")]
    public float positionScale = 1.0f;

    [Header("Coordinate Conversion")]
    public bool invertX;
    public bool invertY;
    public bool invertZ;

    [Header("Rotation Conversion")]
    public bool invertRotationX;
    public bool invertRotationY;
    public bool invertRotationZ;

    void Start()
    {
        try
        {
            client = new UdpClient(5000);
            running = true;

            receiveThread = new Thread(ReceiveLoop);
            receiveThread.IsBackground = true;
            receiveThread.Start();
        }
        catch (Exception e)
        {
            Debug.LogError($"UDP initialization failed: {e.Message}");
        }
    }

    void ReceiveLoop()
    {
        IPEndPoint remoteEndPoint =
            new IPEndPoint(IPAddress.Any, 0);

        while (running)
        {
            try
            {
                byte[] bytes = client.Receive(ref remoteEndPoint);
                string json = Encoding.UTF8.GetString(bytes);
                print($"Received JSON: {json}"); // デバッグ用に受信したJSONを表示

                FaceData data = JsonUtility.FromJson<FaceData>(json);
                // print(data);

                if (data != null && data.position != null && data.rotation != null)
                {
                    lock (dataLock)
                    {
                        latestData = data;
                        print($"Received Data: pos=({data.position.x}, {data.position.y}, {data.position.z}), rot=({data.rotation.x}, {data.rotation.y}, {data.rotation.z}, {data.rotation.w})");
                    }
                }
            }
            catch (ObjectDisposedException)
            {
                break;
            }
            catch (SocketException)
            {
                if (!running) break;
            }
            catch (Exception e)
            {
                Debug.LogWarning($"UDP receive error: {e.Message}");
            }
        }
    }

    void Update()
    {
        FaceData data;

        lock (dataLock)
        {
            data = latestData;
        }

        if (data == null || data.position == null || data.rotation == null)
            return;

        // Pythonから受信した位置
        Vector3 receivedPosition = new Vector3(
            invertX ? -data.position.x : data.position.x,
            invertY ? -data.position.y : data.position.y,
            invertZ ? -data.position.z : data.position.z
        );

        // オブジェクトの位置に反映
        this.transform.localPosition = receivedPosition * positionScale;


        // Pythonから受信したクォータニオンに軸反転を適用
        Quaternion receivedRotation = new Quaternion(
            invertRotationX ? -data.rotation.x : data.rotation.x,
            invertRotationY ? -data.rotation.y : data.rotation.y,
            invertRotationZ ? -data.rotation.z : data.rotation.z,
            data.rotation.w
        );

        // オブジェクトの回転に反映
        this.transform.localRotation = receivedRotation;
    }

    void OnApplicationQuit()
    {
        running = false;

        client?.Close();

        if (receiveThread != null && receiveThread.IsAlive)
        {
            receiveThread.Join(200);
        }
    }
}

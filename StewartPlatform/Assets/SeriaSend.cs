using UnityEngine;
using System.IO.Ports;
using System;
using System.Collections;
using System.Collections.Generic;

public class SeriaSend : MonoBehaviour
{
    // 設定
    private string portName = "COM10";
    private int baudRate = 115200;
    private SerialPort serialPort;

    // サーボオブジェクトのリスト



    void Start()
    {
        // servos = GetComponent<servocopy>().servos;
        OpenConnection();

        // コルーチンを開始
        StartCoroutine(SerialCoroutine());
    }

    void OpenConnection()
    {
        serialPort = new SerialPort(portName, baudRate);
        serialPort.ReadTimeout = 50;
        serialPort.WriteTimeout = 50;

        try
        {
            serialPort.Open();
            Debug.Log($"シリアルポート {portName} をオープンしました（BaudRate: {baudRate}）。");
        }
        catch (Exception e)
        {
            Debug.LogError($"シリアルポートのオープンに失敗しました: {e.Message}");
        }
    }

    IEnumerator SerialCoroutine()
    {
        string lastFaceMessage = "";
        while (true)
        {



            servo servo = FindFirstObjectByType<servo>();
            for (int s = 0; s < servo.angles.Length; s++)
            {

                // 送信文字列の作成
                string message = $"{s},{(int)(servo.angles[s])}";

                // シリアルポート経由で送信
                SendData(message);
                yield return null;
            }




            // yield return null;
            // byte[] faceFrame = FindFirstObjectByType<FaceCamera>().GetfaceFrame();
            // // yield return new WaitForSeconds(0.1f);

            // string faceMessage = $"{BitConverter.ToString(faceFrame).Replace("-", "")}";
            // if (faceMessage != lastFaceMessage)
            // {
            //     lastFaceMessage = faceMessage;
            //     print($"送信: FACE,{faceMessage}");
            //     SendData($"FACE,{faceMessage}");
            //     yield return new WaitForSeconds(0.1f);

            // }
            yield return null;
        }
    }

    void SendData(string message)
    {
        if (serialPort != null && serialPort.IsOpen)
        {
            try
            {
                // 改行付きで送信（マイコン側がreadLine等で受信する場合に対応）
                serialPort.WriteLine(message);
                Debug.Log($"送信: {message}"); // デバッグしたい場合はコメントアウトを解除
            }
            catch (Exception e)
            {
                Debug.LogError($"送信エラー: {e.Message}");
            }
        }
    }

    void OnDestroy() => CloseConnection();
    void OnApplicationQuit() => CloseConnection();

    void CloseConnection()
    {
        if (serialPort != null && serialPort.IsOpen)
        {
            serialPort.Close();
            Debug.Log("シリアルポートを閉じました。");
        }
    }
}

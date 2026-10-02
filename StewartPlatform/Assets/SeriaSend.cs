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
    public List<GameObject> servos;


    void Start()
    {
        servos = GetComponent<servocopy>().servos;
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
        while (true)
        {
            for (int i = 0; i < servos.Count; i++)
            {
                if (servos[i] != null)
                {
                    servo servoScript = servos[i].GetComponent<servo>();
                    if (servoScript != null)
                    {
                        // 送信文字列の作成
                        string message = $"{servoScript.id},{servoScript.angle}";

                        // シリアルポート経由で送信
                        SendData(message);
                    }
                }

                // 0.1秒待機（次のサーボへ）
                yield return new WaitForSeconds(0.01f);
            }
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
                // Debug.Log($"送信: {message}"); // デバッグしたい場合はコメントアウトを解除
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

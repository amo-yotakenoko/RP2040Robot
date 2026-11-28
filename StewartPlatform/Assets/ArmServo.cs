using UnityEngine;
using System.Collections.Generic;

public class ArmServo : MonoBehaviour
{
    public List<Transform> axis = new List<Transform>();
    public List<float> angles = new List<float>();
    public Transform ArmTarget;
    Transform Hand;

    void Start()
    {
        List<Transform> servos = new List<Transform>();
        for (int i = 1; i <= 6; i++)
        {
            Transform servo = transform.Find($"ArmServo{i:D3}").transform;
            servos.Add(servo);
            GameObject axisObj = new GameObject($"axis{i:D3}");
            axisObj.transform.SetParent(servo);
            axisObj.transform.localPosition = Vector3.zero;
            axisObj.transform.localRotation = Quaternion.identity;
            axis.Add(axisObj.transform);
            angles.Add(90f); // 初期値を90度に設定
        }

        Transform BaseYaw = transform.Find("BaseYaw");
        Transform UpperArm = transform.Find("UpperArm");
        Transform Forearm = transform.Find("Forearm");
        Transform WristRoll = transform.Find("WristRoll");
        Transform WristPitch = transform.Find("WristPitch");
        Hand = transform.Find("Hand");

        BaseYaw.SetParent(axis[0]);

        axis[1].SetParent(BaseYaw);

        UpperArm.SetParent(axis[1]);
        servos[1].SetParent(axis[1]);
        servos[2].SetParent(axis[1]);

        Forearm.SetParent(axis[2]);
        servos[3].SetParent(axis[2]);

        WristRoll.SetParent(axis[3]);
        servos[4].SetParent(axis[3]);

        WristPitch.SetParent(axis[4]);
        servos[5].SetParent(axis[4]);

        Hand.SetParent(axis[5]);

        fk(angles);
    }

    float CalcDistance()
    {
        if (Hand == null || ArmTarget == null) return float.MaxValue;

        float distance = Vector3.Distance(Hand.position, ArmTarget.position);
        float angleDiff = Quaternion.Angle(Hand.rotation, ArmTarget.rotation);

        return distance + angleDiff * 0.001f;
    }

    float fk(List<float> inputAngles)
    {
        for (int i = 0; i < axis.Count; i++)
        {
            // 90度を基準（オフセット0）として回転姿勢に変換
            float offsetAngle = inputAngles[i] - 90f;

            if (i == 1)
            {
                axis[i].localEulerAngles = new Vector3(90f - offsetAngle, 0f, -90f);
            }
            else
            {
                axis[i].localEulerAngles = new Vector3(0f, offsetAngle, 0f);
            }
        }
        return CalcDistance();
    }

    bool updateAngles()
    {
        if (ArmTarget == null || Hand == null) return true;

        float currentDist = fk(angles);
        if (currentDist < 0.001f) return true;

        // 手首側から根元に向かって各軸を更新
        for (int i = angles.Count - 1; i >= 0; i--)
        {
            float original = angles[i];

            // 微小変化 ±0.05度
            angles[i] = original + 0.05f;
            float distPlus = fk(angles);

            angles[i] = original - 0.05f;
            float distMinus = fk(angles);

            angles[i] = original;

            // 勾配（傾き）
            float grad = (distPlus - distMinus) / 0.1f;

            float step = Mathf.Clamp(-grad * 100.0f, -10.0f, 10.0f);
            angles[i] += step;

            // 0度 〜 180度にクランプ
            angles[i] = Mathf.Clamp(angles[i], 0f, 180f);

            fk(angles);
        }

        return false;
    }

    void Update()
    {
        for (int i = 0; i < 100; i++)
        {
            if (updateAngles()) break;
        }
        // fk(angles);
    }


}

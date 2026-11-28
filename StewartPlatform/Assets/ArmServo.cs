using UnityEngine;
using System.Collections.Generic;

public class ArmServo : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public List<Transform> axis;
    public List<float> angles;
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
            angles.Add(0f);
        }
        Transform BaseYaw = transform.Find("BaseYaw");
        Transform UpperArm = transform.Find("UpperArm");
        Transform Forearm = transform.Find("Forearm");
        Transform WristRoll = transform.Find("WristRoll");
        Transform WristPitch = transform.Find("WristPitch");
        Hand = transform.Find("Hand");


        // transform.Find($"servo000").transform;
        BaseYaw.SetParent(axis[0]);

        axis[1].SetParent(BaseYaw);
        // axis[1].localRotation = Quaternion.Euler(0f, 0f, 90f);

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





    }

    float CalcDistance()
    {
        // handとArmTargetの距離と角度の差を計算する

        // 位置の距離（m）
        float distance = Vector3.Distance(Hand.position, ArmTarget.position);

        // 回転の角度差（0° 〜 180°）
        float angleDiff = Quaternion.Angle(Hand.rotation, ArmTarget.rotation);

        // 単純に足す場合
        // return distance + angleDiff;

        // 位置と角度のスケールを合わせるための重み付け（例: 角度の重みを 0.01f にする）
        float angleWeight = 0.01f;
        return distance + (angleDiff * angleWeight);
    }


    float fk(List<float> angles)
    {
        for (int i = 0; i < angles.Count; i++)
        {
            if (i == 1)
            {
                axis[i].localEulerAngles = new Vector3(90 + angles[i], 0f, -90f);
            }
            else
                axis[i].localEulerAngles = new Vector3(0f, angles[i], 0f);
        }
        return CalcDistance();
    }


    void updateAngles()
    {

        float initDistance = CalcDistance();


        for (int i = 0; i < angles.Count; i++)
        {
            List<float> copy = new List<float>(angles);
            copy[i] += 0.1f;
            fk(copy);
            float distance = fk(copy);
            print(distance);

            float grad = (distance - initDistance) * 1000; // 0.1度の変化に対する距離の変化

            angles[i] -= Mathf.Clamp(grad, -1f, 1f); // 角度を減少させる

            // angles[i] = grad; // 学習率を0.1に設定
            print(grad);

        }
    }

    // Update is called once per frame
    void Update()
    {
        fk(angles);
        updateAngles();


    }
}



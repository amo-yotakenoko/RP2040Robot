using UnityEngine;
using System.Collections.Generic;
using System.Linq;
// using System.Numerics;



public class HeadServo : MonoBehaviour
{
    public List<Transform> hones = new List<Transform>();
    public List<Transform> uppreholes = new List<Transform>();

    float target_lod_length = 0.1f;

    public float[] angles;

    void Start()
    {
        Transform HeadBase = GameObject.Find($"HeadBase").transform;
        for (int i = 1; i <= 6; i++)
        {
            // Transform servoTransform = GameObject.Find($"servo00{i}").transform;
            print($"servo{i:D3}");
            Transform honeTransform = transform.Find($"servo{i:D3}/hone{i:D3}").transform;
            // honeTransform.SetParent(servoTransform);
            hones.Add(honeTransform);

            Transform uppreholeTransform = transform.Find($"Head/upperhole00{i}").transform;
            // uppreholeTransform.SetParent(HeadBase);
            uppreholes.Add(uppreholeTransform);
        }

        Transform vrHead = GameObject.Find("Main Camera").transform;
        Transform headBase = GameObject.Find("HeadBase").transform;


        // vrHeadの設定
        // Vector3 originalScale = headBase.lossyScale;
        // headBase.SetParent(vrHead, false);
        // Vector3 parentScale = vrHead.lossyScale;
        // headBase.localScale = new Vector3(
        //     originalScale.x / parentScale.x,
        //     originalScale.y / parentScale.y,
        //     originalScale.z / parentScale.z
        // );


    }

    float CalcDistance(float angle, Transform hone, Transform upperhole)
    {
        float prevY = hone.localEulerAngles.y;

        hone.localEulerAngles = new Vector3(0f, angle, 0f);

        Vector3 honeTip = hone.position + hone.forward * 0.0135f;
        float distance = Vector3.Distance(honeTip, upperhole.position);

        hone.localEulerAngles = new Vector3(0f, prevY, 0f);

        return distance;
    }

    void Update()
    {
        angles = new float[6];
        int index = 0;
        foreach (var pair in hones.Zip(uppreholes, (h, u) => (h, u)))
        {

            Transform hone = pair.h;
            Transform upperhole = pair.u;

            float offset = (index % 2 == 0) ? 180f : 0f;

            float bestAngle = 0f;
            float bestDiff = float.MaxValue;
            bool solved = false;

            // 0〜180度を全探索して最初に十分近い角度を探す(単純増加と限らない為全探索)
            for (float angle = 0f; angle <= 180f; angle += 0.5f)
            {
                float testAngle = angle + offset;
                float dist = CalcDistance(testAngle, hone, upperhole);
                float diff = Mathf.Abs(dist - target_lod_length);

                if (diff < bestDiff)
                {
                    bestDiff = diff;
                    bestAngle = angle;
                }


            }
            if (bestDiff < 0.0001f)
            {
                solved = true;
            }

            hone.localEulerAngles = new Vector3(0f, bestAngle + offset, 0f);

            Vector3 honeTipFinal = hone.position + hone.forward * 0.0135f;
            Debug.DrawLine(honeTipFinal, hone.position, Color.yellow);
            Debug.DrawLine(honeTipFinal, upperhole.position, solved || bestDiff < 0.1f ? Color.green : Color.red);
            angles[index] = 180 - bestAngle;
            index++;
        }
    }
}
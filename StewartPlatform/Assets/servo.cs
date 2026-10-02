using UnityEngine;

public class servo : MonoBehaviour
{
    public Transform servoHone;
    public Transform HornLodPoint;
    public Transform HeadLodPoint;

    public bool isOpposite;
    public int id;
    public float angle;

    float target_lod_length = 50;

    float baseY, baseZ;       // 最初のy, z（固定）
    float initialAngle;       // 最初の角度（解の選択基準）

    void Start()
    {
        baseY = servoHone.localEulerAngles.y;
        baseZ = servoHone.localEulerAngles.z;

        float minAngle = isOpposite ? -180f : 0f;
        float maxAngle = isOpposite ? 0f : 180f;

        // 最初のX角度を記憶（0〜360 → -180〜180 に直して範囲内にクランプ）
        float a = servoHone.localEulerAngles.x;
        if (a > 180f) a -= 360f;
        initialAngle = Mathf.Clamp(a, minAngle, maxAngle);
    }

    float Err(float a)
    {
        servoHone.localEulerAngles = new Vector3(a, baseY, baseZ);
        return Vector3.Distance(HornLodPoint.position, HeadLodPoint.position) - target_lod_length;
    }

    float SolveAngle(float minA, float maxA)
    {
        const float step = 2f;
        float best = float.NaN;
        float bestDist = float.MaxValue;
        float minAbsErr = float.MaxValue;
        float minAbsAngle = initialAngle;

        float prevA = minA;
        float prevE = Err(prevA);
        minAbsErr = Mathf.Abs(prevE);
        minAbsAngle = prevA;

        for (float a = minA + step; a <= maxA + 0.001f; a += step)
        {
            float e = Err(a);

            // 解が無い場合の保険（誤差が最小の角度）
            if (Mathf.Abs(e) < minAbsErr) { minAbsErr = Mathf.Abs(e); minAbsAngle = a; }

            // 符号が変わった区間に解がある → 二分法で詰める
            if (prevE * e <= 0f)
            {
                float lo = prevA, hi = a, eLo = prevE;
                for (int k = 0; k < 20; k++)
                {
                    float mid = (lo + hi) * 0.5f;
                    float eMid = Err(mid);
                    if (eLo * eMid <= 0f) hi = mid;
                    else { lo = mid; eLo = eMid; }
                }
                float root = (lo + hi) * 0.5f;

                // 最初の角度に最も近い解を採用
                float d = Mathf.Abs(root - initialAngle);
                if (d < bestDist) { bestDist = d; best = root; }
            }
            prevA = a; prevE = e;
        }

        return float.IsNaN(best) ? minAbsAngle : best;
    }

    void Update()
    {
        float minAngle = isOpposite ? -180f : 0f;
        float maxAngle = isOpposite ? 0f : 180f;

        float currentAngle = SolveAngle(minAngle, maxAngle);
        servoHone.localEulerAngles = new Vector3(currentAngle, baseY, baseZ);

        angle = isOpposite ? 180 + currentAngle : currentAngle;
        this.gameObject.name = $"{angle}";

        Debug.DrawLine(HornLodPoint.position, HeadLodPoint.position, Color.green);
    }
}
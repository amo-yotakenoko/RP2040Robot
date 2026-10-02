using UnityEngine;

public class servo : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public Transform servoHone;
    public Transform HornLodPoint;
    public Transform HeadLodPoint;

    public bool isOpposite;
    public int id;
    public float angle;
    void Start()
    {
        HeadLodPoint.SetParent(GameObject.Find("Head").transform);
    }
    float target_lod_length = 50;
    // Update is called once per frame
    void Update()
    {
        servoHone.localEulerAngles = new Vector3(isOpposite ? -90f : 90f, servoHone.localEulerAngles.y, servoHone.localEulerAngles.z);
        for (int i = 0; i < 90; i++)
        {
            float diff_plus = Mathf.Abs(target_lod_length - Vector3.Distance(HornLodPoint.position + HornLodPoint.up, HeadLodPoint.position));
            float diff_minus = Mathf.Abs(target_lod_length - Vector3.Distance(HornLodPoint.position - HornLodPoint.up, HeadLodPoint.position));

            servoHone.Rotate(-(diff_minus - diff_plus), 0, 0);

            angle = servoHone.localEulerAngles.x;
            // 1. 180度より大きければ「マイナスの角度（逆回転）」として扱う
            if (angle > 180f)
                angle -= 360f;


            angle = Mathf.Clamp(angle, isOpposite ? -180f : 0f, isOpposite ? 0f : 180f);

            servoHone.localEulerAngles = new Vector3(angle, servoHone.localEulerAngles.y, servoHone.localEulerAngles.z);
            if (isOpposite)
            {
                angle = 180 - angle;
            }
            this.gameObject.name = $"{angle}";

            Debug.DrawLine(HornLodPoint.position + HornLodPoint.up, HeadLodPoint.position, diff_minus > diff_plus ? Color.green : Color.red);
            Debug.DrawLine(HornLodPoint.position - HornLodPoint.up, HeadLodPoint.position, diff_minus > diff_plus ? Color.red : Color.green);
            // print(Vector3.Distance(HornLodPoint.position, HeadLodPoint.position));
            // print(servoHone.localEulerAngles.x);
        }

    }
}

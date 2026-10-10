using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Collections.Specialized;

public class servocopy : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public GameObject servo;
    public List<GameObject> servos = new List<GameObject>();
    void Start()
    {
        Vector3 initialPosition = transform.localPosition;
        Quaternion initialRotation = transform.localRotation;

        this.transform.localPosition = Vector3.zero;
        this.transform.localRotation = Quaternion.Euler(-90f, 0f, 0f);

        servos.Add(servo);
        for (int i = 1; i < 6; i++)
        {
            GameObject copy = Instantiate(servo, this.transform);

            // print(i / 2 * 360 / 3);

            if (i % 2 == 1)
            {

                copy.transform.localRotation = Quaternion.Euler(0, 0, 180);
                copy.transform.localPosition = new Vector3(-copy.transform.localPosition.x, copy.transform.localPosition.y, copy.transform.localPosition.z);


                // Transform hone = servo.GetComponent<servo>().servoHone;
                // hone.localScale = new Vector3(hone.localScale.x, hone.localScale.y, -hone.localScale.z);
                copy.GetComponent<servo>().isOpposite = true;
            }
            copy.transform.RotateAround(this.transform.position, Vector3.up, i / 2 * 360 / 3);
            servos.Add(copy);
        }

        // servosのidを設定
        // HeadLodPointはHead原点を中心に反転・回転 (Headが斜め・別位置でもOK)
        transform.localPosition = initialPosition;
        transform.localRotation = initialRotation;

        Transform head = GameObject.Find("Head").transform;

        // 基準(0番)を先にHead下へ付けてHeadローカル位置を取得
        servos[0].GetComponent<servo>().HeadLodPoint.SetParent(head, true);
        Vector3 refLocal = servos[0].GetComponent<servo>().HeadLodPoint.localPosition;
        servos[0].GetComponent<servo>().id = 0;

        for (int i = 1; i < servos.Count; i++)
        {
            Vector3 p = refLocal;

            if (i % 2 == 1)
                p = new Vector3(-p.x, p.y, p.z);

            float angle = (i / 2) * 360f / 3f;
            p = Quaternion.Euler(0f, 0f, -angle) * p;

            servos[i].GetComponent<servo>().HeadLodPoint.SetParent(head, false);
            servos[i].GetComponent<servo>().HeadLodPoint.localPosition = p;
            servos[i].GetComponent<servo>().id = i;
        }


        // StartCoroutine(SerialCoroutine());
    }

}

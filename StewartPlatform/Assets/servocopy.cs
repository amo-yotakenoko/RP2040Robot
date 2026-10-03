using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class servocopy : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public GameObject servo;
    public List<GameObject> servos = new List<GameObject>();
    void Start()
    {
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
                Vector3 headLodPoint = copy.GetComponent<servo>().HeadLodPoint.localPosition;
                headLodPoint = new Vector3(headLodPoint.x, -headLodPoint.y, headLodPoint.z);
                copy.GetComponent<servo>().HeadLodPoint.localPosition = headLodPoint;
            }
            copy.transform.RotateAround(this.transform.position, Vector3.up, i / 2 * 360 / 3);
            servos.Add(copy);
        }

        // servosのidを設定
        for (int i = 0; i < servos.Count; i++)
        {
            servos[i].GetComponent<servo>().HeadLodPoint.SetParent(GameObject.Find("Head").transform);
            servos[i].GetComponent<servo>().id = i;
        }



        // StartCoroutine(SerialCoroutine());
    }

}

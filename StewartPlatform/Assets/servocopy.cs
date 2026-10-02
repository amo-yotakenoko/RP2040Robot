using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class servocopy : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public GameObject servo;
    List<GameObject> servos = new List<GameObject>();
    void Start()
    {
        servos.Add(servo);
        for (int i = 1; i < 6; i++)
        {
            GameObject copy = Instantiate(servo, this.transform);

            print(i / 2 * 360 / 3);

            if (i % 2 == 1)
            {

                copy.transform.localRotation = Quaternion.Euler(0, 0, 180);
                copy.transform.localPosition = new Vector3(-copy.transform.localPosition.x, copy.transform.localPosition.y, copy.transform.localPosition.z);
                servos.Add(copy);


                // Transform hone = servo.GetComponent<servo>().servoHone;
                // hone.localScale = new Vector3(hone.localScale.x, hone.localScale.y, -hone.localScale.z);
                copy.GetComponent<servo>().isOpposite = true;
            }
            copy.transform.RotateAround(this.transform.position, Vector3.up, i / 2 * 360 / 3);
        }

        // servosのidを設定
        for (int i = 0; i < servos.Count; i++)
        {
            servos[i].GetComponent<servo>().id = i;
        }
    }

    // Update is called once per frame
    void Update()
    {

    }
}

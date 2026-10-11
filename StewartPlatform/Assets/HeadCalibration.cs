using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;

public class HeadCalibration : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created

    void Start()
    {
        // StartCoroutine(Caliblation());

    }

    // Update is called once per frame
    void Update()
    {
        if (Keyboard.current.cKey.wasPressedThisFrame)
        {
            Caliblation();
        }
    }




    void Caliblation()
    {


        Transform head = GameObject.Find("Head").transform;
        Transform target = GameObject.Find("HeadCalibrationTarget").transform;

        // this から見た head の相対姿勢(間に何段あっても同じ)
        Quaternion relRot = Quaternion.Inverse(this.transform.rotation) * head.rotation;
        Vector3 relPos = this.transform.InverseTransformPoint(head.position);

        // 1. 回転: head のワールド回転が target になるように this を回す
        this.transform.rotation = target.rotation * Quaternion.Inverse(relRot);

        // 2. 位置: head のワールド位置が target になるように this を動かす
        this.transform.position = target.position - this.transform.rotation * Vector3.Scale(relPos, this.transform.localScale);



    }
}

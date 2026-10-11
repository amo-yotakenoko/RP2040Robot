using System.Collections.Generic;
using UnityEngine;

public class FaceMesh : MonoBehaviour
{
    [Header("Eye / Mouth Curves")]
    public AnimationCurve eyeCurve = AnimationCurve.Linear(0f, 0f, 1f, 1f);
    public AnimationCurve mouthCurve = AnimationCurve.Linear(0f, 0f, 1f, 1f);

    // 目関連: 眉 + 目
    private static readonly HashSet<string> EyeRelated = new HashSet<string>
    {
        "browDownLeft",
        "browDownRight",
        "browInnerUp",
        "browOuterUpLeft",
        "browOuterUpRight",
        "eyeBlinkLeft",
        "eyeBlinkRight",
        "eyeLookDownLeft",
        "eyeLookDownRight",
        "eyeLookInLeft",
        "eyeLookInRight",
        "eyeLookOutLeft",
        "eyeLookOutRight",
        "eyeLookUpLeft",
        "eyeLookUpRight",
        "eyeSquintLeft",
        "eyeSquintRight",
        "eyeWideLeft",
        "eyeWideRight",
    };

    // 口関連: 頬 + 顎 + 口 + 鼻
    private static readonly HashSet<string> MouthRelated = new HashSet<string>
    {
        "cheekPuff",
        "cheekSquintLeft",
        "cheekSquintRight",
        "jawForward",
        "jawLeft",
        "jawOpen",
        "jawRight",
        "mouthClose",
        "mouthDimpleLeft",
        "mouthDimpleRight",
        "mouthFrownLeft",
        "mouthFrownRight",
        "mouthFunnel",
        "mouthLeft",
        "mouthLowerDownLeft",
        "mouthLowerDownRight",
        "mouthPressLeft",
        "mouthPressRight",
        "mouthPucker",
        "mouthRight",
        "mouthRollLower",
        "mouthRollUpper",
        "mouthShrugLower",
        "mouthShrugUpper",
        "mouthSmileLeft",
        "mouthSmileRight",
        "mouthStretchLeft",
        "mouthStretchRight",
        "mouthUpperUpLeft",
        "mouthUpperUpRight",
        "noseSneerLeft",
        "noseSneerRight",
    };

    public void setBlendShape(string blendShapeName, float value)
    {
        float weight = value;

        if (EyeRelated.Contains(blendShapeName))
        {
            if (eyeCurve != null)
                weight = eyeCurve.Evaluate(weight);
        }
        else if (MouthRelated.Contains(blendShapeName))
        {
            if (mouthCurve != null)
                weight = mouthCurve.Evaluate(weight);
        }
        // _neutral 等、上記以外はカーブなしで素通し

        foreach (SkinnedMeshRenderer skinnedMeshRenderer in GetComponentsInChildren<SkinnedMeshRenderer>())
        {
            if (skinnedMeshRenderer != null)
            {
                int blendShapeIndex = skinnedMeshRenderer.sharedMesh.GetBlendShapeIndex(blendShapeName);
                if (blendShapeIndex >= 0)
                {
                    skinnedMeshRenderer.SetBlendShapeWeight(blendShapeIndex, weight * 100f);
                }
            }
        }
    }
}

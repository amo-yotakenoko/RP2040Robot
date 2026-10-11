using UnityEngine;

public class FaceMesh : MonoBehaviour
{


    public AnimationCurve eyeBlinkCurve;

    public void setBlendShape(string blendShapeName, float value)
    {
        float weight = value;
        weight = eyeBlinkCurve.Evaluate(weight);

        foreach (SkinnedMeshRenderer skinnedMeshRenderer in GetComponentsInChildren<SkinnedMeshRenderer>())
        {
            if (skinnedMeshRenderer != null)
            {
                print(skinnedMeshRenderer);
                int blendShapeIndex = skinnedMeshRenderer.sharedMesh.GetBlendShapeIndex(blendShapeName);
                if (blendShapeIndex >= 0)
                {
                    skinnedMeshRenderer.SetBlendShapeWeight(blendShapeIndex, weight * 100f);
                }
                else
                {
                    // Debug.LogWarning($"Blend shape '{blendShapeName}' not found.");
                }
            }
            else
            {
                // Debug.LogWarning("SkinnedMeshRenderer component not found.");
            }
        }
    }
}

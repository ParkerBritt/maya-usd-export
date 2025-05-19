#pragma once

#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/prim.h>
#include <pxr/usd/usdGeom/mesh.h>
#include <pxr/usd/usdGeom/primvar.h>
#include "export/ExportItem.h"
#include "export/ExportOptions.h"
#include "maya/MApiNamespace.h"

namespace MayaUSDExport {

/**
 * @class PrimWriter
 * @brief Responsible for writing Maya primitives to a USD stage.
 *
 * This class provides functionality to export scene elements (primitives) 
 * from Maya into a USD file. It handles the conversion of Maya geometry,
 * animation data, and scene hierarchy into appropriate USD representations.
 */
class PrimWriter {
public:

    /**
     * @brief Constructor for the PrimWriter.
     * @param _exportOptions Reference to export options that guide the export behavior.
     */
    PrimWriter(ExportOptions& _exportOptions);

    /**
     * @brief Write all added export items to the given USD stage.
     * @param stage A reference pointer to the USD stage where primitives will be written.
     */
    void writePrims(pxr::UsdStageRefPtr stage);

    /**
     * @brief Add a new export item to be written to USD.
     * @param _exportItem The item containing Maya DAG information and metadata for export.
     */
    void addExportItem(ExportItem _exportItem);

    /**
     * @brief Set the animation frame range for exporting animated geometry.
     * @param frameStart The starting frame of the animation.
     * @param frameEnd The ending frame of the animation.
     */
    void setAnim(float frameStart, float frameEnd);

    /**
     * @brief Derive the USD primitive type from a given Maya DAG path.
     * @param dagPath The DAG path to analyze.
     * @param promoteShapes Whether to promote Maya shapes to their corresponding USD types.
     * @return A string representing the USD primitive type name.
     */
    static std::string derivePrimType(MDagPath dagPath, bool promoteShapes = true);

    /// List of export items queued for writing.
    std::vector<ExportItem> m_exportItems;

private:

    /**
     * @brief Convert Maya vertex points to USD-compatible format.
     * @param _meshPath The DAG path to the Maya mesh.
     * @return An array of USD vectors representing point positions.
     */
    pxr::VtArray<pxr::GfVec3f> convertMayaPoints(MDagPath _meshPath);

    /// Reference to the export options used during export.
    ExportOptions& m_exportOptions;

    /**
     * @brief Animate vertex positions for a given export item.
     * @param _pointsAttr The USD points attribute to animate.
     * @param _exportItem The export item containing mesh and DAG path.
     */
    void animatePoints(pxr::UsdAttribute _pointsAttr, ExportItem _exportItem);

    /**
     * @brief Build UV primvar data on a USD mesh from a Maya mesh.
     * @param _usdMesh The target USD mesh to receive UVs.
     * @param _mayaMesh The Maya mesh containing UV information.
     * @return The generated USD primvar containing UV data.
     */
    pxr::UsdGeomPrimvar buildUVs(pxr::UsdGeomMesh& _usdMesh, MFnMesh& _mayaMesh);

    /**
     * @brief Determine and handle the type of a DAG path.
     * @param dagPath The DAG path to inspect.
     */
    void getDagPathType(const MDagPath& dagPath);

    /**
     * @brief Set the type of a USD prim based on a token name.
     * @param prim The USD prim whose type is being set.
     * @param primTypeName The token representing the USD type.
     */
    void setPrimType(pxr::UsdPrim& prim, const pxr::TfToken& primTypeName);

    /**
     * @brief Apply transformation from Maya DAG path to USD prim.
     * @param usdPrim The target USD primitive.
     * @param dagPath The source Maya DAG path.
     */
    void setTransform(pxr::UsdPrim usdPrim, MDagPath dagPath);
};

}

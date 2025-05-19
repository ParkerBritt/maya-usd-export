#ifndef EXPORT_ITEM_H
#define EXPORT_ITEM_H

#include <maya/MDagPath.h>
#include <pxr/base/tf/token.h>

/**
 * @file ExportItem.h
 * @brief Defines the ExportItem class used in the Maya to USD export process.
 */

namespace MayaUSDExport {

/**
 * @class ExportItem
 * @brief Represents a single Maya DAG node intended for export to USD.
 *
 * ExportItem encapsulates the essential data required to export a Maya object
 * to USD. It stores the DAG path of the Maya object and the corresponding USD
 * primitive type that it should be represented as.
 *
 * @note Future implementations may include export arguments for finer control.
 */
class ExportItem {
public:
    /**
     * @brief Constructor that initializes the export item with a Maya DAG path.
     * 
     * @param dagPath The DAG path of the Maya object to be exported.
     */
    ExportItem(MDagPath dagPath);

    /**
     * @brief The DAG path of the Maya node associated with this export item.
     */
    MDagPath dagPath;

    /**
     * @brief Sets the USD primitive type for this item.
     *
     * @param usdTypeName A TfToken specifying the USD primitive type
     *                    (e.g., "Mesh", "Xform").
     */
    void setPrimType(pxr::TfToken usdTypeName) { usdTypeName_ = usdTypeName; }

    /**
     * @brief Gets the USD primitive type assigned to this item.
     *
     * @return A TfToken representing the USD primitive type.
     */
    pxr::TfToken getPrimType() { return usdTypeName_; }

private:
    /**
     * @brief The USD primitive type name (e.g., "Mesh", "Xform") to export as.
     */
    pxr::TfToken usdTypeName_;
};

} // namespace MayaUSDExport

#endif // EXPORT_ITEM_H

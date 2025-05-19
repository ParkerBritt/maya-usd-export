#pragma once

#include <string>

/**
 * @file ExportOptions.h
 * @brief Defines export configuration options for Maya to USD export.
 */

namespace MayaUSDExport
{

/**
 * @class ExportOptions
 * @brief Holds configuration options that control the behavior of a Maya to USD export.
 *
 * This class provides basic options for animation frame range and structural control 
 * during the export process. It's planned to be extended in the future to support more advanced settings.
 */
class ExportOptions
{
public:
    /**
     * @brief The start frame for animation export.
     *
     * Only frames starting from this value (inclusive) will be included in the exported USD data.
     */
    int animFrameStart = 0;

    /**
     * @brief The end frame for animation export.
     *
     * Only frames up to this value (inclusive) will be included in the exported USD data.
     */
    int animFrameEnd = 0;

    /**
     * @brief The increment between animation frames to export.
     *
     * For example, if set to 2, every other frame will be exported.
     */
    int animFrameInc = 1;

    /**
     * @brief Whether to automatically create any missing parent nodes in the USD hierarchy.
     *
     * If true, the exporter will generate parent USD primitives for any nodes that 
     * do not have a complete hierarchy exported from Maya.
     */
    bool createParents = false;
};

}

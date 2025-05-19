#include <catch2/catch_test_macros.hpp>
#include "export.h"
#include "export/exportItem.h"
#include <maya/MDagPath.h>


TEST_CASE( "Test export", "[export]" ) {
    REQUIRE( 1 == 1 );
}

TEST_CASE("ExportItem", "[export]"){
    MDagPath path;
    MayaUSDExport::ExportItem exportItem(path);
}
